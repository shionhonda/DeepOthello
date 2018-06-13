# What is IaGo?
IaGo is an Othello AI using SL(supervised learning) policy network inspired by AlphaGo.  
It doesn't predict plays ahead, but it is still powerful.  
Description in Japanese:  
[AlphaGoを模したオセロAIを作る(1): SLポリシーネットワーク - Qiita](https://qiita.com/shionhonda/items/7a3eb79f55299e743630)

# How to play?  
1. Install chainer  
`$ pip install chainer`  

2. Download this repository  
`$ git clone git@github.com:shionhonda/IaGo.git`  

3. Execute game.py  
`$ python ./IaGo/game.py`

4. When placing a stone, input two numbers seperated by comma. For example:  
`4,3`  
The first number corresponds to the vertical position and the second to the horizontal.

# How to train?
1. Download data from <http://meipuru-344.hatenablog.com/entry/2017/11/27/205448>
2. Save it as "IaGo/data/data.txt"    
3. Augment data  
`$ python load.py`  
You need at least 32MB RAM to complete this step.  
4. Execute train.py  
`$ python train.py --epoch=180`  
You need GPU to complete this step. It will take about 2 days.

# Acknowledgements  
Special thanks to @lazmond3 for giving lots of feedbacks!
