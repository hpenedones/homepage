"""Generate a diagram illustrating the Clebsch-Gordan tensor product of two vectors (ℓ=1),
showing how combining two 3-component inputs produces outputs at ℓ=0, ℓ=1, and ℓ=2."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(-0.5, 13.5)
ax.set_ylim(-0.5, 9.5)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("none")

# ── Colors ──────────────────────────────────────────────────────────────────

C_VEC_A = "#4A90D9"
C_VEC_B = "#7B68C8"
C_SCALAR = "#6BAF6B"
C_VECTOR = "#D97A4A"
C_MATRIX = "#C04040"
C_ARROW = "#333333"
C_LABEL = "#333333"
C_SUBLABEL = "#777777"
C_CG = "#555555"

# ── Helper: draw a block of cells ──────────────────────────────────────────

def draw_block(ax, x, y, width, height, n_cells, color, values, zorder=2):
    cell_w = width / n_cells
    for i in range(n_cells):
        rect = FancyBboxPatch((x + i * cell_w, y), cell_w, height,
                              boxstyle="round,pad=0.02", fc=color, ec="white",
                              lw=1.5, alpha=0.85, zorder=zorder)
        ax.add_patch(rect)
        if values and i < len(values):
            ax.text(x + i * cell_w + cell_w / 2, y + height / 2, values[i],
                    ha="center", va="center", fontsize=13, color="white",
                    fontweight="bold", fontfamily="monospace", zorder=zorder + 1)

CELL_H = 0.8
CELL_W = 0.85

# ── Title ───────────────────────────────────────────────────────────────────

ax.text(6.5, 9.2,
        "Clebsch–Gordan tensor product: combining two vectors ($\\ell = 1$)",
        ha="center", va="center", fontsize=16, fontweight="bold",
        color=C_LABEL, fontfamily="serif")

# ── INPUT: two vectors ──────────────────────────────────────────────────────

# Vector v
v_x = 1.0
v_y = 7.5
draw_block(ax, v_x, v_y, 3 * CELL_W, CELL_H, 3, C_VEC_A,
           ["$v_x$", "$v_y$", "$v_z$"])
ax.text(v_x + 1.5 * CELL_W, v_y + CELL_H + 0.25,
        "$\\mathbf{v}$  ($\\ell = 1$, dim 3)",
        ha="center", fontsize=13, color=C_VEC_A, fontweight="bold")

# Tensor product symbol
ax.text(5.0, v_y + CELL_H / 2, "$\\otimes$",
        ha="center", va="center", fontsize=28, color=C_CG, fontweight="bold")

# Vector u
u_x = 6.0
draw_block(ax, u_x, v_y, 3 * CELL_W, CELL_H, 3, C_VEC_B,
           ["$u_x$", "$u_y$", "$u_z$"])
ax.text(u_x + 1.5 * CELL_W, v_y + CELL_H + 0.25,
        "$\\mathbf{u}$  ($\\ell = 1$, dim 3)",
        ha="center", fontsize=13, color=C_VEC_B, fontweight="bold")

# ── CG box ──────────────────────────────────────────────────────────────────

cg_x = 3.5
cg_y = 5.3
cg_w = 6.0
cg_h = 1.0

rect = FancyBboxPatch((cg_x, cg_y), cg_w, cg_h,
                       boxstyle="round,pad=0.08", fc="#F0EDE8", ec=C_CG,
                       lw=2, zorder=2)
ax.add_patch(rect)
ax.text(cg_x + cg_w / 2, cg_y + cg_h / 2,
        "Clebsch–Gordan coefficients",
        ha="center", va="center", fontsize=13, color=C_CG,
        fontweight="bold", fontfamily="serif")

# Arrows from inputs to CG box
mid_v = v_x + 1.5 * CELL_W
mid_u = u_x + 1.5 * CELL_W
ax.annotate("", xy=(cg_x + cg_w * 0.3, cg_y + cg_h),
            xytext=(mid_v, v_y),
            arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.12",
                            color=C_ARROW, lw=2))
ax.annotate("", xy=(cg_x + cg_w * 0.7, cg_y + cg_h),
            xytext=(mid_u, v_y),
            arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.12",
                            color=C_ARROW, lw=2))

# ── OUTPUTS ─────────────────────────────────────────────────────────────────

out_y = 2.5

# ℓ = 0 output (scalar, 1 component)
s_x = 0.5
draw_block(ax, s_x, out_y, 1 * CELL_W, CELL_H, 1, C_SCALAR,
           ["$s$"])
ax.text(s_x + 0.5 * CELL_W, out_y + CELL_H + 0.25,
        "$\\ell = 0$",
        ha="center", fontsize=13, color=C_SCALAR, fontweight="bold")
ax.text(s_x + 0.5 * CELL_W, out_y - 0.3,
        "dot product",
        ha="center", fontsize=11, color=C_SCALAR, fontstyle="italic")
ax.text(s_x + 0.5 * CELL_W, out_y - 0.7,
        "$\\mathbf{v} \\cdot \\mathbf{u}$",
        ha="center", fontsize=13, color=C_SUBLABEL)

# Arrow from CG to scalar
ax.annotate("", xy=(s_x + 0.5 * CELL_W, out_y + CELL_H + 0.55),
            xytext=(cg_x + cg_w * 0.15, cg_y),
            arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.12",
                            color=C_SCALAR, lw=2))

# ℓ = 1 output (vector, 3 components)
v_out_x = 4.0
draw_block(ax, v_out_x, out_y, 3 * CELL_W, CELL_H, 3, C_VECTOR,
           ["$w_x$", "$w_y$", "$w_z$"])
ax.text(v_out_x + 1.5 * CELL_W, out_y + CELL_H + 0.25,
        "$\\ell = 1$",
        ha="center", fontsize=13, color=C_VECTOR, fontweight="bold")
ax.text(v_out_x + 1.5 * CELL_W, out_y - 0.3,
        "cross product",
        ha="center", fontsize=11, color=C_VECTOR, fontstyle="italic")
ax.text(v_out_x + 1.5 * CELL_W, out_y - 0.7,
        "$\\mathbf{v} \\times \\mathbf{u}$",
        ha="center", fontsize=13, color=C_SUBLABEL)

# Arrow from CG to vector
ax.annotate("", xy=(v_out_x + 1.5 * CELL_W, out_y + CELL_H + 0.55),
            xytext=(cg_x + cg_w * 0.5, cg_y),
            arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.12",
                            color=C_VECTOR, lw=2))

# ℓ = 2 output (degree-2, 5 components)
m_x = 8.5
draw_block(ax, m_x, out_y, 5 * CELL_W, CELL_H, 5, C_MATRIX,
           ["$t_1$", "$t_2$", "$t_3$", "$t_4$", "$t_5$"])
ax.text(m_x + 2.5 * CELL_W, out_y + CELL_H + 0.25,
        "$\\ell = 2$",
        ha="center", fontsize=13, color=C_MATRIX, fontweight="bold")
ax.text(m_x + 2.5 * CELL_W, out_y - 0.3,
        "traceless outer product",
        ha="center", fontsize=11, color=C_MATRIX, fontstyle="italic")
ax.text(m_x + 2.5 * CELL_W, out_y - 0.7,
        "$\\mathbf{v} \\otimes \\mathbf{u}$ (traceless symmetric part)",
        ha="center", fontsize=13, color=C_SUBLABEL)

# Arrow from CG to degree-2
ax.annotate("", xy=(m_x + 2.5 * CELL_W, out_y + CELL_H + 0.55),
            xytext=(cg_x + cg_w * 0.85, cg_y),
            arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.12",
                            color=C_MATRIX, lw=2))

# ── Bottom annotation ──────────────────────────────────────────────────────

ax.text(6.5, 1.2,
        "3 $\\times$ 3  =  1  +  3  +  5     (input dimensions multiply, "
        "output splits into irreps)",
        ha="center", fontsize=13, color=C_SUBLABEL, fontfamily="serif",
        fontstyle="italic")

ax.text(6.5, 0.5,
        "Selection rule:  $|\\ell_1 - \\ell_2| \\leq \\ell_{\\mathrm{out}}"
        " \\leq \\ell_1 + \\ell_2$"
        "     →     $|1 - 1| \\leq \\ell_{\\mathrm{out}} \\leq 1 + 1$"
        "     →     $\\ell_{\\mathrm{out}} \\in \\{0, 1, 2\\}$",
        ha="center", fontsize=12, color=C_SUBLABEL, fontfamily="serif")

plt.tight_layout()

fig.savefig("/home/hpenedones/source/homepage/static/images/cg-tensor-product-diagram.svg",
            bbox_inches="tight", transparent=True)
fig.savefig("/home/hpenedones/source/homepage/static/images/cg-tensor-product-diagram.png",
            bbox_inches="tight", dpi=200, transparent=True)
print("Done — saved SVG and PNG.")
