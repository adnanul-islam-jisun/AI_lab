
import math
import csv
import random
import pandas as pd
import heapq

dataset_file = "/content/dataset.csv"

min_marks = {
    "Assignment-1": 100,
    "Assignment-2": 100,
    "Assignment-3": 100,
    "Assignment-4": 100,
    "Assignment-5": 100,
    "Final": 100,
    "Mid": 100,
}

max_marks = {
    "Assignment-1": -100,
    "Assignment-2": -100,
    "Assignment-3": -100,
    "Assignment-4": -100,
    "Assignment-5": -100,
    "Final": -100,
    "Mid": -100,
}

df = pd.read_csv(dataset_file)

def load_min_max(df):
    for k in min_marks:
        min_marks[k] = min(df.loc[:, k])
        max_marks[k] = max(df.loc[:, k])

load_min_max(df)

def get_normalized_entry(row):
    result = []
    result.append((row[0] - min_marks["Assignment-1"]) / (max_marks["Assignment-1"] - min_marks["Assignment-1"]))
    result.append((row[1] - min_marks["Assignment-2"]) / (max_marks["Assignment-2"] - min_marks["Assignment-2"]))
    result.append((row[2] - min_marks["Assignment-3"]) / (max_marks["Assignment-3"] - min_marks["Assignment-3"]))
    result.append((row[3] - min_marks["Assignment-4"]) / (max_marks["Assignment-4"] - min_marks["Assignment-4"]))
    result.append((row[4] - min_marks["Assignment-5"]) / (max_marks["Assignment-5"] - min_marks["Assignment-5"]))
    result.append((row[5] - min_marks["Final"]) / (max_marks["Final"] - min_marks["Final"]))
    result.append((row[6] - min_marks["Mid"]) / (max_marks["Mid"] - min_marks["Mid"]))
    return result

mark_records = []
for row in range(len(df)):
    current_record = list(df.loc[row, :])
    current_record_updated = [current_record[0]]
    current_record_updated.extend(get_normalized_entry(current_record[1: len(current_record) - 1]))
    current_record_updated.append(current_record[-1])
    mark_records.append(current_record_updated)

random.shuffle(mark_records)

train_len = math.floor(len(mark_records) * 0.8)
valid_len = math.floor(len(mark_records) * 0.1)

training = mark_records[:train_len]
validation = mark_records[train_len:train_len + valid_len]
testing = mark_records[train_len + valid_len:]

def euclidean_distance(row1, row2):
    if len(row1) != len(row2):
        return None
    ret_val = 0
    for idx, item in enumerate(row1):
        ret_val += (row1[idx] - row2[idx]) ** 2
    return math.sqrt(ret_val)

def get_accuracy(true_output, predicted_output):
    correct = 0
    for idx, outcome in enumerate(true_output):
        if outcome == predicted_output[idx]:
            correct += 1
    accuracy = (correct / float(len(true_output))) * 100.0
    return accuracy

def predict_section(validation_set, k):
    predictions = []
    for entry in validation_set:
        dist_vector = []
        for compare_entry in training:
            s1 = entry[1:8]
            s2 = compare_entry[1:8]
            dist_vector.append((euclidean_distance(s1, s2), compare_entry[-1]))

        dist_vector.sort(key=lambda x: x[0])

        neighbors = heapq.nlargest(k, dist_vector, key=lambda x: x[0])
        classes = [neighbor[1] for neighbor in neighbors]
        predictions.append(max(set(classes), key=classes.count))

    return predictions

best_k = None
best_accuracy = 0

for k_value in [1, 3, 5, 7]:
    predicted_validation = predict_section(validation, k_value)
    true_out_validation = [entry[-1] for entry in validation]
    acc_validation = get_accuracy(true_out_validation, predicted_validation)

    if acc_validation > best_accuracy:
        best_k = k_value
        best_accuracy = acc_validation

print(f"Best k value for validation set: {best_k}")

predicted_testing = predict_section(testing, best_k)
true_out_testing = [entry[-1] for entry in testing]
acc_testing = get_accuracy(true_out_testing, predicted_testing)

print(f"Testing Accuracy (k={best_k}): {acc_testing}%")

def predict_new_students(new_students_data, k):
    normalized_new_students = []

    for entry in new_students_data:
        normalized_entry = get_normalized_entry(entry)
        normalized_new_students.append([entry[0]] + normalized_entry)

    predictions = predict_section(normalized_new_students, k)

    return predictions

new_students_data = [
    [1271653, 9, 14, 12, 11, 8, 13, 3]  # Replace this with actual input
]

normalized_predictions = predict_new_students(new_students_data, best_k)

for i, prediction in enumerate(normalized_predictions):
    print(f"Student {i + 1} - Predicted Section: {prediction}")