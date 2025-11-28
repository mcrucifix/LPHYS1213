import numpy as np
import matplotlib
# Use Agg backend since we are generating PDFs and avoiding interactive issues
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from pathlib import Path

figure_directory =  ""

# --- 🎯 LaTeX Integration Setup ---
fig_width_in = 8.0 
fig_height_in = fig_width_in / 1.618 

plt.rcParams.update({
    "font.family": "sans-serif",          
    "font.sans-serif": ["Linux Libertinus Sans"], 
    "font.serif": ["Computer Modern Roman", "Times"], 
    "font.size": 11,                      
    "text.usetex": True,                  
    "pgf.rcfonts": False,                 
    "figure.figsize": (fig_width_in, fig_height_in),
    "savefig.format": "pdf",              
    "pdf.fonttype": 42                    
})
# -----------------------------------

# Parameters
U = 1.0        # free-stream velocity
R = 1.0       # cylinder radius
N = 400     # resolution

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
    

# plot 1 (No circulation)
fig, axes = plt.subplots(1, 3, sharex=True, sharey=True)
Gamma_values = [2., 4., 12.]
filename = Path(figure_directory) / "04_SF_with_circulation.pdf"

# Create a figure with 1 row and 3 columns of subplots
fig, axes = plt.subplots(1, 3, sharex=True, sharey=True)

# Loop through the Gamma values and corresponding axes
for i, Gamma in enumerate(Gamma_values):
    # Determine if we should show the y-label (only for the first plot)
    show_label = (i == 0)
    
    # Call the plotting function for the current subplot
    plot_stream_and_potential(ax=axes[i], Gamma=Gamma, show_ylabel=show_label)
    
# Add a super title for the whole figure
fig.suptitle("Fonctions de courant et potentiel poru différentes circulations", 
             fontsize=1.2*plt.rcParams['font.size'], y=0.95)

# Save the final figure
plt.savefig(filename, bbox_inches='tight')
plt.close(fig)
