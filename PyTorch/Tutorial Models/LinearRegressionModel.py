
# 1. Design model (input, output size, forward pass)
# 2. Construct loss and optimizer
# 3. Training loop:
#   - Forward pass > Compute Predictions
#   - Backward pass > Gradients
#   - Update Weights

import torch
import torch.nn as nn
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt

# Preapare Data:
X_numpy, y_numpy = datasets.make_regression(n_samples=100, n_features=1, noise=20, random_state=1)

X = torch.from_numpy(X_numpy.astype(np.float32))
y = torch.from_numpy(y_numpy.astype(np.float32))
y = y.view(y.shape[0], 1)

n_samples, n_features = X.shape

# Model:
input_size = n_features
output_size = 1
model = nn.Linear(input_size, output_size)

# Loass & Optimizer:
learning_rate = 0.01
crit = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# Training Loop:
num_epochs = 1000
for epoch in range(num_epochs):
    # Forward & Loss:
    y_pred = model(X)
    loss = crit(y_pred, y)
    # Backward:
    loss.backward()
    # Update:
    optimizer.step()
    optimizer.zero_grad()

    if epoch % 10 == 0:
        print(f"Epoch: {epoch + 1}, loss = {loss.item():.4f}")

# Plot:
predicted = model(X).detach().numpy()
plt.plot(X_numpy, y_numpy, "ro")
plt.plot(X_numpy, predicted, "b")
plt.show()
