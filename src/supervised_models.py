from sklearn.ensemble import *
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier
import pickle
import os.path
from sklearn.metrics import matthews_corrcoef
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np

data_frame = pd.read_csv("training_batch.csv")
labels = data_frame["abnormal activity"]
samples = data_frame.drop(["abnormal activity"], axis=1)
array_labels = labels.to_numpy()
array_samples = samples.to_numpy()
scores = []
sample_train, sample_test, label_train, label_test = train_test_split(array_samples, array_labels, test_size=0.33, random_state=42)

if not os.path.exists("scaler.pkl"):
    scaler = StandardScaler()
    scaler.fit(sample_train)
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
else:
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

sample_train = scaler.transform(sample_train)
sample_test = scaler.transform(sample_test)

if not os.path.exists("random_forest_cls.pkl"):
    random_forest_cls = RandomForestClassifier(n_estimators=50)
    random_forest_cls.fit(sample_train, label_train)
    with open("random_forest_cls.pkl", "wb") as f:
        pickle.dump(random_forest_cls, f)
else:
    with open("random_forest_cls.pkl", "rb") as f:
        random_forest_cls = pickle.load(f)

if not os.path.exists("ada_boost_cls.pkl"):
    ada_boost_cls = AdaBoostClassifier(n_estimators=15)
    ada_boost_cls.fit(sample_train, label_train)
    with open("ada_boost_cls.pkl", "wb") as g:
        pickle.dump(ada_boost_cls, g)
else:
    with open("ada_boost_cls.pkl", "rb") as g:
        ada_boost_cls = pickle.load(g)

if not os.path.exists("mlp_cls.pkl"):
    mlp_classifier = MLPClassifier(hidden_layer_sizes=[30,10], learning_rate="adaptive", max_iter=2000)
    mlp_classifier.fit(sample_train, label_train)
    with open("mlp_cls.pkl", "wb") as h:
        pickle.dump(mlp_classifier, h)
else:
    with open("mlp_cls.pkl", "rb") as h:
        mlp_classifier = pickle.load(h)

if not os.path.exists("log_regr_cls.pkl"):
    log_regr_cls = LogisticRegression(solver="newton-cholesky", C=1.1)
    log_regr_cls.fit(sample_train, label_train)
    with open("log_regr_cls.pkl", "wb") as i:
        pickle.dump(log_regr_cls, i)
else:
    with open("log_regr_cls.pkl", "rb") as i:
        log_regr_cls = pickle.load(i)

if not os.path.exists("spv_cls.pkl"):
    spv_cls = SVC(kernel="linear", C=1.1)
    spv_cls.fit(sample_train, label_train)
    with open("spv_cls.pkl", "wb") as j:
        pickle.dump(spv_cls, j)
else:
    with open("spv_cls.pkl", "rb") as j:
        spv_cls = pickle.load(j)

predicted_labels_rand_forest = random_forest_cls.predict(sample_test)
predicted_labels_ada_boost = ada_boost_cls.predict(sample_test)
predicted_labels_mlp = mlp_classifier.predict(sample_test)
predicted_labels_log_regr = log_regr_cls.predict(sample_test)
predicted_labels_spv = spv_cls.predict(sample_test)

scores_rand_forest = cross_val_score(random_forest_cls, sample_train, label_train, scoring="accuracy")
scores_ada_boost = cross_val_score(ada_boost_cls, sample_train, label_train, scoring="accuracy")
scores_mlp = cross_val_score(mlp_classifier, sample_train, label_train, scoring="accuracy")
scores_log_regr = cross_val_score(log_regr_cls, sample_train, label_train, scoring="accuracy")
scores_spv = cross_val_score(spv_cls, sample_train, label_train, scoring="accuracy")

scores.append({"name": "Random Forest",
               "MCC": float(matthews_corrcoef(label_test, predicted_labels_rand_forest)),
               "cross-validated mean accuracy": float(scores_rand_forest.mean()),
               "std of cross-validated accuracy": float(scores_rand_forest.std()),
               "test accuracy": float(random_forest_cls.score(sample_test, label_test))})
scores.append({"name": "ADA Boost",
               "MCC": float(matthews_corrcoef(label_test, predicted_labels_ada_boost)),
               "cross-validated mean accuracy": float(scores_ada_boost.mean()),
               "std of cross-validated accuracy": float(scores_ada_boost.std()),
               "test accuracy": float(ada_boost_cls.score(sample_test, label_test))})
scores.append({"name": "MultiLayer Perceptron",
               "MCC": float(matthews_corrcoef(label_test, predicted_labels_mlp)),
               "cross-validated mean accuracy": float(scores_mlp.mean()),
               "std of cross-validated accuracy": float(scores_mlp.std()),
               "test accuracy": float(mlp_classifier.score(sample_test, label_test))})
scores.append({"name": "Logistic Regression",
               "MCC": float(matthews_corrcoef(label_test, predicted_labels_log_regr)),
               "cross-validated mean accuracy": float(scores_log_regr.mean()),
               "std of cross-validated accuracy": float(scores_log_regr.std()),
               "test accuracy": float(log_regr_cls.score(sample_test, label_test))})
scores.append({"name": "Support Vector Machine",
               "MCC": float(matthews_corrcoef(label_test, predicted_labels_spv)),
               "cross-validated mean accuracy": float(scores_spv.mean()),
               "std of cross-validated accuracy": float(scores_spv.std()),
               "test accuracy": float(spv_cls.score(sample_test, label_test))})

for dict_e in scores:
    print(dict_e)
