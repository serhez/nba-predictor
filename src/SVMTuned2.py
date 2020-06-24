import optunity
import optunity.metrics
import sklearn.svm
from sklearn import metrics
import Generator


train_paths = ["../Data/2017-2018/traditional.csv", "../Data/2016-2017/traditional.csv"]
(X_train, y_train) = Generator.generate(train_paths)

test_path = ["../Data/2018-2019/traditional.csv"]
(X_test, y_test) = Generator.generate(test_path)

print(1)

# score function: twice iterated 10-fold cross-validated accuracy
@optunity.cross_validated(x=X_train, y=y_train, num_folds=10, num_iter=2)
def svm_auc(x_train, y_train, x_test, y_test, logC, logGamma):
    model = sklearn.svm.SVC(C=10 ** logC, gamma=10 ** logGamma).fit(x_train, y_train)
    decision_values = model.decision_function(x_test)
    return optunity.metrics.roc_auc(y_test, decision_values)

print(2)

# perform tuning
hps, _, _ = optunity.maximize(svm_auc, num_evals=200, logC=[-5, 2], logGamma=[-5, 1])

print(3)

# train model on the full training set with tuned hyperparameters
optimal_model = sklearn.svm.SVC(C=10 ** hps['logC'], gamma=10 ** hps['logGamma']).fit(X_train, y_train)

print(4)

y_pred = optimal_model.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

count0 = 0.0
count1 = 0.0
for y in y_pred:
    if y == 0.0:
        count0 += 1.0
    else:
        count1 += 1.0
print('Count of pred 0s = ' + str(count0))
print('Count of pred 1s = ' + str(count1))
print('Pred ratio 0s/1s = ' + str(count0/count1))
