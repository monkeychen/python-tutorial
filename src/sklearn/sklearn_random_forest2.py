from sklearn.ensemble import RandomForestClassifier
import csv
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


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


print("features.len = ", len(features))
print("targets.len = ", len(targets), sum(targets))

feature_train, feature_test, flag_train, flag_test = train_test_split(features, targets, test_size=0.4, random_state=10)
clf = RandomForestClassifier(n_estimators=100, n_jobs=-1, min_samples_leaf=2, random_state=5)
# clf = RandomForestClassifier(random_state=5)

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
