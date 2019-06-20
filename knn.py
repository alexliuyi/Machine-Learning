import numpy as np

def knn(input, data, label, k):
    # Get number of observations in training set
    nobs = data.shape[0]
    # Make the new input the same shape of training set, 
    # and calculate the differenct bewteen new input and each training observation
    diff = np.tile(input, (nobs,1))-data
    squareDiff = diff**2
    squareDist = np.sum(squareDiff, axis=1) 
    distance = squareDist**0.5

    # Sort distance
    sortedDistIndices = np.argsort(distance)
    
    # Count k nearest observations
    classCount = {}
    for i in range(k):
        votelabel = label[sortedDistIndices[i]]
        classCount[votelabel]=classCount.get(votelabel,0)+1
    # Most frequently voted label
    maxCount = 0
    for k, v in classCount.items():
        if v > maxCount:
            maxCount = v
            maxIndex = k
    return maxIndex
