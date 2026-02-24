# Yoshua Bengio's talk in London

**Date:** April 16, 2015

---

Yesterday I attended a [talk organized by the London Machine Learning meetup group, where Yoshua Bengio was the invited speaker](http://www.meetup.com/London-Machine-Learning-Meetup/events/221601571/). Not surprisingly, there were about 200 people attending.

![deep_learning_theory](../../images/deep_learning_theory.jpg)

Yoshua reinforced the idea that a lot of the success of learning algorithms for AI tasks comes from incorporating meaningful priors. These should be general enough to hold true in a wide range of applications, but also specific enough to vastly reduce the amount of training data needed to achieve good generalization. This reminded me of a [previous post](post.html#2010-11-12-the-ai-set-of-functions) I wrote in this blog, almost 5 years ago!

In the meanwhile, deep learning became main-stream, and Yoshua's slides highlighted several theoretical progresses that were made, e.g:

1. Expressiveness of deep networks with piecewise linear activation functions: exponential advantage for depth ([Montufar et al NIPS 2014](http://papers.nips.cc/paper/5422-on-the-number-of-linear-regions-of-deep-neural-networks))
2. Theoretical and empirical evidence against bad local minima ([Dauphin et al NIPS 2014](http://papers.nips.cc/paper/5486-sparse-pca-via-covariance-thresholding))
3. Manifold and probabilistic interpretations of auto-encoders:

- Estimating the gradient of the energy function ([Alain and Bengio ICLR 2013](http://arxiv.org/abs/1211.4246))
- Sampling via Markov chain ([Bengio et al NIPS 2013](http://papers.nips.cc/paper/5023-generalized-denoising-auto-encoders-as-generative-models))
- Variational auto-encoder breakthrough ([Gregor et al arXiv 2015](http://arxiv.org/abs/1502.04623))

Enjoy reading!
