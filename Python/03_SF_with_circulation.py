import numpy as np
import matplotlib.pyplot as plt

# --- 🎯 LaTeX Integration Setup ---
# Set the figure width (8 inches) and use a suitable height for aspect ratio
fig_width_in = 8.0 
fig_height_in = fig_width_in / 1.618 # Golden ratio for height

# Configure Matplotlib for LaTeX output
plt.rcParams.update({
    "font.family": "sans-serif",          # Use sans-serif font
    "font.sans-serif": ["Linux Libertinus Sans"], # Specify the font
    "font.size": 11,                      # Base font size (11pt)
    "text.usetex": True,                  # Enable LaTeX rendering for text
    "pgf.rcfonts": False,                 # Disable TeX setting the font
    "figure.figsize": (fig_width_in, fig_height_in),
    "savefig.format": "pdf",              # Default to saving as PDF
    "pdf.fonttype": 42,                     # Embed fonts for better compatibility
    # Add a fallback for math symbols that need standard LaTeX math fonts (e.g., Gamma)
    # The default 'serif' family often handles the required math symbols
    "font.serif": ["Computer Modern Roman", "Times"], # Fallback/Primary font for math
})
# -----------------------------------


def plot_stream_and_potential(Gamma, filename="Out.pdf"):
    """Plot streamfunction (solid) and potential (dashed) for given circulation Gamma."""
    
    # Streamfunction
    psi = U*(r - R**2/r)*np.sin(theta) + Gamma/(2*np.pi)*np.log(r)
    psi = np.ma.array(psi, mask=mask)
    
    # Velocity potential
    phi = U*(r + R**2/r)*np.cos(theta) + Gamma/(2*np.pi)*theta
    phi = np.ma.array(phi, mask=mask)
    
    plt.figure(figsize=(6.6, 6.6))

    # Streamfunction (solid lines)
    levels_psi = np.linspace(np.min(psi), np.max(psi), 40)
    plt.contour(X, Y, psi, levels=levels_psi)

    # Potential function (dashed lines)
    levels_phi = np.linspace(np.min(phi), np.max(phi), 40)
    plt.contour(X, Y, phi, levels=levels_phi, colors="gray", linestyles="dashed")

    # Cylinder boundary
    circle = plt.Circle((0,0), R, color='black', fill=False, linewidth=2)
    plt.gca().add_artist(circle)
    
    plt.gca().set_aspect('equal')
    # --- 💡 FIX: Use \mathnormal or \mathrm to explicitly use the standard math font for the symbol ---
    # \mathnormal will use the standard LaTeX math font, which is usually Roman and contains Gamma.
    plt.title(r"Streamfunction (solid) and Potential (dashed) -- $\Gamma = {0:.2f}$".format(Gamma))

    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig(filename, format='pdf')
    

# plot 1
plot_stream_and_potential(0., filename="03_zero_circulation.pdf")

# plot 2
plot_stream_and_potential(1., filename="03_one_circulation.pdf")

