from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
import Generator

train_paths = ["../Data/2017-2018/traditional.csv", "../Data/2016-2017/traditional.csv"]
(X_train, y_train) = Generator.generate(train_paths)

test_path = ["../Data/2018-2019/traditional.csv"]
(X_test, y_test) = Generator.generate(test_path)

# paths = ["../Data/2017-2018/traditional.csv", "../Data/2016-2017/traditional.csv", "../Data/2018-2019/traditional.csv"]
# (X, y) = Generator.generate(paths)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=109)

# Set the parameters by cross-validation
tuned_parameters = [{'C': [1, 10, 100, 1000, 10000, 100000, 1000000], 'max_iter': [100, 1000, 10000, 100000], 'solver': ['lbfgs']}]

print("# Tuning hyper-parameters for %s" % 'accuracy')
print()
clf = GridSearchCV(LogisticRegression(), tuned_parameters, cv=5,
                   scoring='accuracy')
clf.fit(X_train, y_train)

print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
          % (mean, std * 2, params))
    print()

print("Detailed classification report:")
print()
print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")
print()
y_true, y_pred = y_test, clf.predict(X_test)
print(classification_report(y_true, y_pred))
print()

# count0 = 0.0
# count1 = 0.0
# for i in y:
#     if i == 0.0:
#         count0 += 1.0
#     else:
#         count1 += 1.0
# print('Count of real 0s = ' + str(count0))
# print('Count of real 1s = ' + str(count1))
# print('Real % 1s/0s = ' + str(count1/(count1+count0)))
# print()
# print()

count0 = 0.0
count1 = 0.0
for y in y_test:
    if y == 0.0:
        count0 += 1.0
    else:
        count1 += 1.0
print('Count of test 0s = ' + str(count0))
print('Count of test 1s = ' + str(count1))
print('Test % 1s/0s = ' + str(count1/(count1+count0)))
print()
print()

count0 = 0.0
count1 = 0.0
for y in y_pred:
    if y == 0.0:
        count0 += 1.0
    else:
        count1 += 1.0
print('Count of pred 0s = ' + str(count0))
print('Count of pred 1s = ' + str(count1))
print('Pred % 1s/0s = ' + str(count1/(count1+count0)))

# model = LogisticRegression()
# model.fit(X_train, y_train)
#
# # predict class labels for the test set
# predicted = model.predict(X_test)
#
# # generate class probabilities
# probs = model.predict_proba(X_test)
#
# # generate evaluation metrics
# print('Test Acc = ' + str(metrics.accuracy_score(y_test, predicted)))
