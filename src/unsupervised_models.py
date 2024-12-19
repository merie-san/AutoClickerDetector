import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import matthews_corrcoef
from scipy.stats import mode


def preprocess_label(label_list):
    processed_labels = []
    for label in label_list:
        if label:
            processed_labels.append(1)
        else:
            processed_labels.append(0)
    return processed_labels


def match_clusters_to_labels(cluster_labels, true_labels):
    is0_list = cluster_labels == 0
    count0 = np.sum(true_labels[is0_list] == 1) + np.sum(true_labels[~is0_list] == 0)
    count1 = np.sum(true_labels[is0_list] == 0) + np.sum(true_labels[~is0_list] == 1)
    if count0 > count1:
        return is0_list, count0
    else:
        return ~is0_list, count1


data_frame = pd.read_csv("training_batch.csv")
labels = data_frame["abnormal activity"]
samples = data_frame.drop(["abnormal activity"], axis=1)
array_labels = labels.to_numpy()
array_samples = samples.to_numpy()
scaler = StandardScaler()
array_samples = scaler.fit_transform(array_samples)
sample_train, sample_test, label_train, label_test = train_test_split(array_samples, array_labels, test_size=0.33, random_state=42)

pca_model = PCA(n_components=11)
pca_model.fit(sample_train)
sample_train = pca_model.transform(sample_train)
sample_test = pca_model.transform(sample_test)

k_means_cls = KMeans(n_clusters=2)
k_means_cls.fit(sample_train)
# Align labels
aligned_train_labels, train_matches = match_clusters_to_labels(k_means_cls.labels_, label_train)
aligned_test_labels, test_matches = match_clusters_to_labels(k_means_cls.predict(sample_test), label_test)

# Compute metrics
train_accuracy = train_matches / len(label_train)
test_accuracy = test_matches / len(label_test)

train_mcc = matthews_corrcoef(label_train, aligned_train_labels)
test_mcc = matthews_corrcoef(label_test, aligned_test_labels)

print("train dataset accuracy " + str(train_accuracy))
print("test dataset accuracy " + str(test_accuracy))
print("train dataset MCC " + str(train_mcc))
print("test dataset MCC " + str(test_mcc))
