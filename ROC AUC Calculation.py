#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 19:16:47 2019

@author: alex liu
"""

# Import Data
import pandas as pd
data = pd.read_csv("C:/Users/alexliuyi/Documents/LAHealth/model_outcome.csv")

#%%
# 1. Manually calculate the sensitivity and specificity of the model, 
#    using a predicted_prob threshold of greater than or equal to .5.
import numpy as np

def FPR_TPR_Calculator(threshold):
    #Calculate predicted class with prob
    data["predicted_class"] = np.where(data.predicted_prob >= threshold, 1,0)
    
    # Create confusion matrix 
    data["TP"] = np.where((data["class"]==1) & (data["predicted_class"]==1), 1,0)
    data["FN"] = np.where((data["class"]==1) & (data["predicted_class"]!=1), 1,0)
    data["FP"] = np.where((data["class"]!=1) & (data["predicted_class"]==1), 1,0)
    data["TN"] = np.where((data["class"]!=1) & (data["predicted_class"]!=1), 1,0)
    
    TP = np.sum(data.TP)
    FN = np.sum(data.FN)
    FP = np.sum(data.FP)
    TN = np.sum(data.TN)
    
    # Calculate sensitivity
    sensitivity = TP/(TP+FN)
    # Calculate specificity
    specificity = TN/(TN+FP)
    # Return FPR and TPR
    return round(1-specificity,4),round(sensitivity,4)


# Calculate sensitivity and specificity when threshold = 0.5
FPR, TPR = FPR_TPR_Calculator(0.5)

print("Sensitivity of the model is %.4f"% TPR)
print("Specificity of the model is %.4f"% (1-FPR))
#%%
#2. Manually calculate the Area Under the Receiver Operating Characteristic Curve.
# Create 1000 cut point between 0 and 1
threshold = np.linspace(1,0,1000)
# Create empty list for FPR and TPR
FPR = list()
TPR = list()
# For each cup point, append FPR and TPR
for i in threshold:
    temp_FPR, temp_TPR = FPR_TPR_Calculator(i)
    FPR.append(temp_FPR)
    TPR.append(temp_TPR)
# Transfer list to numpp array
FPR = np.array(FPR)
TPR = np.array(TPR)   
# Caluculate AUC 
AUC = 1/2*np.sum((FPR[1:]-FPR[0:-1])*(TPR[0:-1]+TPR[1:]))
# Print result
print("The AUC of the model is: %.4f"%AUC)
#%%
#3. Visualize the Receiver Operating Characterstic Curve.
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(FPR, TPR)
ax.set(title = 'ROC Curve for the Baseline Model',
       xlabel = 'False Positive Rate',
       ylabel = 'True Positive Rate')
plt.show()
#%%
