# -*- coding: UTF-8 –*-
__author__ = 'DragonflyLiu'
"""
C4.5的实现与ID3基本相同，不同的是C4.5使用了信息增益比，可以惩罚那些取值较多，信息增益大的属性
"""
from math import log2


def calcShannoEnt(dataSet):
    """calculate Shanno Entropy"""
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        labelCount[featVec[-1]] = labelCount.get(featVec[-1], 0) + 1
    entropy = 0.0
    for label in labelCount:
        prob = labelCount[label]/numEntries
        entropy -= prob * log2(prob)
    return entropy

def createDataSet():
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
    """split data set"""
    subDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            subFeatVec = featVec[:axis]
            subFeatVec.extend(featVec[axis+1:])
            subDataSet.append(subFeatVec)
    return subDataSet

def chooseBestFeature(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEnt = calcShannoEnt(dataSet)
    bestInfoGainRatio = 0.0
    bestFeature = -1
    bestFeatureValues = []
    for i in range(numFeatures):
        featList = [featVec[i] for featVec in dataSet]
        uniqueValues = set(featList)
        newEnt = 0.0
        intrinsicValue = 0.0
        for value in uniqueValues:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/len(dataSet)
            newEnt += prob * calcShannoEnt(subDataSet)
            # 计算intrinsicValue（split information）
            intrinsicValue -= prob * log2(prob)
        # 采用信息增益比
        infoGainRatio = (baseEnt - newEnt) / intrinsicValue
        if infoGainRatio > bestInfoGainRatio:
            bestInfoGainRatio = infoGainRatio
            bestFeature = i
            bestFeatureValues = uniqueValues
    return bestFeature, bestFeatureValues

def majorityCnt(classList):
    classCnt = {}
    for vote in classList:
        classCnt[vote] = classCnt.get(vote, 0) + 1
    sortedClassCnt = sorted(classCnt.items(), key=lambda item:item[1], reverse=True)
    return sortedClassCnt[0][0]

def createTree(dataSet, labels):
    """递归生成子树"""
    classList = [featVec[-1] for featVec in dataSet]
    # 停止条件1
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 停止条件2
    if len(labels) == 1:
        return majorityCnt(classList)
    # 停止条件3，信息增益比小于某个阈值

    # 递归生成子树
    bestFeature, bestFeatValues = chooseBestFeature(dataSet)
    bestFeatLabel = labels[bestFeature]
    myTree = {bestFeatLabel:{}}
    del labels[bestFeature]
    for value in bestFeatValues:
        subDataSet = splitDataSet(dataSet, bestFeature, value)
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(subDataSet, subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    labelIndex = featLabels.index(firstStr)
    for key in secondDict:
        if key == testVec[labelIndex]:
            if type(secondDict[key]) is dict:
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

if __name__ == '__main__':
    dataSet, labels = createDataSet()
    myTree = createTree(dataSet, labels[:])
    print(myTree)
    print(classify(myTree, labels, ['presbyopic', 'myope', 'no', 'reduced']))
