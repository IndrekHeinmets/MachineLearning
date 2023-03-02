import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Load MNIST database of handwritten digits: [8 * 8 images]
X, y = load_digits(return_X_y=True)

# Setup features and targets:
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Choose/Build model: Solvers['lbfgs', 'sgd', 'adam']
model = MLPClassifier(max_iter=500, hidden_layer_sizes=(100, 50), alpha=1e-4, solver='sgd')
model.fit(X_train, y_train)

# Running the final model:
test_i = 0
print(f'Prediction: {model.predict([X_test[test_i]])[0]}')
print(f'Confidence: {round(model.score(X_test, y_test) * 100, 2)}%')
print(f'Correct answer: {y_test[test_i]}')

# Visualize input data: Grayscale[0-White, 16-Black]
plt.matshow(X_test[test_i].reshape(8, 8), cmap=plt.cm.gray)
plt.xticks(())
plt.yticks(())
plt.show()
