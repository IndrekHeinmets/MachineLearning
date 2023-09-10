
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
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Preapare Data:
bc = datasets.load_breast_cancer()
X, y = bc.data, bc.target

n_samples, n_features = X.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

# Scale:
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

X_train = torch.from_numpy(X_train.astype(np.float32))
X_test = torch.from_numpy(X_test.astype(np.float32))
y_train = torch.from_numpy(y_train.astype(np.float32))
y_test = torch.from_numpy(y_test.astype(np.float32))

y_train = y_train.view(y_train.shape[0], 1)
y_test = y_test.view(y_test.shape[0], 1)

# Model [ f = wx + b, sigmoid at the end ]:


class LogisticRegression(nn.Module):

    def __init__(self, n_input, n_input_features):
        super(LogisticRegression, self).___init__()
        self.linear = nn.Linear(n_input_features, 1)

    def forward(self, x):
        y_pred = torch.sigmoid(self.linear(x))
        return y_pred


model = LogisticRegression(n_features)


# Loass & Optimizer:
learning_rate = 0.01
crit = nn.BCELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# Training Loop:
num_epochs = 100
for epoch in range(num_epochs):

    # Forward & Loss:
    y_pred = model(X_train)
    loss = crit(y_pred, y_train)

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
