import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Read data into DataFrame:
data = load_breast_cancer()
df = pd.DataFrame(data['data'], columns=data['feature_names'])
df['target'] = data['target']

# Setup features and targets:
X = df[data.feature_names].values
y = df['target'].values

# Find optimal tree count:
n_estimators = list(range(1, 101))
param_grid = {
    'n_estimators': n_estimators,
}
model = RandomForestClassifier()
gs = GridSearchCV(model, param_grid, cv=5)
gs.fit(X, y)
scores = gs.cv_results_['mean_test_score']
plt.plot(n_estimators, scores)
plt.xlabel('n_estimators')
plt.ylabel('accuracy')
plt.xlim(0, 100)
plt.ylim(0.9, 1)
plt.show()

# Choose/build the best model:
final_model = RandomForestClassifier(n_estimators=10)
final_model.fit(X, y)

# Running the final model:
x_test = X[0]
print(f'Prediction: {final_model.predict([x_test])[0]}')
