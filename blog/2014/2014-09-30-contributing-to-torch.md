# Contributing to Torch

**Date:** September 30, 2014

---

I recently started playing with the torch library again. Torch7 is now a growing set of packages, managed by luarocks. I really like this approach because it forces torch contributors to make their code more modular and re-usable.

So far, I have done a few very simple contributions to the torch ecosystem:

1) Extended the matio package, which reads MAT files, to support structs, cell arrays and strings, in addition to loading tensors, which was already implemented:

https://github.com/hpenedones/matio-ffi.torch

2) Started working on a metrics package for torch, which will compute things like ROC (Receiver Operator Curve) and Confusion Matrices. Probably dozens of other people have written similar code for torch, but I couldn't find an authoritative package doing just that. So, I started one at:

[https://github.com/hpenedones/metrics](https://github.com/hpenedones/metrics)

3) Finally, I did a small refactoring on my example project that uses convolutional neural networks for handwritten digit recognition. The code is now split into two files: one to load the USPS dataset and another one to create the network, train it and evaluate it. This makes it easier for new people to understand the example.

[https://github.com/hpenedones/luacnn](https://github.com/hpenedones/luacnn)

Enjoy it!
