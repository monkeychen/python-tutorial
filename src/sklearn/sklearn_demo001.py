import numpy as np
import pandas as pd
import csv
from sklearn.datasets.base import Bunch
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import r2_score
from collections import defaultdict

X = [[0, 15], [1, -10]]
print(StandardScaler().fit(X).transform(X))

iris_data_set = datasets.load_iris()
x = iris_data_set.data
y = iris_data_set.target
print(iris_data_set['feature_names'])
# print(x, y)


def load_my_fancy_dataset():
    with open('ds1.csv') as csv_file:
        data_file = csv.reader(csv_file)
        temp = next(data_file)
        n_samples = int(temp[0])
        n_features = int(temp[1])
        data = np.empty((n_samples, n_features))
        target = np.empty((n_samples,), dtype=np.int)
        feature_names = temp[2:]

        for i, sample in enumerate(data_file):
            data[i] = np.asarray(sample[:-1], dtype=np.float64)
            target[i] = np.asarray(sample[-1], dtype=np.int)

    return Bunch(data=data, target=target, feature_names=feature_names)


def mean_decrease_impurity():
    boston = datasets.load_boston()
    X1 = boston["data"]
    print(type(X1), X1.shape)
    Y1 = boston["target"]
    names = boston["feature_names"]
    print(names)
    rf = RandomForestRegressor()
    rf.fit(X1, Y1)
    print("Features sorted by their score:")
    print(sorted(zip(map(lambda a: round(a, 4), rf.feature_importances_), names), reverse=True))


def mean_decrease_accuracy():
    boston = datasets.load_boston()
    X1 = boston["data"]
    Y1 = boston["target"]
    names = boston["feature_names"]
    rf = RandomForestRegressor()
    scores = defaultdict(list)
    shuff_split = ShuffleSplit(5, test_size=0.3, random_state=100)
    for train_idx, test_idx in shuff_split.split(X1):
        X_train, X_test = X1[train_idx], X1[test_idx]
        Y_train, Y_test = Y1[train_idx], Y1[test_idx]
        r = rf.fit(X_train, Y_train)
        acc = r2_score(Y_test, rf.predict(X_test))
        for i in range(X1.shape[1]):
            print("shuff:%d" % i)
            X_t = X_test.copy()
            np.random.shuffle(X_t[:, i])
            shuff_acc = r2_score(Y_test, rf.predict(X_t))
            scores[names[i]].append((acc - shuff_acc) / acc)

    print("Features sorted by their score:")
    print(sorted([(round(np.mean(score), 4), feat) for feat, score in scores.items()], reverse=True))


def pandas_demo():
    pd_data = pd.read_csv("ds2.csv")
    X1 = pd_data[["first_feat", "second_feat", "third_feat"]]
    Y1 = pd_data["flag"]
    rf = RandomForestRegressor()
    rf.fit(X1, Y1)
    print("特征重要性：", rf.feature_importances_)


if __name__ == '__main__':
    # data1 = load_my_fancy_dataset()
    # print(data1['feature_names'])
    # print(data)
    # mean_decrease_impurity()
    # mean_decrease_accuracy()
    pandas_demo()
