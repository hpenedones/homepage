---
title: "Equivariance in Neural Networks: A Free Lunch That Isn't"
date: 2026-04-11
draft: true
math: true
tags: ["machine learning", "equivariance", "MLIPs", "geometric deep learning", "molecular simulation"]
description: "Enforcing rotational symmetry in neural networks sounds like a costless constraint: it encodes something we know must be true. So why are state-of-the-art models quietly abandoning it?"
---

Most inductive biases in machine learning encode *beliefs* about the data — bets that
certain features matter, that certain regularities hold. These can be wrong. But some
encode *theorems* about the target function. These cannot be wrong. Rotational
equivariance in molecular simulation is one of them.

This post is about why encoding a provably correct theorem into a neural network
architecture is harder than it sounds.

## What equivariance means and why it is provably correct

A function $f$ is *equivariant* with respect to a group $G$ if applying a group transformation
to the input produces a correspondingly transformed output [^gdl2021]:

$$f(g \cdot x) = g \cdot f(x) \quad \forall g \in G$$

<img src="/images/equivariance-diagram.svg" alt="Commutative diagram showing equivariance: rotating a molecule then predicting forces gives the same result as predicting forces then rotating." style="max-width: 100%; border: none; margin: 20px auto; display: block;">

For molecular simulations, the relevant group is SE(3): rotations and translations
in three dimensions. The potential energy of a molecule is *invariant* under SE(3) —
rotate the whole molecule and the energy does not change. The forces on each atom
are *equivariant* — they rotate with the molecule. This follows directly from the laws
of physics; an MLIP (machine-learned interatomic potential) that violates rotational
symmetry is predicting a physically impossible energy surface.

The natural response is to build the symmetry directly into the architecture. Models
like NequIP [^batzner2022], MACE [^batatia2022], and the Equiformer family [^liao2023]
do exactly this: every layer is constrained to preserve equivariance. The inductive bias
is not a belief; it is a theorem baked into the network's structure.

## A related but distinct constraint: energy conservation

Equivariance is often discussed alongside energy conservation — the requirement that forces
are the negative gradient of a scalar potential:
$\mathbf{F} = -\nabla_\mathbf{r} E(\mathbf{r})$. These are conceptually separate constraints,
and the key asymmetry is that approximate equivariance is often good enough (and its
failures can be detected and mitigated, for example by averaging predictions over random
rotations [^batzner2022]), while approximate energy conservation is far more dangerous because
violations are silent and accumulate as unphysical energy drift during simulation
[^darkforces2024]. Mark Neumann's [Modeling Symmetries](https://markneumann.xyz/blog/modeling-symmetries)
post gives an excellent treatment of this distinction and is well worth reading in full.

## Why this seems like a free lunch

By restricting the hypothesis class to equivariant functions, you remove every physically
impossible function from consideration without losing any you actually want — the true
potential energy surface is equivariant, so it remains in the hypothesis class. The search
space shrinks dramatically without losing any relevant solutions.

The empirical record confirms this. NequIP [^batzner2022] and MACE [^batatia2022]
demonstrated order-of-magnitude improvements in data efficiency over non-equivariant
predecessors, reaching chemical accuracy with training sets of only a few hundred
structures.

This is what makes the subsequent story surprising.

## The theorem is correct. The implementation is not.

*Equivariance as a property* and *the mechanisms used to implement it* are not the same
thing. The theorem guarantees the former is a good constraint. It says nothing about the
latter.

Current equivariant architectures enforce symmetry through *Clebsch-Gordan (CG) tensor
products* of *irreducible representations* (irreps). Understanding where the costs come
from requires understanding this machinery.

### What equivariant features look like

In a standard network, a hidden feature is just a vector of numbers with no constraints
on what each component means. In an equivariant network, features must *transform
predictably* under rotations — rotate the input molecule, and every intermediate feature
must change in a well-defined way.

