import numpy as np
import matplotlib.pyplot as plt

# Domaine
x = np.linspace(-1.5, 1.5, 400)
y = np.linspace(-1.5, 1.5, 400)
X, Y = np.meshgrid(x, y)

# Champ psi
psi = np.cos(2 * np.pi * X) * np.sin(2 * np.pi * Y)

# Visualisation
plt.figure(figsize=(6, 5))
contours = plt.contour(X, Y, psi, levels=20)  # 20 niveaux de contours
plt.clabel(contours, inline=True, fontsize=8)  # Étiquettes sur les courbes
plt.title(r"$\psi(x,y) = \cos(2\pi x)\sin(2\pi y)$")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")  # Respect des proportions
plt.show()

