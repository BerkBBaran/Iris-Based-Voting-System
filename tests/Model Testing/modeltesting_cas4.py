import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
from sklearn.metrics import roc_curve, auc


def read_similarity(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    data = []
    for line in lines:
        match = re.search(r'(casia4_images.*.jpg) and (casia4_images.*.jpg): (\d+\.\d+)', line)
        if match:
            file1, file2 = match.group(1), match.group(2)
            similarity = float(match.group(3))
            data.append([file1, file2, similarity])

    df = pd.DataFrame(data, columns=['file1', 'file2', 'similarity'])
    return df

# Read similarity data from the text file
df = read_similarity('casia4_results.txt')

# Add 'same_person' column with binary values indicating whether files belong to the same person
# Modify this part according to your data and criteria for determining 'same_person'
df['same_person'] = df['file1'].str.split('\\', expand=True)[1] == df['file2'].str.split('\\', expand=True)[1]


def calculate_FAR_FRR(df, similarity_col, same_person_col, threshold):
    genuine_scores = df[df[same_person_col] == True][similarity_col].values
    impostor_scores = df[df[same_person_col] == False][similarity_col].values

    genuine_accept = sum(score >= threshold for score in genuine_scores)
    impostor_accept = sum(score >= threshold for score in impostor_scores)

    FAR = impostor_accept / len(impostor_scores)
    FRR = 1 - (genuine_accept / len(genuine_scores))

    return FAR, FRR


# Read similarity data from the text file
df = read_similarity('casia4_results.txt')

# Add 'same_person' column with binary values indicating whether files belong to the same person
# Modify this part according to your data and criteria for determining 'same_person'
df['same_person'] = df['file1'].str.split('\\', expand=True)[1] == df['file2'].str.split('\\', expand=True)[1]

# Specify the threshold
thresholds = np.arange(0.4, 0.71, 0.01)
FAR_values = []
FRR_values = []

for threshold in thresholds:
    FAR, FRR = calculate_FAR_FRR(df, 'similarity', 'same_person', threshold)
    FAR_values.append(FAR)
    FRR_values.append(FRR)
    print("At threshold", threshold, "FAR =", FAR, "FRR =", FRR)

# Find the threshold at the intersection point
intersection_index = np.argmin(np.abs(np.array(FAR_values) - np.array(FRR_values)))
intersection_threshold = thresholds[intersection_index]
intersection_threshold = round(intersection_threshold, 2)
print("Intersection threshold:", intersection_threshold)

plt.scatter(intersection_threshold, FAR_values[intersection_index], color='blue', label='Intersection Point')
plt.scatter(intersection_threshold, FRR_values[intersection_index], color='blue')


#optimal threshold for our database
optimal_threshold = thresholds[FAR_values.index(min(FAR_values) + min(FRR_values))]
optimal_threshold = round(optimal_threshold, 2)
print("Optimal threshold:", optimal_threshold)
optimal_FAR = np.min(FAR_values)
optimal_FRR = np.min(FRR_values)

plt.scatter(optimal_threshold, optimal_FAR, color='red', label='Optimal Threshold')
plt.scatter(optimal_threshold, optimal_FRR, color='red')

plt.plot(thresholds, FAR_values, label='FAR')
plt.plot(thresholds, FRR_values, label='FRR')
plt.xlabel('Threshold')
plt.ylabel('Error Rate')
plt.title('FAR and FRR vs. Threshold')
plt.legend()
plt.show()


