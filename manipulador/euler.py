import numpy as np

# Ángulos de Euler en grados

alpha, beta, gamma = 3.14, 0, 0

alpha = np.radians(alpha)
beta = np.radians(beta)
gamma = np.radians(gamma)

# Matrices de rotación individuales
R_X = np.array([
    [1, 0, 0],
    [0, np.cos(alpha), -np.sin(alpha)],
    [0, np.sin(alpha), np.cos(alpha)]
])

R_Y = np.array([
    [np.cos(beta), 0, np.sin(beta)],
    [0, 1, 0],
    [-np.sin(beta), 0, np.cos(beta)]
])

R_Z = np.array([
    [np.cos(gamma), -np.sin(gamma), 0],
    [np.sin(gamma), np.cos(gamma), 0],
    [0, 0, 1]
])

# Matriz de rotación compuesta
R = np.dot(R_Z, np.dot(R_Y, R_X))

# Ángulo de rotación (theta)
theta = np.arccos((np.trace(R) - 1) / 2)

# Componentes del eje de rotación
sin_theta = np.sin(theta)
if sin_theta != 0:
    vx = (R[2, 1] - R[1, 2]) / (2 * sin_theta)
    vy = (R[0, 2] - R[2, 0]) / (2 * sin_theta)
    vz = (R[1, 0] - R[0, 1]) / (2 * sin_theta)
else:
    # Para theta = 0, elegir un vector unitario arbitrario
    vx, vy, vz = 1, 0, 0

# Normalizar el vector
axis = np.array([vx, vy, vz])
axis = axis / np.linalg.norm(axis)

# Mostrar el resultado
theta_degrees = np.degrees(theta)
print(axis, theta_degrees)
