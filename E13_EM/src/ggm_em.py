#!/usr/bin/env python
# coding: utf-8

# In[1]:


# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def loadData(filename):
    """从文件中读取数据。"""
    dataSet = []
    id2country = []  # 将索引对应到国家名
    with open(filename) as fr:
        for i, line in enumerate(fr.readlines()):
            curLine = line.strip().split(' ')
            fltLine = list(map(int, curLine[1:]))  # 去掉第一列国家名
            dataSet.append(fltLine)
            id2country.append(curLine[0])
    return dataSet, id2country


# In[3]:


def prob(x, mu, sigma):
    """高斯分布的概率密度函数。"""
    n = np.shape(x)[1]
    expOn = float(-0.5 * (x - mu) * (sigma.I) * ((x - mu).T))
    divBy = pow(2 * np.pi, n / 2) * pow(np.linalg.det(sigma), 0.5)
    return pow(np.e, expOn) / divBy


# In[4]:


def EM(dataMat, maxIter=50):
    m, n = np.shape(dataMat)
    # 1.初始化各高斯混合成分参数
    alpha = [1/3, 1/3, 1/3]                                  # 初始化 alpha
    mu = [dataMat[1, :], dataMat[13, :], dataMat[11, :]]           # 初始化mu
    sigma = [np.mat((np.eye(7, dtype=float))) for x in range(3)]  # 初始化协方差矩阵
    gamma = np.mat(np.zeros((m, 3)))
    
    for i in range(maxIter):
        for j in range(m):
            sumAlphaMulP = 0
            for k in range(3):
                gamma[j, k] = alpha[k] * prob(dataMat[j, :], mu[k], sigma[k]) # 4.计算混合成分生成的后验概率，即gamma
                sumAlphaMulP += gamma[j, k]
            for k in range(3):
                gamma[j, k] /= sumAlphaMulP
        sumGamma = np.sum(gamma, axis=0)

        for k in range(3):
            mu[k] = np.mat(np.zeros((1, n)))
            sigma[k] = np.mat(np.zeros((n, n)))
            for j in range(m):
                mu[k] += gamma[j, k] * dataMat[j, :]
            mu[k] /= sumGamma[0, k] #  7.计算新均值向量
            for j in range(m):
                sigma[k] += gamma[j, k] * (dataMat[j, :] - mu[k]).T *(dataMat[j, :] - mu[k])
            sigma[k] /= sumGamma[0, k]  # 8. 计算新的协方差矩阵
            alpha[k] = sumGamma[0, k] / m   # 9. 计算新混合系数
        
        for s in sigma:
            s += np.eye(7)
            
    print('gamma')
    [print(g) for g in gamma]
    print('\nmu')
    [print(m) for m in mu]
    print('\nsigma')
    [print(s) for s in sigma]
    
    return gamma


# In[5]:


def initCentroids(dataMat, k):
    """Init centroids with random samples."""
    numSamples, dim = dataMat.shape
    centroids = np.zeros((k, dim))
    for i in range(k):
        index = int(np.random.uniform(0, numSamples))
        centroids[i, :] = dataMat[index, :]
    return centroids


# In[6]:


def gaussianCluster(dataMat):
    """进行聚类。"""
    m, n = np.shape(dataMat)
    centroids = initCentroids(dataMat, m)  ## step 1: init centroids
    clusterAssign = np.mat(np.zeros((m, 2)))
    gamma = EM(dataMat)
    for i in range(m):
        # amx返回矩阵最大值，argmax返回矩阵最大值所在下标
        clusterAssign[i, :] = np.argmax(gamma[i, :]), np.amax(gamma[i, :])  # 15.确定x的簇标记lambda
        ## step 4: update centroids
    for j in range(m):
        pointsInCluster = dataMat[np.nonzero(clusterAssign[:, 0].A == j)[0]]
        centroids[j, :] = np.mean(pointsInCluster, axis=0)  # 计算出均值向量
    return centroids, clusterAssign


# In[7]:


dataMat, id2country = loadData('football.txt')
dataMat = np.mat(dataMat)
centroids, clusterAssign = gaussianCluster(dataMat)


# In[8]:


result = ([], [], [])
for i, assign in enumerate(clusterAssign):
    result[int(assign[0, 0])].append(id2country[i])
print('\n-------------------------------------------\n')
print('First-class:', result[0])
print('Second-class:', result[1])
print('Third-class:', result[2])


# In[ ]:




