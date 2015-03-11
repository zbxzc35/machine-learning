# -*- coding: UTF-8 –*-
__author__ = 'DragonflyLiu'
from math import log2


def calcShannoEnt(dataSet):
    """计算熵，混合的数据越多，熵越高"""
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        # 这里也可以使用collections里面的defaultdict来直接实现+=操作
        labelCounts[currentLabel] = labelCounts.get(currentLabel, 0) + 1
    shannoEnt = 0.0
    for label in labelCounts:
        prob = labelCounts[label]/numEntries
        shannoEnt -= prob * log2(prob)
    return shannoEnt

def createDataSet():
    """创建数据集"""
    # dataSet = [[1, 1, 'yes'],
    #            [1, 1, 'yes'],
    #            [1, 0, 'no'],
    #            [0, 1, 'no'],
    #            [0, 1, 'no']]
    # labels = ['no surfacing', 'flippers']
    # return dataSet, labels
    filename = '../data/lenses.txt'
    with open(filename, 'r', encoding='utf8', errors='ignore') as infile:
        dataSet = [line.strip().split('\t') for line in infile]
        labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    """按照特征值分割数据集"""
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    """选择最好的特征"""
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannoEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featureList = (featVec[i] for featVec in dataSet)
        uniqueVals = set(featureList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / len(dataSet)
            newEntropy += prob * calcShannoEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    """用投票法选出类别"""
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote, 0) + 1
    # 这里也可以用operator.itemgetter来代替lambda
    sortedClassCount = sorted(classCount.items(), key=lambda item : item[1], reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    """递归的创建决策树"""
    # 返回条件1，如果类别完全相同，则停止继续划分
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 返回条件2，如果所有的特征已经被遍历完，则停止继续划分，返回出现次数最多的
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    # 返回条件3， 如果信息增益小于某个阈值，则停止继续划分，返回出现次数最多的
    # 递归创建子树
    bestFeature = chooseBestFeatureToSplit(dataSet)
    bestFeatureLabel = labels[bestFeature]
    myTree = {bestFeatureLabel:{}}
    # 以A-{Ag}为特征值递归
    del labels[bestFeature]
    featValues = (example[bestFeature] for example in dataSet)
    uniqueVals = set(featValues)
    # ID3的特点是根据值的个数确定分支的个数
    for value in uniqueVals:
        # deep copy
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree(splitDataSet(dataSet, bestFeature, value), subLabels)

    return myTree

def getNumLeafs(myTree):
    """递归的方式求解叶子的数目"""
    # numLeafs = 0
    # for value in myTree.values():
    #     if type(value) is dict:
    #         numLeafs += getNumLeafs(value)
    #     else:
    #         numLeafs += 1
    # return numLeafs
    # 注意起始位置
    numleafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for value in secondDict.values():
        if type(value) is dict:
            numleafs += getNumLeafs(value)
        else:
            numleafs += 1
    return numleafs

def getTreeDepth(myTree):
    """递归的方式求解树的深度"""
    # 注意起始位置
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for value in secondDict.values():
        if type(value) is dict:
            thisDepth = 1 + getTreeDepth(value)
        else:
            thisDepth = 1
        if maxDepth < thisDepth:
            maxDepth = thisDepth
    return maxDepth

def classify(inputTree, featLabels, testVec):
    """递归的分类"""
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]) is dict:
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

# 使用pickle模块存储决策树
def saveTree(inputTree, filename):
    import pickle
    with open(filename, 'w') as infile:
        pickle.dump(inputTree, infile)

def grabTree(inputTree, filename):
    import pickle
    with open(filename, 'r') as outfile:
        return pickle.load(outfile)

if __name__ == '__main__':
    dataSet, labels = createDataSet()
    myTree = createTree(dataSet, labels[:])
    print(myTree)
    print(classify(myTree, labels, ['presbyopic', 'myope', 'no', 'reduced']))