# -*- coding: utf-8 -*-
"""Credit Scoring Model .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JQFjSgjGhNyBN-7_eHudb8Dx4s27yCTS
"""

import pandas as pd

# Load dataset
df = pd.read_csv("/content/credit_score.csv")

# Drop ID column
df.drop("CUST_ID", axis=1, inplace=True)

# Check for nulls
df = df.dropna()  # or use df.fillna(df.median(), inplace=True)

X = df.drop("DEFAULT", axis=1)
y = df["DEFAULT"]

# Get dummies for categorical columns
X = pd.get_dummies(X, drop_first=True)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Logistic Regression
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Logistic Regression
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Logistic Regression
print("Logistic Regression")
print(confusion_matrix(y_test, lr.predict(X_test)))
print(classification_report(y_test, lr.predict(X_test)))
print("ROC AUC:", roc_auc_score(y_test, lr.predict_proba(X_test)[:, 1]))

# Random Forest
print("\nRandom Forest")
print(confusion_matrix(y_test, rf.predict(X_test)))
print(classification_report(y_test, rf.predict(X_test)))
print("ROC AUC:", roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1]))

import matplotlib.pyplot as plt
import seaborn as sns

feature_importances = rf.feature_importances_
features = X.columns

# Plot top 20 important features
top_n = 20
sorted_idx = feature_importances.argsort()[::-1][:top_n]

plt.figure(figsize=(10,6))
sns.barplot(x=feature_importances[sorted_idx], y=features[sorted_idx])
plt.title("Top 20 Feature Importances (Random Forest)")
plt.show()

from sklearn.metrics import roc_curve

fpr, tpr, _ = roc_curve(y_test, rf.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label="Random Forest")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.grid()
plt.show()

from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

print("Decision Tree")
print(classification_report(y_test, dt.predict(X_test)))
print("ROC AUC:", roc_auc_score(y_test, dt.predict_proba(X_test)[:, 1]))

from sklearn.model_selection import GridSearchCV

param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [5, 10, None]}
grid = GridSearchCV(RandomForestClassifier(), param_grid, cv=3, scoring='roc_auc')
grid.fit(X_train, y_train)
print("Best parameters:", grid.best_params_)

import joblib
joblib.dump(rf, "credit_model.pkl")