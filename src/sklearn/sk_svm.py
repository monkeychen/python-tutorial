import csv
import joblib
from sklearn.model_selection import train_test_split
import sklearn.metrics as sm
from sklearn import svm
import numpy as np
import matplotlib.pyplot as mp


def to_float(x):
    try:
        return float(x)
    except ValueError:
        # print(x)
        return 0


features = []
targets = []
feature_names = []
with open('data_set_fields.csv') as name_file:
    column_name_file = csv.reader(name_file)
    feature_names = next(column_name_file)[1:-1]

with open('cza_satisfaction_data_set.csv') as data_file:
    csv_file = csv.reader(data_file)
    for content in csv_file:
        content = content[:1] + list(map(to_float, content[1:]))
        if len(content) != 0:
            features.append(content[1:-2])
            targets.append(content[-1])

features = np.array(features)
targets = np.array(targets)
print("features.len = ", len(features))
print("targets.len = ", len(targets), sum(targets))

feature_train, feature_test, flag_train, flag_test = train_test_split(features, targets, test_size=0.4, random_state=10)
clf = svm.SVC(kernel='rbf', C=600)
clf.fit(feature_train, flag_train)
print("=============")
print(clf.get_params())

predict_result = clf.predict(feature_test)
print(sm.classification_report(flag_test, predict_result))

# # 绘制分类边界线
# l, r = features[:, 0].min() - 1, features[:, 0].max() + 1
# b, t = features[:, 1].min() - 1, features[:, 1].max() + 1
# n = 500
# grid_x, grid_y = np.meshgrid(np.linspace(l, r, n), np.linspace(b, t, n))
# bg_x = np.column_stack((grid_x.ravel(), grid_y.ravel()))
# bg_y = clf.predict(bg_x)
# grid_z = bg_y.reshape(grid_x.shape)
#
# # 画图显示样本数据
# mp.figure('SVM Classification', facecolor='lightgray')
# mp.title('SVM Classification', fontsize=16)
# mp.xlabel('X', fontsize=14)
# mp.ylabel('Y', fontsize=14)
# mp.tick_params(labelsize=10)
# mp.pcolormesh(grid_x, grid_y, grid_z, cmap='gray')
# mp.scatter(feature_test[:, 0], feature_test[:, 1], s=80, c=flag_test, cmap='jet', label='Samples')
#
# mp.legend()
# mp.show()
