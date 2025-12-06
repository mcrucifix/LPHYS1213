import numpy as np
import matplotlib
# Use Agg backend since we are generating PDFs and avoiding interactive issues
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from pathlib import Path
from localtools import plot_stream_and_potential

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

# plot with circulation
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
fig.suptitle("Fonctions de courant et potentiel pour différentes circulations", 
             fontsize=1.2*plt.rcParams['font.size'], y=0.95)

# Save the final figure
plt.savefig(filename, bbox_inches='tight')
plt.close(fig)
