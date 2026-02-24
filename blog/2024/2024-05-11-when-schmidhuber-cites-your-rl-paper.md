# When Schmidhuber Cites Your RL Paper

**Date:** May 11, 2024

**Original post:** [LinkedIn](https://www.linkedin.com/posts/hpenedones_that-feeling-when-schmidhuber-cites-your-activity-7195052610528149504-58pu)

---

That feeling when Schmidhuber cites your (not well known) RL paper! 😝

![Schmidhuber citing our 2019 NeurIPS RL paper](../images/schmidhuber_cites_rl_paper.jpg)

Our 2019 NeurIPS paper ["Adaptive Temporal-Difference Learning for Policy Evaluation with Per-State
Uncertainty Estimates"](https://arxiv.org/abs/1906.07871) didn't catch much attention, but it actually
addresses a very fundamental problem in Deep Reinforcement Learning: how can you trust Temporal
Difference updates, when you are not in a tabular setting, and instead your function approximator is a
neural network?

The value estimate of the neural network at a given state, can be perturbed during learning, even if
the mini batch contained a set of completely different states. But if you now use that value estimate
to bootstrap the value of another, you might be propagating estimation errors further. We suggested a
technique using uncertainty estimation, that can cleverly decide, at each state, whether you should
rely on Monte Carlo targets or you can trust TD targets.

Seems like in 2021 it was also cited by Michael Jordan (Berkeley). 🤯 With a total of only 8
citations, 2 are from papers of legendary, highly influential ML researchers.

A precursor paper to this one, which also has only 8 citations, includes mentions from E Bengio
(Yoshua's son), Joelle Pineau and Doina Precup. Another precursor paper, that has only 14 citations,
was cited in one of Rich Sutton's papers.

I'm going to update my "research pride index" to focus less on AlphaFold 1 and increase the weight
on this line of RL research! Like in PageRank -- citations from more prestigious, influential
scientists, weigh more. Eh eh. 😀

Back to real life... 🌞😎
