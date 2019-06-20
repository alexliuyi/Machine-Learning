#Input data
data <- read.csv("C:/Users/alexliuyi/Documents/LAHealth/model_outcome.csv")

# Check Data
head(data,3)
# Output:
# index class predicted_prob
# 1     1     0     0.59283738
# 2     2     1     0.62482872
# 3     3     0     0.07384827

dim(data)
# OUtput:
#[1] 1000    3

summary(data)
# Output:
# index            class       predicted_prob     
# Min.   :   1.0   Min.   :0.000   Min.   :0.0009673  
# 1st Qu.: 250.8   1st Qu.:0.000   1st Qu.:0.3132660  
# Median : 500.5   Median :0.000   Median :0.5153817  
# Mean   : 500.5   Mean   :0.492   Mean   :0.5101500  
# 3rd Qu.: 750.2   3rd Qu.:1.000   3rd Qu.:0.7023137  
# Max.   :1000.0   Max.   :1.000   Max.   :0.9942578  

# 1. Manually calculate the sensitivity and specificity of the model, using a predicted_prob threshold of greater than or equal to .5.

FPR_TPR_Calculator <- function(threshold){
  
  data$predicted_class <- ifelse(data$predicted_prob>=threshold, 1,0)
  
  data$TP <- ifelse((data$class==1) & (data$predicted_class==1), 1,0)
  data$FN <- ifelse((data$class==1) & (data$predicted_class!=1), 1,0)
  data$FP <- ifelse((data$class!=1) & (data$predicted_class==1), 1,0)
  data$TN <- ifelse((data$class!=1) & (data$predicted_class!=1), 1,0)
  
  TP <- sum(data$TP)
  FN <- sum(data$FN)
  FP <- sum(data$FP)
  TN <- sum(data$TN)
  # Calculate sensitivity
  sensitivity <- TP/(TP+FN)
  # Calculate specificity
  specificity <- TN/(TN+FP)
  
  result <- cbind(round(1-specificity,4), round(sensitivity,4))
  colnames(result) <- c("FPR","TPR")
  return(result)
}

# Calculate sensitivity and specificity when threshold = 0.5
task1 <- FPR_TPR_Calculator(0.5)

print(paste("Sensitivity of the model is: ", task1[2]))
print(paste("Specificity of the model is: ", (1-task1[1])))
# Output:
# [1] "Sensitivity of the model is:  0.8171"
# [1] "Specificity of the model is:  0.7579"

#2. Manually calculate the Area Under the Receiver Operating Characteristic Curve. Create 1000 cut point between 0 and 1
threshold <- seq(0,1,length.out = 1000)
threshold <- sort(threshold, decreasing = TRUE)

FPR.TPR <- c()
for(i in threshold){
  temp <- FPR_TPR_Calculator(i)
  FPR.TPR <- rbind(FPR.TPR, temp)
}

AUC <- 1/2*sum((FPR.TPR[2:dim(FPR.TPR)[1],1]-FPR.TPR[1:dim(FPR.TPR)[1]-1,1])*(FPR.TPR[2:dim(FPR.TPR)[1],2]+FPR.TPR[1:dim(FPR.TPR)[1]-1,2]))

print(paste("The AUC of the model is: ",round(AUC,4)))
# Output:
#[1] "The AUC of the model is:  0.8886"


#3. Visualize the Receiver Operating Characterstic Curve.
plot(FPR.TPR[,1],FPR.TPR[,2],
     type = "l",
     main = "ROC Curve for the Baseline Model",
     xlab = "False Positive Rate",
     ylab = "True Positive Rate")


