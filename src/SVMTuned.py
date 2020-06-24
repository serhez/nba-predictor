from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import Generator

train_paths = ["../Data/2017-2018/traditional.csv", "../Data/2016-2017/traditional.csv"]
(X_train, y_train) = Generator.generate(train_paths)

test_path = ["../Data/2018-2019/traditional.csv"]
(X_test, y_test) = Generator.generate(test_path)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['sigmoid'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = ['accuracy']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVC(), tuned_parameters, cv=5,
                       scoring=score)
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

count0 = 0.0
count1 = 0.0
for y in y_test:
    if y == 0.0:
        count0 += 1.0
    else:
        count1 += 1.0
print('Count of real 0s = ' + str(count0))
print('Count of real 1s = ' + str(count1))
print('Real ratio 0s/1s = ' + str(count0/count1))
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
print('Pred ratio 0s/1s = ' + str(count0/count1))