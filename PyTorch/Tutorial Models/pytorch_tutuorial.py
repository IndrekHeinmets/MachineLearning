import torch
import numpy as np

# ############ Move Operations to Cuda GPU ##################
# if torch.cuda.is_available():
#     device = torch.device("cuda")
#     #--------------------------------
#     x = torch.ones(5, device=device)
#     #---------------OR---------------
#     y = torch.ones(5)
#     y = y.to(device)
#     #--------------------------------
#     z = x + y  # Operation on GPU
#
#     z = z.to("cpu")  # Transfer back to CPU
#     z.numpy()
# ################################################

############### AutoGrad for Back Propegation ###############
# x = torch.randn(3, requires_grad=True)
# print(x)

# y = x + 2
# z = y * y * 2

# v = torch.tensor([0.1, 1.0, 0.001], dtype=torch.float32)
# z.backward(v) # dz/dx
# print(x.grad)
#################################################

############### Turn Off AutoGrad ###############
# x = torch.randn(3, requires_grad=True)
# print(x)
#--------------------------------
# x.requires_grad_(False)
# print(x)
#--------------------------------
# y = x.detach()
# print(y)
#--------------------------------
# with torch.no_grad():
#     y = x + 2
#     print(y)
#--------------------------------

# weights = torch.ones(4, requires_grad=True)

# for epoch in range(3):
#     model_out = (weights * 3).sum()

#     model_out.backward()
#     print(weights.grad)

#     weights.grad.zero_()
#     print(weights.grad)
#################################################


############### Back Propegation ###############
# x = torch.tensor(1.0)
# y = torch.tensor(2.0)

# w = torch.tensor(1.0, requires_grad=True)

# # Forward Pass:
# y_hat = w * x
# loss = (y_hat - y) ** 2
# print(loss)

# # Backward Pass:
# loss.backward()
# print(w.grad)

# ### Update weights, new forward/backward
#################################################

############### NumPy Gradients ###############
# # f = w * x -> f = 2 * x
# X = np.array([1, 2, 3, 4], dtype=np.float32)
# Y = np.array([2, 4, 6, 8], dtype=np.float32)

# w = 0.0

# # Model Prediction:


# def forward(x):
#     return w * x

# # Loss = MSE:


# def loss(y, y_pred):
#     return ((y_pred - y) ** 2).mean()

# # Gradient:


# def gradient(x, y, y_pred):
#     return np.dot(2 * x, y_pred - y).mean()


# print(f"Prediction before training: f(5) = {forward(5):.3f}")

# # Training:
# learning_rate = 0.01
# n_iters = 50

# for epoch in range(n_iters):
#     # Prediction = forward pass
#     y_pred = forward(X)

#     # Loss
#     l = loss(Y, y_pred)

#     # Gradients
#     dw = gradient(X, Y, y_pred)

#     # Update Weights
#     w -= learning_rate * dw

#     if epoch % 2 == 0:
#         print(f"Epoch {epoch + 1}: w = {w:.3f}, loss = {l:.8f}")

# print(f"Prediction after training: f(5) = {forward(5):.3f}")
# #################################################
