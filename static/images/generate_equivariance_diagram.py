"""Generate a commutative diagram illustrating SE(3) equivariance for molecular forces."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ── Molecule drawing helpers ────────────────────────────────────────────────

ATOM_COLORS = {"O": "#E04040", "H": "#4090E0", "N": "#3050C0"}
ATOM_RADII = {"O": 0.18, "H": 0.13, "N": 0.16}


def draw_molecule(ax, positions, elements, bonds, forces=None,
                  alpha=1.0, zorder=2):
    """Draw atoms, bonds, and optional force arrows."""
    # Bonds
    for i, j in bonds:
        ax.plot(*zip(positions[i], positions[j]),
                color="#888888", lw=2.2, solid_capstyle="round",
                alpha=alpha, zorder=zorder)
    # Atoms
    for k, (pos, el) in enumerate(zip(positions, elements)):
        circle = plt.Circle(pos, ATOM_RADII[el], fc=ATOM_COLORS[el],
                            ec="white", lw=1.4, alpha=alpha, zorder=zorder + 1)
        ax.add_patch(circle)
        ax.text(*pos, el, ha="center", va="center", fontsize=7,
                fontweight="bold", color="white", alpha=alpha, zorder=zorder + 2)
    # Forces
    if forces is not None:
        for pos, f in zip(positions, forces):
            if np.linalg.norm(f) < 1e-6:
                continue
            ax.annotate("", xy=(pos[0] + f[0], pos[1] + f[1]), xytext=pos,
                        arrowprops=dict(arrowstyle="->,head_width=0.12,head_length=0.10",
                                        color="#E8A020", lw=2.0,
                                        shrinkA=ATOM_RADII.get("O", 0.15) * 72 * 0.45,
                                        shrinkB=0),
                        zorder=zorder + 3)


def rotate_2d(points, angle_deg):
    """Rotate an array of 2-D points around the origin."""
    theta = np.radians(angle_deg)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return (R @ np.asarray(points).T).T


# ── Molecule definition (water-like, easy to recognise) ─────────────────────

mol_pos = np.array([[0.0, 0.12],       # O (top-centre)
                    [-0.30, -0.18],     # H (left)
                    [ 0.30, -0.18]])    # H (right)
mol_elem = ["O", "H", "H"]
mol_bonds = [(0, 1), (0, 2)]

# Forces on the original molecule (arbitrary but plausible-looking)
forces_orig = np.array([[ 0.00,  0.30],
                        [-0.25, -0.15],
                        [ 0.25, -0.15]])

ROT_ANGLE = 55  # degrees – visually clear rotation

mol_pos_rot = rotate_2d(mol_pos, ROT_ANGLE)
forces_rot = rotate_2d(forces_orig, ROT_ANGLE)

# ── Layout constants ────────────────────────────────────────────────────────

CX_L, CX_R = 1.0, 4.6          # horizontal centres of left / right panels
CY_T, CY_B = 2.6, 0.5          # vertical centres of top / bottom rows
PANEL_W, PANEL_H = 1.8, 1.5     # light background rectangles

# ── Figure ──────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8.2, 5.0))
ax.set_xlim(-0.4, 6.0)
ax.set_ylim(-0.45, 3.85)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("none")

# Light background panels
for cx, cy in [(CX_L, CY_T), (CX_R, CY_T), (CX_L, CY_B), (CX_R, CY_B)]:
    rect = FancyBboxPatch((cx - PANEL_W / 2, cy - PANEL_H / 2),
                          PANEL_W, PANEL_H,
                          boxstyle="round,pad=0.08", fc="#F5F5F0",
                          ec="#CCCCCC", lw=0.8, zorder=0)
    ax.add_patch(rect)

# ── Draw molecules ──────────────────────────────────────────────────────────

# Top-left: input molecule  x
draw_molecule(ax, mol_pos + [CX_L, CY_T], mol_elem, mol_bonds)

# Top-right: rotated input  R·x
draw_molecule(ax, mol_pos_rot + [CX_R, CY_T], mol_elem, mol_bonds)

# Bottom-left: output f(x) — molecule + forces
draw_molecule(ax, mol_pos + [CX_L, CY_B], mol_elem, mol_bonds,
              forces=forces_orig)

# Bottom-right: rotated output R·f(x) = f(R·x) — rotated molecule + rotated forces
draw_molecule(ax, mol_pos_rot + [CX_R, CY_B], mol_elem, mol_bonds,
              forces=forces_rot)

# ── Arrows between panels ──────────────────────────────────────────────────

arrow_kw = dict(arrowstyle="->,head_width=0.18,head_length=0.14",
                color="#333333", lw=1.6, connectionstyle="arc3,rad=0")

gap = 0.12  # gap from panel edge

# Horizontal arrows  (rotate R)
for cy in [CY_T, CY_B]:
    ax.annotate("", xy=(CX_R - PANEL_W / 2 + gap, cy),
                xytext=(CX_L + PANEL_W / 2 - gap, cy),
                arrowprops=arrow_kw, zorder=5)

# Vertical arrows  (apply f)
for cx in [CX_L, CX_R]:
    ax.annotate("", xy=(cx, CY_B + PANEL_H / 2 - gap),
                xytext=(cx, CY_T - PANEL_H / 2 + gap),
                arrowprops=arrow_kw, zorder=5)

# ── Labels ──────────────────────────────────────────────────────────────────

label_fs = 13
math_style = dict(fontsize=label_fs, ha="center", va="center", color="#333333")

# Horizontal labels: "rotate R"
for cy, nudge in [(CY_T, 0.18), (CY_B, 0.18)]:
    mid_x = (CX_L + CX_R) / 2
    ax.text(mid_x, cy + nudge, r"rotate $R$", **math_style)

# Vertical labels: "predict f"
for cx, nudge in [(CX_L, -0.38), (CX_R, -0.38)]:
    mid_y = (CY_T + CY_B) / 2
    ax.text(cx + nudge, mid_y, r"predict $f$", rotation=90,
            fontsize=label_fs, ha="center", va="center", color="#333333")

# Panel corner labels (top-right corner of each panel)
ax.text(CX_L + PANEL_W / 2 - 0.08, CY_T + PANEL_H / 2 - 0.12,
        r"$\mathbf{x}$", fontsize=13, color="#555555", ha="right", va="top")
ax.text(CX_R + PANEL_W / 2 - 0.08, CY_T + PANEL_H / 2 - 0.12,
        r"$R \cdot \mathbf{x}$", fontsize=13, color="#555555", ha="right", va="top")
ax.text(CX_L + PANEL_W / 2 - 0.08, CY_B + PANEL_H / 2 - 0.12,
        r"$f(\mathbf{x})$", fontsize=13, color="#555555", ha="right", va="top")
ax.text(CX_R + PANEL_W / 2 - 0.08, CY_B + PANEL_H / 2 - 0.12,
        r"$f(R \cdot \mathbf{x})$", fontsize=11, color="#555555", ha="right", va="top")

# Equality annotation — centred below diagram
ax.text((CX_L + CX_R) / 2, CY_B - PANEL_H / 2 - 0.22,
        "both paths give the same result",
        fontsize=9, ha="center", va="top", color="#888888", style="italic")

# Title
ax.text((CX_L + CX_R) / 2, 3.70,
        "Equivariance: rotating the input then predicting\n"
        "is the same as predicting then rotating",
        fontsize=12, ha="center", va="center", color="#333333",
        fontweight="bold", linespacing=1.4)

fig.savefig("/home/hpenedones/source/homepage/static/images/equivariance-diagram.svg",
            bbox_inches="tight", transparent=True)
fig.savefig("/home/hpenedones/source/homepage/static/images/equivariance-diagram.png",
            bbox_inches="tight", dpi=200, transparent=True)
print("Done — saved SVG and PNG.")
