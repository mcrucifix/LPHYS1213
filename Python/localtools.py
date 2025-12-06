import numpy as np
import matplotlib.pyplot as plt

# Parameters
U = 1.0          # free-stream velocity
R = 1.0          # cylinder radius
N = 400          # resolution

# Cartesian grid
x = np.linspace(-3*R, 3*R, N)
y = np.linspace(-3*R, 3*R, N)
X, Y = np.meshgrid(x, y)

# Polar coordinates
r = np.sqrt(X**2 + Y**2)
theta = np.arctan2(Y, X)

# Mask inside the cylinder
mask = (r < R)



def plot_stream_and_potential(ax, Gamma, filename=None, show_ylabel=True):
    """Plot streamfunction (solid) and potential (dashed) for given circulation Gamma,
       with added velocity arrows (quiver plot)."""
    
    # --- 1. Calculate Flow Variables ---
    
    # Streamfunction (for contours)
    psi = U*(r - R**2/r)*np.sin(theta) + Gamma/(2*np.pi)*np.log(r)
    psi = np.ma.array(psi, mask=mask)
    
    # Velocity potential (for contours)
    phi = U*(r + R**2/r)*np.cos(theta) + Gamma/(2*np.pi)*theta
    phi = np.ma.array(phi, mask=mask)
    
    # Radial and Tangential Velocity Components (u_r, u_theta)
    # Note: The stream function used gives -u_theta from the derivative wrt r.
    u_r = U*(1 - R**2/r**2)*np.cos(theta) 
    u_theta = -U*(1 + R**2/r**2)*np.sin(theta) - Gamma/(2*np.pi*r)
    
    # Cartesian Velocity Components (u, v)
    u = u_r * np.cos(theta) - u_theta * np.sin(theta)
    v = u_r * np.sin(theta) + u_theta * np.cos(theta)
    
    # Apply mask to velocities outside the cylinder
    u = np.ma.array(u, mask=mask)
    v = np.ma.array(v, mask=mask)
    
    # --- 2. Plotting ---

    # Streamfunction (solid lines)
    levels_psi = np.linspace(np.min(psi), np.max(psi), 40)
    ax.contour(X, Y, psi, levels=levels_psi, colors='blue', linewidths=0.8) # Set color explicitly

    # Potential function (dashed lines)
    levels_phi = np.linspace(np.min(phi), np.max(phi), 40)
    ax.contour(X, Y, phi, levels=levels_phi, colors="gray", linestyles="dashed", linewidths=0.5)

    # Velocity Quiver Plot (Arrows)
    # Slice the grid for a cleaner plot (e.g., every 20th point)
    Q = 20
    ax.quiver(X[::Q, ::Q], Y[::Q, ::Q], u[::Q, ::Q], v[::Q, ::Q], 
               color='black', units='xy', scale=10, width=0.03, 
               headwidth=5, headlength=5, headaxislength=4) 

    # Cylinder boundary
    circle = plt.Circle((0,0), R, color='red', fill=False, linewidth=1.5, zorder=10) # Set zorder high
    ax.add_artist(circle)
    
    # --- 3. Aesthetics ---
    ax.set_aspect('equal')
    if (Gamma == 0):
        title_text = f"Fonction de courant (bleu) et potentiel (gris)"
    else:
        title_text = f"$\\Gamma = {Gamma:.2f}$"

    
    # Then wrap the result in the LaTeX command
    
    ax.set_title(title_text, 
               fontsize=1.1*plt.rcParams['font.size'])
    if (show_ylabel): 
      ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
 
