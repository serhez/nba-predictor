from sklearn import svm
from sklearn import metrics
import Generator

train_path1 = "../Data/2017-2018/traditional.csv"
(X_train1, y_train1) = Generator.generate(train_path1)
train_path2 = "../Data/2016-2017/traditional.csv"
(X_train2, y_train2) = Generator.generate(train_path2)

(X_train, y_train) = (X_train1 + X_train2), (y_train1 + y_train2)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=109)
test_path = "../Data/2018-2019/traditional.csv"
(X_test, y_test) = Generator.generate(test_path)

#Create a svm Classifier
clf1 = svm.SVC(kernel='linear')   # Linear Kernel
clf3 = svm.SVC(kernel='sigmoid')  # Sigmoid Kernel
clf4 = svm.SVC(kernel='rbf')      # RBF Kernel

#Train the model using the training sets
clf1.fit(X_train, y_train)
clf3.fit(X_train, y_train)
clf4.fit(X_train, y_train)

#Predict the response for test dataset
y_pred1 = clf1.predict(X_test)
y_pred3 = clf3.predict(X_test)
y_pred4 = clf4.predict(X_test)

print('\n----- Linear Kernel -----')
# Model Accuracy
print("Accuracy:", metrics.accuracy_score(y_test, y_pred1))
# Model Precision
print("Precision:", metrics.precision_score(y_test, y_pred1))
# Model Recall
print("Recall:", metrics.recall_score(y_test, y_pred1))
print(y_pred1)

print('\n----- Sigmoid Kernel -----')
# Model Accuracy
print("Accuracy:", metrics.accuracy_score(y_test, y_pred3))
# Model Precision
print("Precision:", metrics.precision_score(y_test, y_pred3))
# Model Recall
print("Recall:", metrics.recall_score(y_test, y_pred3))
print(y_pred3)

print('\n----- RBF Kernel -----')
# Model Accuracy
print("Accuracy:", metrics.accuracy_score(y_test, y_pred4))
# Model Precision
print("Precision:", metrics.precision_score(y_test, y_pred4))
# Model Recall
print("Recall:", metrics.recall_score(y_test, y_pred4))
print(y_pred4)