A classical result in group theory (Schur's lemma) [^gdl2021] gives the complete list of
objects that transform predictably under 3D rotations. They decompose into fundamental
types, indexed by a non-negative integer $\ell$ called the **degree**:

- **$\ell = 0$: scalar** (1 number). Does not change under rotation. Example: energy.
- **$\ell = 1$: vector** (3 numbers). Rotates the way a 3D arrow does. Example: force.
- **$\ell = 2$** (5 numbers). Captures more complex angular structure. Think of it as
  describing not just *which direction* but *which pair of directions* matter.
- **$\ell = 3$** (7 numbers). Even finer angular detail.
- And so on: degree $\ell$ has $2\ell + 1$ components.

These are called **irreducible representations** (irreps) because they cannot be broken into
simpler pieces that each transform independently — they are the atoms of equivariant
features.

A feature vector in an equivariant network is therefore a structured object made of
blocks, not a flat list of interchangeable numbers. For example, a feature might contain
3 scalars, 2 vectors, and 1 degree-2 block:

<img class="wide-diagram" src="/images/feature-vector-diagram.svg" alt="Diagram showing an equivariant feature vector decomposed into irrep blocks (scalars, vectors, matrix-like), and how a rotation acts on each block independently.">

When a rotation $R$ is applied, each block transforms according to its type:

- **Scalars** ($\ell = 0$) are unchanged.
- **Vectors** ($\ell = 1$) are multiplied by $R$, the familiar 3x3 rotation matrix.
- **Degree-2 blocks** ($\ell = 2$) are multiplied by $D^2(R)$, a 5x5 matrix uniquely
  determined by $R$. The details of how $D^2(R)$ is derived don't matter here — what
  matters is that for any rotation, there is exactly one correct matrix for each degree,
  just as $R$ is the one correct matrix for vectors. Degree $\ell$ has a
  $(2\ell+1) \times (2\ell+1)$ rotation matrix $D^\ell(R)$.

The network's layers must preserve this block structure. Nonlinearities must operate on
rotationally invariant quantities (like the norm of a vector block) or use tensor products
that respect the coupling rules — which is where the costs described below come from.

In practice, networks choose a **maximum degree** $L$: the highest $\ell$ in their
features. $L = 0$ means only scalars (no directional information). $L = 1$ adds vectors.
$L = 2$ adds degree-2 features, and so on. Higher $L$ gives finer angular resolution,
but the cost grows rapidly.

For readers interested in the mathematical foundations, these building blocks correspond
to [spherical harmonics](https://en.wikipedia.org/wiki/Spherical_harmonics), and the
$D^\ell(R)$ matrices are known as Wigner D-matrices. The Geometric Deep Learning
monograph [^gdl2021] provides a thorough treatment.

### The tensor product: expressive but expensive

In a standard network, combining two features is trivial: concatenate them, multiply
by a weight matrix, done. In an equivariant network, you cannot freely mix blocks of
different degrees — the result would not transform correctly under rotations. The only
way to combine two equivariant features while preserving equivariance is through a
*Clebsch-Gordan (CG) tensor product*.

The key idea is that combining two features of degree $\ell_1$ and $\ell_2$ does not
produce a single output — it produces outputs at *multiple* degrees. For example,
combining two vectors ($\ell = 1$) yields:

- a scalar ($\ell = 0$): this is the dot product — how aligned are they?
- a vector ($\ell = 1$): this is the cross product — what axis are they both
  perpendicular to?
- a degree-2 feature ($\ell = 2$): the traceless outer product — what is the full
  angular relationship?

The CG coefficients are fixed numbers (determined by group theory, not learned) that
specify exactly how to perform each of these combinations. The operation is the
equivariant analogue of matrix multiplication in a standard network — but considerably
more expensive.

The cost grows polynomially with the maximum degree $L$, but the polynomial is steep
enough to be painful in practice. Three factors compound:

1. **Feature vectors get wider.** Each degree $\ell$ contributes $2\ell + 1$ components.
   The total width for degrees $0$ through $L$ is $(L+1)^2$, so going from $L = 1$ to
   $L = 3$ grows the feature size from 4 to 16 — a 4$\times$ increase.

2. **Coupling paths multiply.** Every valid triple $(\ell_1, \ell_2, \ell_\text{out})$
   with $|\ell_1 - \ell_2| \leq \ell_\text{out} \leq \ell_1 + \ell_2$ is a separate
   tensor product that must be computed. The number of such triples is $O(L^3)$.

3. **Each path is itself non-trivial.** A single CG tensor product between degree
   $\ell_1$ and $\ell_2$ involves dense operations on blocks of size $2\ell + 1$, and
   must be performed for every pair of input features at those degrees.

For comparison, in a standard network doubling the hidden dimension roughly quadruples
the compute ($n^2$ scaling). In an equivariant network, increasing $L$ by one widens
every feature, adds new coupling paths, and makes each path more expensive — all at once.
The result is that going from $L = 2$ to $L = 6$ can easily increase the cost of a
single layer by over 100$\times$.

This is why models truncate at low $L$. MACE, for example, uses $L \leq 3$ in its
standard configurations [^batatia2022]. Features beyond degree $L$ cannot be captured
directly, though they can in principle be built up indirectly through products of
lower-order features across multiple layers.

### The nonlinearity problem: where things genuinely break

A subtler and arguably more fundamental cost is in the nonlinearities.

Recall what makes nonlinearities valuable: a hundred stacked linear layers are
mathematically equivalent to one. Nonlinearities like ReLU break this by discarding
information in a *direction-specific* way — zeroing out negative components independently
per dimension. This is what gives deep networks their expressive power.

For equivariant networks, this is where the cost becomes fundamental. A pointwise
nonlinearity applied to a vector feature would break equivariance: rotating then applying
ReLU gives a different result than applying ReLU then rotating, because ReLU treats each
coordinate independently and the coordinates change under rotation.

The workarounds are:

**Norm nonlinearities**: Apply a scalar nonlinearity to the *norm* of a vector feature, then
rescale. The direction is preserved; only the magnitude is transformed.

**Gating**: A learned scalar multiplies a higher-order feature. Directional information
survives, but interaction between components is limited.

**Tensor products as nonlinearities**: The CG product of a feature with itself is
information-preserving, but expensive.

The critical limitation becomes clear with a concrete example. For a vector
$\mathbf{v} = (v_x, v_y, v_z)$, a norm nonlinearity computes
$\sigma(\|\mathbf{v}\|) \cdot \hat{\mathbf{v}}$: it can learn complex functions of the
vector's *magnitude*, but it preserves the direction exactly. It cannot respond differently
when the vector points up versus sideways, because doing so would break equivariance.
An elementwise ReLU, by contrast, independently gates each component — it *can*
distinguish directions, which is precisely what makes standard networks expressive. The
two desiderata are in direct conflict: useful nonlinearities are direction-specific;
equivariance requires all directions to be treated the same.

### Do universality theorems save us?

Equivariant networks with norm nonlinearities are still universal approximators
[^dym2020] [^ravanbakhsh2020] — but these are *existence* results, not *efficiency*
results. They say nothing about how large the network needs to be.

To see why, consider applying ReLU componentwise to a vector $\mathbf{v} = (1, -2, 3)$.
A standard network produces $(1, 0, 3)$ in one operation — the negative component is
zeroed while the others are kept. Now try a different input: $(-1, 2, 3)$ gives $(0, 2, 3)$.
The output depends on *which* components are negative; the nonlinearity creates different
responses in different directions.

A norm nonlinearity cannot do this. Both inputs have the same norm
($\sqrt{14}$), so they produce the same scaling — the nonlinearity cannot tell them apart.
To build up a direction-dependent response, the network must use multiple layers that
effectively project the vector onto different axes, apply the norm nonlinearity to each
projection, and recombine. What a standard network does in one step requires an indirect
multi-layer construction.

Tensor product nonlinearities have stronger universality properties [^maron2019], but at
higher per-layer cost. The trade-off is clear: norm nonlinearities are cheap but may
require many layers; tensor products are expensive but need fewer.

### Depth compounds the problem

In standard networks, residual connections [^he2016] make very deep networks trainable.
In equivariant networks, stacking layers is less straightforward: the irrep degrees must be
compatible across layers, and the coupling structure must be redesigned accordingly. Most
deployed equivariant models remain relatively shallow [^batatia2022] [^liao2023].

## The honest accounting

**No cost:**
- The function class is correct — no expressiveness is lost.
- Sample efficiency is genuinely improved.
- Symmetry is exact, not approximate.

**Real costs:**
- Truncation at low $\ell$ limits angular resolution.
- Nonlinearities are restricted to norm-based or gating operations, requiring more depth
  than standard activations to approximate the same functions.
- CG products are expensive and hard to accelerate on GPUs optimized for dense matrix
  operations [^geiger2022].
- Deep equivariant networks remain relatively unexplored.

The costs are not in the equivariance constraint itself, but in the mechanisms
(CG products, constrained nonlinearities, truncated irreps) used to *achieve* it.

## What the theoretical ideal looks like

What would it take to get equivariance without paying these costs? The ideal architecture
would be:

1. **Exactly equivariant** under SE(3)
2. **Fully expressive** — not truncated at low $\ell$
3. **Unconstrained nonlinearities** — no information discarded by design
4. **Trainable to arbitrary depth**
5. **Efficient on modern hardware** — maps well to GPU-style dense computation

Whether such a thing exists in a computationally tractable form is genuinely open, but
there are partial answers.

*Frame-based methods* [^puny2021] attach a local coordinate frame to each atom,
apply an arbitrary network inside it, and transform back. This recovers near-full
expressiveness, but as Puny et al. discuss, the frame construction can be discontinuous
at symmetric configurations.

*Learned equivariance via regularization* offers a different approach. Equigrad [^orbv3],
introduced in the Orb V3 forcefield, penalizes equivariance violations during training by
computing the gradient of the predicted energy with respect to a rotation applied at the
input — for a perfectly equivariant model this gradient is zero. This encourages the model
to learn equivariance without requiring equivariant layers, though it is only applicable to
conservative models and requires careful tuning.

Recent work [^unconstrained2026] has shown that fully unconstrained architectures can
reach competitive accuracy with equivariant models when trained on large enough datasets.
This is not a refutation of equivariance — it is evidence that the *implementation cost*
has grown large enough that, in the large-data regime, a flexible model can match a
constrained one.

The equivariance theorem is still correct. The implementation just has not caught up.

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

[^simeon2023]: Simeon & De Fabritiis, *TensorNet: Cartesian Tensor Representations for Efficient Learning of Molecular Potentials*, NeurIPS 36 (2023). [arxiv.org/abs/2306.06482](https://arxiv.org/abs/2306.06482)

[^he2016]: He et al., *Deep Residual Learning for Image Recognition*, CVPR 2016. [arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)

[^puny2021]: Puny et al., *Frame Averaging for Invariant and Equivariant Network Design*, ICLR 2022. [arxiv.org/abs/2110.03336](https://arxiv.org/abs/2110.03336)

[^dym2020]: Dym & Maron, *On the Universality of Rotation Equivariant Point Cloud Networks*, ICLR 2021. [arxiv.org/abs/2010.02449](https://arxiv.org/abs/2010.02449)

[^ravanbakhsh2020]: Ravanbakhsh, *Universal Equivariant Multilayer Perceptrons*, arXiv:2002.02912 (2020). [arxiv.org/abs/2002.02912](https://arxiv.org/abs/2002.02912)

[^maron2019]: Maron et al., *Universality of Equivariant Graph Networks*, NeurIPS 2019. [arxiv.org/abs/1905.04943](https://arxiv.org/abs/1905.04943)

[^unconstrained2026]: Bigi et al., *Pushing the limits of unconstrained machine-learned interatomic potentials*, arXiv:2601.16195 (2026). [arxiv.org/abs/2601.16195](https://arxiv.org/abs/2601.16195)

[^darkforces2024]: Bigi, Langer & Ceriotti, *The dark side of the forces: assessing non-conservative force models for atomistic machine learning*, arXiv:2412.11569 (2024). [arxiv.org/abs/2412.11569](https://arxiv.org/abs/2412.11569)

[^orbv3]: Rhodes et al., *Orb-v3: atomistic simulation at scale*, arXiv:2504.06231 (2025). [arxiv.org/abs/2504.06231](https://arxiv.org/abs/2504.06231)

[^geiger2022]: Geiger & Smidt, *e3nn: Euclidean Neural Networks*, arXiv:2207.09453 (2022). [arxiv.org/abs/2207.09453](https://arxiv.org/abs/2207.09453)
