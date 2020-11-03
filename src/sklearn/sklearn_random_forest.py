from sklearn.ensemble import RandomForestClassifier
import csv
import joblib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

data = []
features = []
targets = []
feature_names = []
with open('satisfaction_feature_names.csv') as name_file:
    column_name_file = csv.reader(name_file)
    feature_names = next(column_name_file)[2:394]

with open('cza_satisfaction_train_0922.csv') as data_file:
    csv_file = csv.reader(data_file)
    idx = 0
    for content in csv_file:
        idx = idx + 1
        if idx > 30000:
            break
        content = content[:2] + list(map(float, content[2:]))
        if len(content) != 0:
            # data.append(content)
            features.append(content[2:394])
            targets.append(content[-1])

print("data.len = ", len(data))
print("features.len = ", len(features))
print("targets.len = ", len(targets), sum(targets))

# scaler = StandardScaler()
# scaler.fit(features)
# features = scaler.transform(features)
feature_train, feature_test, flag_train, flag_test = train_test_split(features, targets, test_size=0.3, random_state=10)
# clf = RandomForestClassifier(n_estimators=100, n_jobs=-1, min_samples_leaf=5, random_state=50)
clf = RandomForestClassifier(random_state=5)

# print(clf.get_params())
#
# scores = cross_val_score(clf, feature_train, flag_train, cv=5)
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print(clf.get_params())

clf.fit(feature_train, flag_train)
print("=============")
print(clf.get_params())

important_feature_list = zip(map(lambda a: round(a, 4), clf.feature_importances_), feature_names)
sorted_feature_scores = sorted(important_feature_list, reverse=True)
for item in sorted_feature_scores:
    print(item)
predict_result = clf.predict(feature_test)
print(accuracy_score(predict_result, flag_test))
conf_matrix = confusion_matrix(flag_test, predict_result)
print(conf_matrix)
print(classification_report(flag_test, predict_result))

# joblib.dump([clf, sorted_feature_scores], "cza_rf.pkl")
