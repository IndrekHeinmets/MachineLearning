import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV


def score_model(X, y):
    # Compare impurity algorithms:
    for crit in ['gini', 'entropy']:
        # Compare pruning parameters with k-fold cross validation:
        param_grid = {'max_depth': [3, 15, 25, 50],
                      'max_leaf_nodes': [10, 20, 35, 50, 100],
                      'min_samples_leaf': [1, 2, 3]}

        model = DecisionTreeClassifier(criterion=crit)
        gs = GridSearchCV(model, param_grid, scoring='f1', cv=5)
        gs.fit(X, y)
        print(f'Decision Tree - {crit}')
        print(f'Best score: {gs.best_score_}')
        print(f'Best params: {gs.best_params_}\n')


# Read/modify data into DataFrame:
df = pd.read_csv('Datasets\\Titanic.csv')
df['male'] = df['Sex'] == 'male'

# Setup feature options and targets:
X1 = df[['Pclass', 'male', 'Age', 'Siblings/Spouses', 'Parents/Children', 'Fare']].values
X2 = df[['Pclass', 'male', 'Age']].values
X3 = df[['Age', 'Fare']].values
y = df['Survived'].values

print('Logistic Regression with all features:')
score_model(X1, y)
print()
print('Logistic Regression with Pclass, Sex & Age features:')
score_model(X2, y)
print()
print('Logistic Regression with Age & Fare features:')
score_model(X3, y)
print()

# Choose/build the best model, with the best feature matrix, criterion and pruning parameters:
final_model = DecisionTreeClassifier(criterion='gini', max_depth=25, max_leaf_nodes=35, min_samples_leaf=1)
final_model.fit(X1, y)

# Running the final model:
x_test = [3, False, 25, 0, 1, 2]
print(f'Prediction: {final_model.predict([x_test])[0]}')
