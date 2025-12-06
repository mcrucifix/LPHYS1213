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
fig, axes = plt.subplots(1, 1, sharex=True, sharey=True)
plot_stream_and_potential(ax=axes, Gamma=0., show_ylabel=1.)
print('plot_stream')
filename = Path(figure_directory) / "03_zero_circulation.pdf"
plt.savefig(filename, bbox_inches='tight')

