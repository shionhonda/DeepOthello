import argparse
import numpy as np
from tqdm import tqdm

import chainer
import chainer.links as L
from chainer import serializers, cuda, optimizers, Variable
from chainer.functions import mean_squared_error

import value

def main():
	# Set the number of epochs
	parser = argparse.ArgumentParser(description='IaGo:')
	parser.add_argument('--epoch', '-e', type=int, default=100, help='Number of sweeps over the dataset to train')
	parser.add_argument('--gpuid', '-g', type=int, default=0, help='Number of sweeps over the dataset to train')
	args = parser.parse_args()

	# Model definition
	model = value.ValueNet()
	optimizer = optimizers.Adam()
	optimizer.setup(model)
	optimizer.add_hook(chainer.optimizer_hooks.WeightDecay(5e-4))
	cuda.get_device(args.gpuid).use()

	test_x = np.load('./value_data/npy/states_test.npy')
	test_y = np.load('./value_data/npy/results_test.npy')
	test_x = np.stack([test_x==1, test_x==2], axis=0).astype(np.float32)
	test_x = chainer.Variable(cuda.to_gpu(test_x.transpose(1,0,2,3)))
	test_y = chainer.Variable(cuda.to_gpu(test_y.astype(np.float32)))

	# Load train dataset
	train_x = np.load('./value_data/npy/states.npy')
	train_y = np.load('./value_data/npy/results.npy')
	train_size = train_y.shape[0]
	minibatch_size = 4096 # 2**12

	# Learing loop
	for epoch in tqdm(range(args.epoch)):
		model.to_gpu(args.gpuid)
		# Shuffle train dataset
		rands = np.random.choice(train_size, train_size, replace=False)
		train_x = train_x[rands,:,:]
		train_y = train_y[rands]

		# Minibatch learning
		for idx in tqdm(range(0, train_size, minibatch_size)):
			x = train_x[idx:min(idx+minibatch_size, train_size), :, :]
			x = np.stack([x==1, x==2], axis=0).astype(np.float32)
			x = chainer.Variable(cuda.to_gpu(x.transpose(1,0,2,3)))
			y = train_y[idx:min(idx+minibatch_size, train_size)]
			y = chainer.Variable(cuda.to_gpu(y.astype(np.float32)))
			train_pred = model(x)
			train_loss = mean_squared_error(train_pred, y)
			model.cleargrads()
			train_loss.backward()
			optimizer.update()
		# Calculate loss
		with chainer.using_config('train', False), chainer.using_config('enable_backprop', False):
			test_pred = model(test_x)
			test_loss = mean_squared_error(test_pred, test_y)
			print('\nepoch :', epoch, '  loss :', test_loss.data)
			# Log
			with open("./log_value.txt", "a") as f:
				f.write(str(test_loss.data)+", \n")
		# Save models
		model.to_cpu()
		serializers.save_npz('./models/value_model.npz', model)
		serializers.save_npz('./models/value_optimizer.npz', optimizer)
		# Early stop
		#if loss<0.94:
		#	print("Early stop")
		#	break

if __name__ == '__main__':
    main()
