"""Generate a diagram showing SO(3) irreducible representations (spherical harmonics)
for ℓ = 0, 1, 2, 3 with labels, dimensions, and physical meaning."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm_y

# ── Spherical harmonic helpers ──────────────────────────────────────────────

def real_spherical_harmonic(ell, m, theta, phi):
    """Compute real-valued spherical harmonic Y_ell^m.
    scipy.special.sph_harm_y(l, m, theta, phi) uses physics convention:
    theta = polar (colatitude), phi = azimuthal."""
    if m > 0:
        return np.sqrt(2) * (-1)**m * np.real(sph_harm_y(ell, m, theta, phi))
    elif m < 0:
        return np.sqrt(2) * (-1)**m * np.imag(sph_harm_y(ell, -m, theta, phi))
    else:
        return np.real(sph_harm_y(ell, 0, theta, phi))


def spherical_harmonic_surface(ell, m, n_pts=80):
    """Return x, y, z, colors for a spherical harmonic surface plot.
    The radius is |Y_ℓ^m|, colored by sign."""
    theta = np.linspace(0, np.pi, n_pts)
    phi = np.linspace(0, 2 * np.pi, n_pts)
    theta, phi = np.meshgrid(theta, phi)

    Y = real_spherical_harmonic(ell, m, theta, phi)
    r = np.abs(Y)

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return x, y, z, Y


# ── Configuration ───────────────────────────────────────────────────────────

# For each ℓ, pick the most visually distinctive m value
IRREPS = [
    (0, 0,  "scalar",          "energy, charge",   1),
    (1, 1,  "vector",          "forces, dipole",   3),
    (2, 0,  "matrix / rank-2", "stress, quadrupole", 5),
    (3, 2,  "rank-3 tensor",   "octupole",         7),
]

# Colors: positive lobe / negative lobe
COLOR_POS = "#4A90D9"
COLOR_NEG = "#E8734A"

# ── Figure ──────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(14, 4.5))
fig.patch.set_facecolor("none")

for i, (ell, m, type_name, phys_name, dim) in enumerate(IRREPS):
    ax = fig.add_subplot(1, 4, i + 1, projection="3d")
    x, y, z, Y = spherical_harmonic_surface(ell, m)

    # Color by sign of Y
    colors = np.empty(Y.shape + (4,))
    pos_rgba = plt.cm.colors.to_rgba(COLOR_POS, alpha=0.85)
    neg_rgba = plt.cm.colors.to_rgba(COLOR_NEG, alpha=0.85)
    for idx in np.ndindex(Y.shape):
        colors[idx] = pos_rgba if Y[idx] >= 0 else neg_rgba

    ax.plot_surface(x, y, z, facecolors=colors, rstride=1, cstride=1,
                    linewidth=0, antialiased=True, shade=True)

    # Clean up axes
    max_r = np.max(np.abs([x, y, z])) * 1.15
    ax.set_xlim(-max_r, max_r)
    ax.set_ylim(-max_r, max_r)
    ax.set_zlim(-max_r, max_r)
    ax.set_box_aspect([1, 1, 1])
    ax.axis("off")
    ax.view_init(elev=20, azim=35)

    # Title and labels below
    ax.set_title(f"$\\ell = {ell}$", fontsize=18, fontweight="bold",
                 color="#333", pad=-2, fontfamily="serif")
    ax.text2D(0.5, 0.02, f"{type_name}\ndim {dim}  ·  {phys_name}",
              transform=ax.transAxes, ha="center", va="bottom",
              fontsize=10, color="#666", linespacing=1.5,
              fontfamily="sans-serif")

# Overall title
fig.suptitle("Irreducible representations of SO(3): the building blocks of equivariant features",
             fontsize=13, fontweight="bold", color="#333", y=0.98,
             fontfamily="serif")

# Bracket with dimension formula at bottom
fig.text(0.5, -0.02,
         "Each irrep has dimension $2\\ell + 1$. "
         "Any equivariant feature must decompose as a direct sum of these.",
         ha="center", va="top", fontsize=11, color="#888", style="italic",
         fontfamily="serif")

plt.tight_layout(rect=[0, 0.04, 1, 0.94])

fig.savefig("/home/hpenedones/source/homepage/static/images/irreps-diagram.svg",
            bbox_inches="tight", transparent=True)
fig.savefig("/home/hpenedones/source/homepage/static/images/irreps-diagram.png",
            bbox_inches="tight", dpi=200, transparent=True)
print("Done — saved SVG and PNG.")
