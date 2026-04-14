---
title: "Equivariance in Neural Networks: A Free Lunch That Isn't"
date: 2026-04-14
draft: false
math: true
tags: ["machine learning", "equivariance", "MLIPs", "geometric deep learning", "molecular simulation"]
description: "Enforcing rotational symmetry in neural networks sounds like a costless constraint: it encodes something we know must be true. So why are state-of-the-art models quietly abandoning it?"
---

Some inductive biases encode *beliefs* about the data: bets that certain hand-crafted
features matter, that certain regularities hold. These can be wrong. But some encode
*theorems* about the target function. These cannot be wrong. Rotational equivariance in
molecular simulation is one of them.

This post is about why encoding a provably correct theorem into a neural network is
harder than it sounds.

## What equivariance means

A function $f$ is [*equivariant*](https://en.wikipedia.org/wiki/Equivariant_map) with
respect to a group $G$ if transforming the input produces a correspondingly transformed
output [^gdl2021]:

$$f(g \cdot x) = g \cdot f(x) \quad \forall g \in G$$

<img src="/images/equivariance-diagram.svg" alt="Commutative diagram showing equivariance: rotating a molecule then predicting forces gives the same result as predicting forces then rotating." style="max-width: 100%; border: none; margin: 20px auto; display: block;">

For molecular simulations, the relevant transformations are rotations and translations.
The potential energy of a molecule is *invariant*: rotate it and the energy stays the
same. The forces are *equivariant*: they rotate with the molecule. This follows from
physics. A [machine-learned interatomic potential](https://en.wikipedia.org/wiki/Interatomic_potential) (MLIP) that violates rotational symmetry predicts a physically impossible
[energy surface](https://en.wikipedia.org/wiki/Potential_energy_surface). (A related but distinct constraint is *energy conservation*
[^darkforces2024]; Mark Neumann's [Modeling Symmetries](https://markneumann.xyz/blog/modeling-symmetries)
covers this well.)

Models like NequIP [^batzner2022], MACE [^batatia2022], and the Equiformer
family [^liao2023] build this symmetry directly into every layer. The inductive bias
is not a belief; it is a theorem baked into the network's structure.

## Why this seems like a free lunch

By restricting the hypothesis class to equivariant functions, you remove every physically
impossible function without losing any you actually want. The search space shrinks
dramatically. NequIP [^batzner2022] and MACE [^batatia2022] demonstrated
order-of-magnitude improvements in data efficiency, reaching chemical accuracy with only
a few hundred training structures. This is what makes the subsequent story surprising.

## The theorem is correct, the implementation is tricky

*Equivariance as a property* and *the mechanisms used to implement it* are not the same
thing. The theorem says the constraint is correct. It says nothing about the cost of
enforcing it.

In a standard network, a hidden feature is just a flat vector of numbers. In an
equivariant network, features must *transform predictably* under rotations. This makes
them structured objects, blocks grouped by type rather than interchangeable components:

<img class="wide-diagram" src="/images/feature-vector-diagram.svg" alt="Diagram showing an equivariant feature vector decomposed into irrep blocks (scalars, vectors, matrix-like), and how a rotation acts on each block independently.">

When a rotation $R$ is applied, each block transforms according to its type:

- **Scalars** ($\ell = 0$) are unchanged.
- **Vectors** ($\ell = 1$) are multiplied by $R$, the familiar 3x3 rotation matrix.
- **Degree-$\ell$ blocks** are multiplied by a $(2\ell+1) \times (2\ell+1)$ matrix
  $D^\ell(R)$ uniquely determined by $R$. For $\ell = 2$ this is a 5x5 matrix; the
  pattern continues for higher degrees.

The network's layers must preserve this block structure. Nonlinearities can only operate
on rotationally invariant quantities (like norms), and combining features of different
degrees requires [Clebsch-Gordan tensor products](https://en.wikipedia.org/wiki/Clebsch%E2%80%93Gordan_coefficients), which are far more expensive than standard matrix
multiplication. These constraints are where the practical costs come from.

Networks choose a **maximum degree** $L$: the highest $\ell$ in their features. Higher
$L$ gives finer angular resolution, but the cost grows rapidly.

> **Hypothesis 1: truncation at low $L$ may limit expressivity.** Current equivariant
> models typically use $L \leq 3$. If the true potential energy surface contains angular
> structure at higher frequencies, this truncation discards it. Whether this matters in
> practice — and for which chemical systems — is an open empirical question.

### The nonlinearity problem

Without nonlinearities, a hundred stacked linear layers are mathematically equivalent
to a single one. Nonlinearities like ReLU break this by selectively discarding
information: zeroing out negative components independently per dimension. This
direction-specific gating is what gives deep networks their expressive power. But
applying ReLU to a vector feature would break equivariance, because the coordinates
change under rotation.

The standard solution is a **norm nonlinearity**: apply a scalar function to the *norm*
of a vector, then rescale. For $\mathbf{v} = (v_x, v_y, v_z)$, this computes
$\sigma(\|\mathbf{v}\|) \cdot \hat{\mathbf{v}}$. It can learn complex functions of the
vector's *magnitude*, but preserves the direction exactly. It cannot respond differently
when the vector points up versus sideways. The two goals are in direct conflict:
expressive nonlinearities are direction-specific; equivariance requires all directions
to be treated the same.

### Do universality theorems save us?

Equivariant networks with norm nonlinearities are still universal approximators
[^dym2020] [^ravanbakhsh2020]. But these are *existence* results, not *efficiency*
results. They say nothing about how many layers are needed.

A concrete example: ReLU applied to $(1, -2, 3)$ produces $(1, 0, 3)$; applied to
$(-1, 2, 3)$ it produces $(0, 2, 3)$. The output depends on *which* components are
negative. A norm nonlinearity cannot distinguish these: both have norm $\sqrt{14}$, so
they get the same scaling. To build direction-dependent responses, the network must stack
multiple layers that project onto different axes, apply the norm nonlinearity, and
recombine. What a standard network does in one step requires an indirect multi-layer
construction.

Tensor product nonlinearities are more expressive [^maron2019] but significantly more
expensive per layer. And going deeper is itself hard: in standard networks, [residual
connections](https://en.wikipedia.org/wiki/Residual_neural_network) [^he2016] make depth tractable, but equivariant networks require compatible
irrep structure across layers. Most deployed models remain shallow
[^batatia2022] [^liao2023].

> **Hypothesis 2: constrained nonlinearities force a depth–expressivity trade-off.**
> Norm nonlinearities require more layers to match what standard activations do in one.
> But training deep equivariant networks is harder than training deep standard networks,
> so in practice models are shallower than they would need to be. If this is the case,
> equivariant models may be paying an expressivity cost not from the symmetry constraint
> itself, but from the difficulty of going deep enough to compensate for weaker
> nonlinearities.

## So what are we actually paying for?

The equivariance constraint itself costs nothing: the function class is correct, symmetry
is exact, and sample efficiency genuinely improves. The costs are in the *mechanisms* used
to achieve it: truncated irreps, constrained nonlinearities, expensive tensor
products [^geiger2022], and limited depth.

## Where the field is heading

The ideal would be an architecture that is **exactly equivariant, fully expressive, and
efficient on modern hardware**. Whether all three are achievable simultaneously is open,
but recent work is exploring different trade-offs.

*Cheaper equivariant primitives.* TensorNet [^simeon2023] sidesteps the [spherical
harmonics](https://en.wikipedia.org/wiki/Spherical_harmonics) machinery entirely, using Cartesian tensor representations that map more
naturally to standard matrix operations on GPUs. On the algorithmic side, Xie et
al. [^xie2026] recently reduced the complexity of Clebsch-Gordan tensor products from
$O(L^6)$ to $O(L^4 \log^2 L)$, bringing higher-$L$ models closer to practical reach.

*Learned equivariance via regularization.* Equigrad [^orbv3] penalizes equivariance
violations during training rather than enforcing them architecturally, though it is only
applicable to conservative models and requires careful tuning.

*Dropping the constraint entirely.* Bigi et al. [^unconstrained2026] showed that fully
unconstrained architectures can match equivariant models when trained on large enough
datasets, evidence that the *implementation cost* has grown large enough for flexible
models to compete in the large-data regime.

Equivariance is the right constraint. The question is whether we can enforce it "for free",
and if not, how much we are willing to pay.

---

*For further reading and lively community discussion on these topics, Chaitanya Joshi's
post [Equivariance is dead, long live equivariance?](https://chaitjo.substack.com/p/transformers-vs-equivariant-networks)
and Mark Neumann's [Modeling Symmetries](https://markneumann.xyz/blog/modeling-symmetries)
are both worth reading in full.*

---

[^batzner2022]: Batzner et al., *E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials*, Nature Communications 13 (2022). [doi.org/10.1038/s41467-022-29939-5](https://doi.org/10.1038/s41467-022-29939-5)

[^gdl2021]: Bronstein, Bruna, Cohen & Veličković, *Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges* (2021). [arxiv.org/abs/2104.13478](https://arxiv.org/abs/2104.13478)

[^batatia2022]: Batatia et al., *MACE: Higher order equivariant message passing neural networks for fast and accurate force fields*, NeurIPS 35 (2022). [arxiv.org/abs/2206.07697](https://arxiv.org/abs/2206.07697)

[^liao2023]: Liao & Smidt, *Equiformer: Equivariant Graph Attention Transformer for 3D Atomistic Graphs*, ICLR 2023. [arxiv.org/abs/2206.11990](https://arxiv.org/abs/2206.11990)

[^he2016]: He et al., *Deep Residual Learning for Image Recognition*, CVPR 2016. [arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)

[^dym2020]: Dym & Maron, *On the Universality of Rotation Equivariant Point Cloud Networks*, ICLR 2021. [arxiv.org/abs/2010.02449](https://arxiv.org/abs/2010.02449)

[^ravanbakhsh2020]: Ravanbakhsh, *Universal Equivariant Multilayer Perceptrons*, arXiv:2002.02912 (2020). [arxiv.org/abs/2002.02912](https://arxiv.org/abs/2002.02912)

[^maron2019]: Maron et al., *Universality of Equivariant Graph Networks*, NeurIPS 2019. [arxiv.org/abs/1905.04943](https://arxiv.org/abs/1905.04943)

[^unconstrained2026]: Bigi et al., *Pushing the limits of unconstrained machine-learned interatomic potentials*, arXiv:2601.16195 (2026). [arxiv.org/abs/2601.16195](https://arxiv.org/abs/2601.16195)

[^darkforces2024]: Bigi, Langer & Ceriotti, *The dark side of the forces: assessing non-conservative force models for atomistic machine learning*, arXiv:2412.11569 (2024). [arxiv.org/abs/2412.11569](https://arxiv.org/abs/2412.11569)

[^orbv3]: Rhodes et al., *Orb-v3: atomistic simulation at scale*, arXiv:2504.06231 (2025). [arxiv.org/abs/2504.06231](https://arxiv.org/abs/2504.06231)

[^geiger2022]: Geiger & Smidt, *e3nn: Euclidean Neural Networks*, arXiv:2207.09453 (2022). [arxiv.org/abs/2207.09453](https://arxiv.org/abs/2207.09453)

[^simeon2023]: Simeon & De Fabritiis, *TensorNet: Cartesian Tensor Representations for Efficient Learning of Molecular Potentials*, NeurIPS 36 (2023). [arxiv.org/abs/2306.06482](https://arxiv.org/abs/2306.06482)

[^xie2026]: Xie, Daigavane, Kotak & Smidt, *Asymptotically Fast Clebsch-Gordan Tensor Products with Vector Spherical Harmonics*, arXiv:2602.21466 (2026). [arxiv.org/abs/2602.21466](https://arxiv.org/abs/2602.21466)

