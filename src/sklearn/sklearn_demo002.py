from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()
X = iris.data
y = iris.target

iris_model = LinearRegression()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3.0, random_state=7)

iris_model.fit(X_train, y_train)

print("-----------模型参数----------------")
print(iris_model.get_params())
print("-----------模型在训练集上的得分--------------")
print(iris_model.score(X_train, y_train))
print("-----------模型在测试集上的得分--------------")
print(iris_model.score(X_test, y_test))

print("-----------预测-----------------")
y_pred = iris_model.predict(X_test)
print("预测标签：", y_pred[:3])
print("真实标签：", y_test[:3])

import _pickle as cPickle

print("dump to pkl file")
with open('LR_model.pkl', 'wb') as f:
    cPickle.dump(iris_model, f)
print("loading from pkl file...")
with open('LR_model.pkl', 'rb') as f:
    model = cPickle.load(f)
    print(model.predict(X_test)[:3])


