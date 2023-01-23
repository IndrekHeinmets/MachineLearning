import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def score_model(X, y, kf):
    accuracy_scores, precision_scores, recall_scores, f1_scores, roc_auc_scores = [], [], [], [], []

    for train_i, test_i in kf.split(X):
        X_train, X_test = X[train_i], X[test_i]
        y_train, y_test = y[train_i], y[test_i]

        # Building the model:
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Running the model:
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)

        # Evaluating the model:
        accuracy_scores.append(accuracy_score(y_test, y_pred))
        precision_scores.append(precision_score(y_test, y_pred))
        recall_scores.append(recall_score(y_test, y_pred))
        f1_scores.append(f1_score(y_test, y_pred))
        roc_auc_scores.append(roc_auc_score(y_test, y_pred_proba[:, 1]))

    print(f'  Accuracy: {np.mean(accuracy_scores)}')
    print(f' Precision: {np.mean(precision_scores)}')
    print(f'    Recall: {np.mean(recall_scores)}')
    print(f'  F1 Score: {np.mean(f1_scores)}')
    print(f'   ROC AUC: {np.mean(recall_scores)}')


# Read/modify data into DataFrame:
df = pd.read_csv('Datasets\\Titanic.csv')
df['male'] = df['Sex'] == 'male'

# Add k-fold cross validation:
kf = KFold(n_splits=5, shuffle=True)

# Setup feature options and targets:
X1 = df[['Pclass', 'male', 'Age', 'Siblings/Spouses', 'Parents/Children', 'Fare']].values
X2 = df[['Pclass', 'male', 'Age']].values
X3 = df[['Age', 'Fare']].values
y = df['Survived'].values

print("Logistic Regression with all features:")
score_model(X1, y, kf)
print()
print("Logistic Regression with Pclass, Sex & Age features:")
score_model(X2, y, kf)
print()
print("Logistic Regression with Age & Fare features:")
score_model(X3, y, kf)
print()

# Choose/build the best model:
final_model = LogisticRegression()
final_model.fit(X1, y)

# Running the final model:
x_test = [3, False, 25, 0, 1, 2]
print(f'Prediction: {final_model.predict([x_test])[0]}')
