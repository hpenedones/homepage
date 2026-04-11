"""Generate a diagram showing an equivariant feature vector decomposed into irrep blocks,
and how a rotation acts on each block independently."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(-0.5, 15.5)
ax.set_ylim(-0.8, 9.5)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("none")

# ── Colors ──────────────────────────────────────────────────────────────────

C_SCALAR = "#6BAF6B"
C_VECTOR = "#4A90D9"
C_MATRIX = "#D97A4A"
C_BG = "#F5F5F0"
C_ARROW = "#333333"
C_LABEL = "#333333"
C_SUBLABEL = "#777777"
C_UNCHANGED = "#6BAF6B"
C_ROTATED = "#C04040"

# ── Helper: draw a block of cells ──────────────────────────────────────────

def draw_block(ax, x, y, width, height, n_cells, color, values, label=None,
               label_above=True, zorder=2):
    """Draw a colored block split into n_cells, with values in each cell."""
    cell_w = width / n_cells
    for i in range(n_cells):
        rect = FancyBboxPatch((x + i * cell_w, y), cell_w, height,
                              boxstyle="round,pad=0.02", fc=color, ec="white",
                              lw=1.5, alpha=0.85, zorder=zorder)
        ax.add_patch(rect)
        if values and i < len(values):
            ax.text(x + i * cell_w + cell_w / 2, y + height / 2, values[i],
                    ha="center", va="center", fontsize=12, color="white",
                    fontweight="bold", fontfamily="monospace", zorder=zorder + 1)
    if label:
        ly = y + height + 0.2 if label_above else y - 0.25
        ax.text(x + width / 2, ly, label, ha="center", va="bottom" if label_above else "top",
                fontsize=10, color=C_LABEL, fontweight="bold")


# ── Layout parameters ──────────────────────────────────────────────────────

ROW_TOP = 7.0      # top row (before rotation)
ROW_BOT = 2.2      # bottom row (after rotation)
CELL_H = 0.8
CELL_W = 0.8

# ── Title ───────────────────────────────────────────────────────────────────

ax.text(7.5, 9.2,
        "How rotation acts on an equivariant feature vector",
        ha="center", va="center", fontsize=18, fontweight="bold",
        color=C_LABEL, fontfamily="serif")

# ── TOP ROW: original feature vector ───────────────────────────────────────

ax.text(0.0, ROW_TOP + CELL_H + 1.0,
        "Feature vector (one hidden layer of an equivariant network)",
        ha="left", va="bottom", fontsize=14, color=C_LABEL, fontfamily="serif")

# Scalars: 3 cells
s_x = 0.5
s_w = 3 * CELL_W
draw_block(ax, s_x, ROW_TOP, s_w, CELL_H, 3, C_SCALAR,
           ["$s_1$", "$s_2$", "$s_3$"])
ax.text(s_x + s_w / 2, ROW_TOP + CELL_H + 0.28, "$\\ell = 0$  (scalars)",
        ha="center", fontsize=13, color=C_SCALAR, fontweight="bold")

# Vectors: 2 blocks of 3
v1_x = s_x + s_w + 0.5
v1_w = 3 * CELL_W
draw_block(ax, v1_x, ROW_TOP, v1_w, CELL_H, 3, C_VECTOR,
           ["$v_x$", "$v_y$", "$v_z$"])

v2_x = v1_x + v1_w + 0.25
v2_w = 3 * CELL_W
draw_block(ax, v2_x, ROW_TOP, v2_w, CELL_H, 3, C_VECTOR,
           ["$u_x$", "$u_y$", "$u_z$"])
ax.text((v1_x + v2_x + v2_w) / 2, ROW_TOP + CELL_H + 0.28,
        "$\\ell = 1$  (vectors)",
        ha="center", fontsize=13, color=C_VECTOR, fontweight="bold")

# Matrix-like: 1 block of 5
m_x = v2_x + v2_w + 0.5
m_w = 5 * CELL_W
draw_block(ax, m_x, ROW_TOP, m_w, CELL_H, 5, C_MATRIX,
           ["$t_1$", "$t_2$", "$t_3$", "$t_4$", "$t_5$"])
ax.text(m_x + m_w / 2, ROW_TOP + CELL_H + 0.28, "$\\ell = 2$  (matrix-like)",
        ha="center", fontsize=13, color=C_MATRIX, fontweight="bold")

# Brace under entire vector
total_left = s_x
total_right = m_x + m_w
ax.annotate("", xy=(total_left, ROW_TOP - 0.2),
            xytext=(total_right, ROW_TOP - 0.2),
            arrowprops=dict(arrowstyle="-", color="#aaa", lw=0.8))
ax.text((total_left + total_right) / 2, ROW_TOP - 0.5,
        "16 numbers total   =   3 $\\times$ 1  +  2 $\\times$ 3  +  1 $\\times$ 5",
        ha="center", fontsize=12, color=C_SUBLABEL, fontfamily="serif")

# ── ROTATION ARROW (center) ────────────────────────────────────────────────

mid_x = (total_left + total_right) / 2
arrow_y_top = ROW_TOP - 0.9
arrow_y_bot = ROW_BOT + CELL_H + 0.9

ax.annotate("", xy=(mid_x, arrow_y_bot), xytext=(mid_x, arrow_y_top),
            arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.18",
                            color=C_ARROW, lw=2.5))
ax.text(mid_x, (arrow_y_top + arrow_y_bot) / 2,
        "  apply rotation $R$",
        ha="left", va="center", fontsize=15, color=C_ARROW,
        fontweight="bold", fontfamily="serif")

# ── BOTTOM ROW: after rotation ─────────────────────────────────────────────

ax.text(0.0, ROW_BOT + CELL_H + 1.0,
        "Same feature vector after rotating the input molecule",
        ha="left", va="bottom", fontsize=14, color=C_LABEL, fontfamily="serif")

# Scalars: unchanged
draw_block(ax, s_x, ROW_BOT, s_w, CELL_H, 3, C_SCALAR,
           ["$s_1$", "$s_2$", "$s_3$"])

# Annotation: unchanged
ax.text(s_x + s_w / 2, ROW_BOT - 0.35, "unchanged",
        ha="center", fontsize=12, color=C_UNCHANGED, fontweight="bold",
        fontstyle="italic")

# Vectors: rotated by R
draw_block(ax, v1_x, ROW_BOT, v1_w, CELL_H, 3, C_VECTOR,
           ["", "", ""])
ax.text(v1_x + v1_w / 2, ROW_BOT + CELL_H / 2, "$R \\mathbf{v}$",
        ha="center", va="center", fontsize=14, color="white",
        fontweight="bold", zorder=5)

draw_block(ax, v2_x, ROW_BOT, v2_w, CELL_H, 3, C_VECTOR,
           ["", "", ""])
ax.text(v2_x + v2_w / 2, ROW_BOT + CELL_H / 2, "$R \\mathbf{u}$",
        ha="center", va="center", fontsize=14, color="white",
        fontweight="bold", zorder=5)

ax.text((v1_x + v2_x + v2_w) / 2, ROW_BOT - 0.35,
        "each multiplied by 3$\\times$3 matrix $R$",
        ha="center", fontsize=12, color=C_ROTATED, fontweight="bold",
        fontstyle="italic")

# Matrix-like: rotated by D^2(R)
draw_block(ax, m_x, ROW_BOT, m_w, CELL_H, 5, C_MATRIX,
           ["", "", "", "", ""])
ax.text(m_x + m_w / 2, ROW_BOT + CELL_H / 2, "$D^2\\!(R)\\, \\mathbf{t}$",
        ha="center", va="center", fontsize=14, color="white",
        fontweight="bold", zorder=5)

ax.text(m_x + m_w / 2, ROW_BOT - 0.35,
        "multiplied by 5$\\times$5 matrix $D^2\\!(R)$",
        ha="center", fontsize=12, color=C_ROTATED, fontweight="bold",
        fontstyle="italic")

# ── Bottom annotation ──────────────────────────────────────────────────────

ax.text(mid_x, ROW_BOT - 1.0,
        "Each block transforms independently. "
        "The network's layers must preserve this block structure.",
        ha="center", fontsize=13, color=C_SUBLABEL, fontstyle="italic",
        fontfamily="serif")

plt.tight_layout()

fig.savefig("/home/hpenedones/source/homepage/static/images/feature-vector-diagram.svg",
            bbox_inches="tight", transparent=True)
fig.savefig("/home/hpenedones/source/homepage/static/images/feature-vector-diagram.png",
            bbox_inches="tight", dpi=200, transparent=True)
print("Done — saved SVG and PNG.")
