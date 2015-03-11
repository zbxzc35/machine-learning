# 决策树
主要实现了ID3/C4.5/CART三个决策树算法
## 信息增益（Information Gain）
#### 信息增益存在的问题
一个属性的信息增益越大，表明属性对样本的熵减少的能力更强，这个属性使得数据由不确定性变成确定性的能力越强。  
所以如果是取值更多的属性，更容易使得数据更“纯”（尤其是连续型数值），其信息增益更大，决策树会首先挑选这个属性作为树的顶点。  
结果训练出来的形状是一棵庞大且深度很浅的树，这样的划分是极为不合理的。  
对于取值多的属性，尤其一些连续型数值，比如两条地理数据的距离属性，这个单独的属性就可以划分所有的样本，使得所有分支下的样本集合都是“纯的”（最极端的情况是每个叶子节点只有一个样本）。
## 信息增益比（Information Gain Ratio）
#### 什么是信息增益比？
The information gain ratio is just the ratio between the information gain and the intrinsic value
#### 为什么用信息增益比？  
选择信息增益比可以对信息增益存在的问题进行校正。这是特征选择的另一标准。  
C4.5使用了信息增益比，用信息增益除以一项split information（intrinsic value）,来惩罚值更多的属性。
信息增益比公式参考[Wiki](http://en.wikipedia.org/wiki/Information_gain_ratio)  
## 基尼指数 （Gini Index）
## ID3算法
## C4.5算法
## CART算法  
