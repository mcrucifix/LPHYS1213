# psi_filaments.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import map_coordinates

# ---- paramètres du domaine ----
xmin, xmax = -1.5, 1.5
ymin, ymax = -1.5, 1.5
nx, ny = 400, 400
x = np.linspace(xmin, xmax, nx)
y = np.linspace(ymin, ymax, ny)
X, Y = np.meshgrid(x, y)

# ---- paramètres du champ de courant ----
S = 1.0  # cisaillement (contrôle l'étirement)
# tourbillons localisés : (x_k, y_k, Gamma_k, sigma_k)
vortices = [
    ( -0.6,  0.2,  2.0, 0.15),
    (  0.5, -0.3, -1.5, 0.18),
    (  0.2,  0.9,  1.0, 0.10),
]
A_hf = 0.2  # amplitude des hautes fréquences
phi_x, phi_y = 0.4, -0.7
phi_x2, phi_y2 = 1.0, 0.3

# ---- définition de psi ----
Psi = 0.5 * S * Y**2
for xk, yk, Gk, sig in vortices:
    r2 = (X - xk)**2 + (Y - yk)**2
    Psi += Gk * np.exp(-r2 / (2.0 * sig**2))

Psi += A_hf * (np.sin(4*np.pi*X + phi_x) * np.sin(2*np.pi*Y + phi_y)
               + 0.5 * np.sin(6*np.pi*X + phi_x2) * np.sin(4*np.pi*Y + phi_y2))

# ---- vitesse (u,v) from psi: u = dPsi/dy, v = -dPsi/dx ----
dy = y[1] - y[0]
dx = x[1] - x[0]
# central differences (interior); numpy.gradient is convenient
dPsi_dy, dPsi_dx = np.gradient(Psi, dy, dx)  # returns [d/dy, d/dx]
u = dPsi_dy
v = -dPsi_dx

# ---- affichage : contours de psi + champs de vitesse ----
plt.figure(figsize=(8, 6))
levels = np.linspace(np.min(Psi), np.max(Psi), 40)
cs = plt.contour(X, Y, Psi, levels=levels, linewidths=0.7)
plt.clabel(cs, inline=True, fontsize=7)
# quiver décimé pour lisibilité
skip = (slice(None, None, 18), slice(None, None, 18))
plt.quiver(X[skip], Y[skip], u[skip], v[skip], scale=15)
plt.title(r'$\Psi(x,y)$ avec cisaillement + tourbillons + petites perturbations')
plt.xlabel('x'); plt.ylabel('y'); plt.axis('equal')
plt.xlim(xmin, xmax); plt.ylim(ymin, ymax)
plt.tight_layout()
plt.show()

# ---- optionnel : advection d'un patch scalaire (simple semi-lagrangien) ----
# champ scalaire initial : un patch circulaire
xc0, yc0 = -0.8, 0.6
r0 = 0.18
theta0 = np.exp(-((X-xc0)**2 + (Y-yc0)**2) / (2*(r0**2)))
theta = theta0.copy()

# grille pour l'interpolation (indices)
iy = np.arange(ny)
ix = np.arange(nx)

# helper: sample field 'f' at float positions (xpos, ypos) via map_coordinates on array indices
def sample_field(f, xpos, ypos):
    # convert physical coords to array indices: xpos -> ix_f = (xpos - xmin)/dx
    ix_f = (xpos - xmin) / dx
    iy_f = (ypos - ymin) / dy
    # map_coordinates expects array with axis 0 = y, axis1 = x (same as f)
    coords = np.vstack([iy_f.ravel(), ix_f.ravel()])
    vals = map_coordinates(f, coords, order=1, mode='reflect')
    return vals.reshape(xpos.shape)

# time-stepping parameters
dt = 0.005
nsteps = 600  # ajuster : plus grand -> filaments plus fins
plot_every = 150

# semi-lagrange: backtrace by one step with RK2 (cheap and stable enough here)
for n in range(1, nsteps+1):
    # compute positions of grid points
    Xpos = X.copy()
    Ypos = Y.copy()
    # velocity at grid points
    u_g = u
    v_g = v

    # backtrace (RK2)
    # first estimate: vel at grid
    x_mid = Xpos - 0.5*dt*u_g
    y_mid = Ypos - 0.5*dt*v_g
    u_mid = sample_field(u, x_mid, y_mid)
    v_mid = sample_field(v, x_mid, y_mid)
    x_back = Xpos - dt * u_mid
    y_back = Ypos - dt * v_mid

    # new theta is old theta sampled at backtraced positions
    theta = sample_field(theta, x_back, y_back)

    if (n % plot_every) == 0 or n == 1:
        plt.figure(figsize=(6,5))
        plt.contourf(X, Y, theta, levels=50)
        plt.title(f'Theta advected, step {n}/{nsteps}')
        plt.xlabel('x'); plt.ylabel('y'); plt.axis('equal')
        plt.xlim(xmin, xmax); plt.ylim(ymin, ymax)
        plt.colorbar(label='theta')
        plt.tight_layout()
        plt.show()

# Fin du script

