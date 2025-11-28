#!/usr/bin/env python
# coding: utf-8

# # Vortex streamfunction, trajectory and streakline visualization\nThis notebook implements the regular vortex described and provides interactive visualization.\n

# In[5]:



# Vortex streamfunction + trajectory + streakline notebook
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from functools import lru_cache
import math

# Parameters
a = 20.0
omega0 = 0.18   # amplitude parameter (tuneable)
Nx, Ny = 100, 100
x_vals = np.linspace(0, 100, Nx)
y_vals = np.linspace(-50, 50, Ny)
X, Y = np.meshgrid(x_vals, y_vals)

def psi_field(t):
    """Return streamfunction psi on the grid for vortex centered at (t,0)."""
    x0 = t
    Xp = X - x0
    Yp = Y
    r2 = Xp**2 + Yp**2
    psi = (omega0 * a**2 / 4.0) * np.exp(-r2 / a**2)
    return psi

def velocity_at_point(x, y, t):
    """Return (u_x, u_y) at a point (x,y) and time t."""
    x0 = t
    xp = x - x0
    yp = y
    r = math.hypot(xp, yp)
    if r == 0.0:
        return 0.0, 0.0
    vtheta = 0.5 * omega0 * r * math.exp(-r*r / (a*a))
    ux = - vtheta * (yp / r)
    uy =   vtheta * (xp / r)
    return ux, uy

def velocity_field(t):
    """Return vector fields (Ux, Uy) on the grid at time t."""
    x0 = t
    Xp = X - x0
    Yp = Y
    r = np.sqrt(Xp**2 + Yp**2)
    with np.errstate(divide='ignore', invalid='ignore'):
        vtheta = 0.5 * omega0 * r * np.exp(-(r**2)/(a**2))
        ux = - vtheta * (Yp / r)
        uy =   vtheta * (Xp / r)
        ux = np.nan_to_num(ux)
        uy = np.nan_to_num(uy)
    return ux, uy

# Particle trajectory: integrate dx/dt = u_x(x,y,t), dy/dt = u_y(x,y,t).
def trajectory(Tmax=100.0, dt=0.5):
    t_eval = np.arange(0.0, Tmax+dt, dt)
    def rhs(t, z):
        x, y = z
        ux, uy = velocity_at_point(x, y, t)
        return [ux, uy]
    z0 = [50.0, 0.0]
    sol = solve_ivp(rhs, (0.0, Tmax), z0, t_eval=t_eval, rtol=1e-6, atol=1e-8, max_step=1.0)
    return sol.t, sol.y[0,:], sol.y[1,:]

# Streakline at time t: for many release times s in [0,t], advect particle from s to t starting at (50,0).
def streakline_at_time(t, n_releases=200):
    release_times = np.linspace(0.0, t, n_releases)
    pts = []
    for s in release_times:
        if s == t:
            pts.append((50.0, 0.0))
            continue
        def rhs(tt, z):
            x, y = z
            ux, uy = velocity_at_point(x, y, tt)
            return [ux, uy]
        z0 = [50.0, 0.0]
        sol = solve_ivp(rhs, (s, t), z0, t_eval=[t], rtol=1e-6, atol=1e-8, max_step=1.0)
        pts.append((sol.y[0,-1], sol.y[1,-1]))
    pts = np.array(pts)
    return pts[:,0], pts[:,1]

# Precompute the full trajectory once (0..100)
t_traj, traj_x, traj_y = trajectory(Tmax=100.0, dt=0.5)

# Simple plotting routine for a given time t
def plot_state(t, ax=None, plot_streamfunction_levels=25, show_grid=True, show_particles=True, streak_n=300):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8,5))
    psi = psi_field(t)
    cs = ax.contour(X, Y, psi, levels=plot_streamfunction_levels, linewidths=0.8)
    ax.clabel(cs, inline=1, fontsize=8)
    Ux, Uy = velocity_field(t)
    step = max(1, Nx//20)
    ax.quiver(X[::step, ::step], Y[::step, ::step], Ux[::step, ::step], Uy[::step, ::step], scale=50)
    idx = np.searchsorted(t_traj, t)
    ax.plot(traj_x[:idx+1], traj_y[:idx+1], linewidth=2, label='trajectory (from 50,0)', color='blue')
    sx, sy = streakline_at_time(t, n_releases=streak_n)
    ax.plot(sx, sy, linewidth=2, label='streakline (source at 50,0)', color='red')
    if idx < len(traj_x):
        ax.plot(traj_x[idx], traj_y[idx], 'o', color='blue')
    ax.set_xlim(x_vals.min(), x_vals.max())
    ax.set_ylim(y_vals.min(), y_vals.max())
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f"t = {t:.2f}, vortex center = ({t:.2f},0)")
    ax.legend(loc='upper left')
    if show_grid:
        ax.grid(True, linestyle='--', alpha=0.3)
    return ax


# In[6]:



# Interactive slider (works when ipywidgets is enabled in the Jupyter environment)
import matplotlib.pyplot as plt



fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Left panel: t=50
plot_state(50, ax=axes[0], plot_streamfunction_levels=25, streak_n=300)
axes[0].set_title("t = 50")

# Right panel: t=100
plot_state(100, ax=axes[1], plot_streamfunction_levels=25, streak_n=300)
axes[1].set_title("t = 100")


plt.savefig("01_vortex_streamlines.pdf")
plt.close()

