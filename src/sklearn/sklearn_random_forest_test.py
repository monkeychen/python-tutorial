import csv
import joblib
from sklearn.metrics import accuracy_score

data = []
features = []
targets = []
feature_names = []
users = []
with open('satisfaction_feature_names.csv') as name_file:
    column_name_file = csv.reader(name_file)
    feature_names = next(column_name_file)[2:394]

with open('cza_satisfaction_train_0922.csv') as data_file:
    csv_file = csv.reader(data_file)
    idx = 0
    for content in csv_file:
        idx = idx + 1
        if idx <= 10000:
            continue

        if idx > 50000:
            break
        content = content[:2] + list(map(float, content[2:]))
        if len(content) != 0:
            data.append(content)
            features.append(content[2:394])
            targets.append(content[-1])
            users.append(content[1])

clf, sorted_feature_scores = joblib.load("cza_rf.pkl")
predict_result = clf.predict(features)
print(sorted_feature_scores)
print(accuracy_score(predict_result, targets))
result = list(zip(users, predict_result))
print(result[:10])
print(sum(predict_result))
print(sum([flag[1] for flag in result]))
with open("rf_predict_result.csv", "w", encoding="UTF-8") as w_file:
    result_file = csv.writer(w_file)
    for idx, row in enumerate(result):
        if idx > 10:
            break
        row = list(row)
        row.insert(0, 20200928)
        result_file.writerow(row)



