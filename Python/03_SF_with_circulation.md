```python
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
from IPython.display import display

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
```


```python
def plot_stream_and_potential(Gamma):
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
    plt.title(f"Streamfunction (solid) and Potential (dashed) — Γ = {Gamma:.2f}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
```


```python
interact(
    plot_stream_and_potential,
    Gamma=FloatSlider(value=0.0, min=-10.0, max=10.0, step=0.1, continuous_update=False)
)
```


    interactive(children=(FloatSlider(value=0.0, continuous_update=False, description='Gamma', max=10.0, min=-10.0…





    <function __main__.plot_stream_and_potential(Gamma)>




```python

```


```python

```
