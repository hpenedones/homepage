# The Future of AI is Physical: Simulation is Key

**Date:** November 7, 2025

**Original URL:** https://inductiva.ai/blog/article/the-future-of-ai-is-physical-simulation-is-key

---

Everyone's talking about LLMs, but it is already pretty clear what the next big wave will be: AI for the physical world. AI that understands intuitive physics, not only the mechanics of large rigid bodies, which is fundamental for Robotics and autonomous driving, but also AI that understands fluid dynamics, thermodynamics, electromagnetism, plasmas, and even the quantum physics that governs the small scale of atoms and molecules. Every major industry stands to gain, including automotive and transportation, renewable energy (wind, solar, nuclear), pharmaceutical and materials development, you name it!

The consensus around that vision is building up fast:

- [Jeff Dean (Google)](https://www.youtube.com/watch?app=desktop&v=dq8MhTFCs80&t=641s) — on simulation and surrogate models for weather forecasting, materials, etc.
- [Yann LeCun (Meta)](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/) — announcing JEPA-2 world models that learn intuitive physics, and the new META [OMol25 dataset](https://huggingface.co/facebook/OMol25) of molecules.
- [Demis Hassabis (Google Deepmind)](https://www.youtube.com/watch?v=h229ZyUxOL4&pp=ygUYZGVtaXMgaGFzc2FiaXMgYWxwaGFmb2xk) – [explaining AlphaFold on Lex Friedman](https://www.youtube.com/watch?v=hHooQmmzG4k) and giving a talk on using AI for Science breakthroughs
- [Jensen Huang (NVIDIA)](https://www.youtube.com/shorts/AP1B37rPrpQ) – on [AI for weather forecasting](https://www.youtube.com/watch?v=9vEaImsSCrw) (with cool visualizations), and on [large scale humanoid Robotics](https://www.youtube.com/watch?v=LETO_-keVFg).

In this article I try to explain why numerical simulation is such a key component of AI for the Physical world. My perspective comes from having helped kick-start DeepMind's [AlphaFold](https://deepmind.google/science/alphafold/) project, and more recently, being a co-founder and CTO of [Inductiva.AI](https://inductiva.ai/).

## 🔬 Learning from real experimental data (AlphaFold)

In early 2016, the Applied team at DeepMind organized an internal hackathon where Rich Evans, Marek Barwinski and myself, played with Deep RL and stochastic search algorithms on top of [FoldIt](https://fold.it/) — a gamified environment for protein folding. This generated enough enthusiasm that Steve Crossan and DeepMind co-founders Demis Hassabis and Mustafa Suleyman, encouraged us to start working on this full-time. Andrew Senior, Laurent Sifre and James Kirkpatrick joined the team and efforts towards [AlphaFold 1](https://www.nature.com/articles/s41586-019-1923-7) began (at that point, the internal code name was actually project “Origami”).

Protein structure prediction was a long standing open problem in computational biology and organic chemistry, because it was/is computationally unfeasible to simulate the folding process from first principles, e.g. using molecular dynamics. Other computational techniques, like template matching techniques or optimization algorithms, were insufficient to achieve high accuracy.

Fast forward a few years and [AlphaFold 2](https://www.nature.com/articles/s41586-021-03819-2) basically solved the problem of Protein Structure Prediction: given a sequence of amino acids, predict the 3D structure of the protein. The [Chemistry Nobel prize in 2024](https://www.nobelprize.org/prizes/chemistry/2024/summary/) brought recognition to AlphaFold and countless projects are now building on top of its predictions.

Even though the very [first version of AlphaFold](https://onlinelibrary.wiley.com/doi/full/10.1002/prot.25834) (the only one I contributed to) used physics energy functions computed by [Rosetta](https://rosettacommons.org/) , all subsequent versions relied almost exclusively on real experimental data, gathered on wet labs for decades, made available publicly via the [Protein Data Bank](https://www.rcsb.org/) (PDB). Using experimental data is so great, that [IsoMorphic Labs](https://www.isomorphiclabs.com/) , the spinout of DeepMind devoted to AI drug design, recently [announced](https://www.gov.uk/government/news/uk-to-become-world-leader-in-drug-discovery-as-technology-secretary-heads-for-london-tech-week) a joint effort with Imperial College to gather more experimental data on how molecules bind to each other, called the [OpenBind consortium](https://openbind.uk/) .

Based on the success of AlphaFold, one could assume that progress in AI for Science, depends exclusively on the availability of real world experimental data. However, I will argue that this is perhaps the exception, not the norm.

Perhaps there are ways of benefiting from our knowledge of Physics, more directly?

## 🧠 Neural Networks and the Laws of Physics

If we already know the fundamental laws of Physics to great precision, can we directly incorporate them into neural networks — to shortcut the need of collecting data?

Unfortunately, not quite. The current state of affairs is that we need to train neural networks with millions or billions of parameters from scratch from sample data, even though we already know the very compact laws of physics that underpin that data! The regime where deep learning works really well is still the supervised learning setting, using the backpropagation algorithm (to compute gradients) and some variant of stochastic gradient descent (to take steps to minimize the loss function). However, we don’t quite know how to reliably and efficiently incorporate previous symbolic knowledge (e.g. Physics laws) into neural networks.

There have been research efforts in that direction, such as [Physics-Informed Neural Networks](https://en.wikipedia.org/wiki/Physics-informed_neural_networks) (PINNs), which explicitly use a Physical law (typically a Partial Differential Equation (PDE)) in the loss function to train the neural network. Given that Deep Learning libraries like PyTorch, Tensorflow and JAX, have auto-differentiation routines, PINNs can actually be implemented quite easily and it is a very neat idea. However, these methods have been somewhat disappointing in practice, as they typically don’t provide guarantees on convergence, accuracy or even speed (see [this recent article by Nick McGreivy](https://www.understandingai.org/p/i-got-fooled-by-ai-for-science-hypeheres) for a well-informed critic). The reality is that classical numerical simulation techniques, that rely on discretizations of space and finite-differences approximations, are still state-of-the-art.

In fact these methods are often so good, that if you have enough computational budget to run high-resolution simulations, the data can often be used as “ground truth” to train Machine Learning models.

## 📊 Learning from numerical simulations

The idea of using numerical simulators as the source of high-quality ground truth data for supervised learning (as opposed to real world experimental data) is actually quite widespread. Notable examples in AI for Science, include:

- **Nuclear Fusion** – the work on [controlling plasmas in Tokamaks via deep reinforcement learning](https://deepmind.google/discover/blog/accelerating-fusion-science-through-learned-plasma-control/) relied on numerical simulators of Tokamaks (initially developed at [Swiss Plasma Center](https://www.epfl.ch/research/domains/swiss-plasma-center/research/tcv/) ), and later DeepMind launched a JAX-based simulator called [TORAX](https://arxiv.org/abs/2406.06718) . Simulators were critical for this, because Deep RL needs many interactions between the agent and its environment to learn good control policies. For cost, speed and safety reasons it wouldn’t be possible to do in the real world exclusively.

- **Weather Forecasting** — NVIDIA developed [FourCastNet](https://build.nvidia.com/nvidia/fourcastnet) (Fourier ForeCasting Neural Network), and DeepMind developed its [GraphCast](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/) model — both tackling the problem of global weather forecasting using neural networks. In addition to real world data collected throughout decades, these models also benefit from weather modeling and simulation techniques — that are combined to create “Reanalysis” datasets, such as the [ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5) .

- **Quantum error correction** — DeepMind’s [AlphaQubit](https://blog.google/technology/google-deepmind/alphaqubit-quantum-error-correction/) used a simulator of a quantum computer, and modelled the effects of environmental noise such as heat, vibration, etc on physical qubits. The simulations are used to create a supervised learning dataset to learn the error correction function (predicting the true hidden state of a logical qubit, from noisy observations of a set of physical qubits).

- **Materials discovery** — Microsoft recently announced their breakthrough on [advancing the accuracy of computational chemistry with deep learning](https://www.microsoft.com/en-us/research/blog/breaking-bonds-breaking-ground-advancing-the-accuracy-of-computational-chemistry-with-deep-learning/) . DeepMind had previously announced [the discovery of many potentially interesting materials](https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning/) — this relied on the [Open Quantum Materials Database](https://oqmd.org/) (among others) that use computational expensive [Density Functional Theory](https://en.wikipedia.org/wiki/Density_functional_theory) (DFT) calculations.

It goes without saying, the progress in autonomous driving and robotics has always involved a strong component of simulation. In those cases it is important that models can learn at scale in a cost-effective manner, and that control policies that would be “unsafe” in the real world can be tested out in a simulated environment. For example, even [in 2019 Waymo said that their autonomous driving system had already driven 10 billion miles in simulated environments](https://techcrunch.com/2019/07/10/waymo-has-now-driven-10-billion-autonomous-miles-in-simulation/) .

## 🤔 Are big datasets enough?

Some big players, like Meta, have recently [announced](https://www.facebook.com/AIatMeta/videos/weve-released-open-molecules-2025-omol25-a-new-density-functional-theory-dft-dat/2104414250064455/) the generation of huge datasets for science, such as the [Open Molecules 2025 (OMol25) dataset](https://huggingface.co/facebook/OMol25) . This includes:

- 100M simulations of molecules of up to 350 atoms (small molecules, electrolytes, metal complexes and biomolecules). See the [paper](https://arxiv.org/abs/2505.08762) .

- Again, they rely on Density Functional Theory (DFT) calculations, requiring approximately 6 billion CPU core-hours of compute, which Facebook did on their private data centers, using spare capacity. On a public cloud provider like AWS, GCP or Azure, the cheapest core-hour prices are in the range of 0.5 to 1 cents (using preemptible VMs). Therefore, generating a dataset of this scale would cost something like 30M-60M USD, minimum. And that’s ignoring storage and data transfer costs.

These big datasets will be fundamental to promote research breakthroughs — but the world is very diverse, and there is a virtually infinite amount of scenarios one can be interested in. One dataset can not encompass all aspects of reality, from the small scale to the large scale, to the very custom (e.g. a specific machine in a factory, or a new car design, etc.)

Much like we observe in Language, Computer Vision, Speech, etc — leading research labs create large foundational models that are very generic, but when applied to specific problems they benefit from fine tuning in more problem-specific datasets. In the real world this might be further accentuated by inherent variability of the geometry of objects and their complex physical interactions, at very different scales.

At [Inductiva](https://inductiva.ai/) we believe that in order for AI for the physical world to really flourish, we need to democratize the process of physics dataset generation . In other words, it needs to become much simpler and cheaper to generate a custom physics dataset, for “my problem”.

## 🌐 Democratizing physics datasets generation

In addition to the questions of motivations and incentives — scientists and engineers face a set of purely technical barriers that might hold them back from generating physics datasets for ML:

- Easy access to compute power (e.g. Cloud resources or HPC clusters)

- Complexity of simulator installation, and execution in those environments

- Dealing with storage of large outputs

- Monitoring failures, and re-launching simulations automatically

- Performing post-processing

- Reducing costs, finding the best performant hardware

At [Inductiva](https://inductiva.ai/) , we have built a managed cloud-HPC platform that greatly reduces those barriers, and whose design choices are greatly influenced by the needs and preferences of the AI community. Our Python API naturally blends with the ML toolset (e.g. PyTorch, Tensorflow, JAX), and it brings together [a wide range of open-source numerical simulators](https://inductiva.ai/simulators) , like OpenFOAM, GROMACS, OpenFast, Quantum ESPRESSO, etc, etc.

We have made a strong bet on **open-source** simulators for several reasons:

- There are literally hundreds of high quality numerical simulators, developed over decades by researchers and engineers in Universities, research institutes, etc.

- Many of them were originally developed to run on a single computer or on traditional HPC clusters — and they could greatly benefit from a common Python interface to run on the cloud, making them accessible to a much wider range of users.

- Open-source is awesome! 🙂 History shows that in Operating Systems, mobile platforms, or AI models — there has been a strong tension between closed, proprietary models and open-source versions. Given enough time, the advantages of open-source: the transparency, diversity, decentralization, and the community aspect, tend to be widely appreciated.

For example, we admire what [HuggingFace](https://huggingface.co/) has done for the world of Machine Learning: they have created a flourishing open-source community, sharing datasets and models. We believe that the world of numerical simulation and scientific computing can also greatly benefit from a platform that integrates all the community efforts and gives them a big boost.

Right now, it is so easy to generate large datasets with Inductiva, that it can literally be done with a Python script of about 20 lines of code. If you want to give it a try, have a look at our guide on [how to generate an OpenFOAM dataset](https://inductiva.ai/guides/openfoam/tutorials/generate-wind-tunnel-dataset) .

## 🧩 Scientific Computing meets AI (in many other ways)

In the previous sections we saw how numerical simulation can be used to generate data to train machine learning models, which can sometimes be orders of magnitude faster than the original simulations (e.g. [GraphCast](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/) ). However, the opposite direction is also very promising: Generative AI being used to construct the inputs for simulations. Some examples include:

- **Creating 3D meshes from images** : image to 3D mesh models are able to receive a single image (or even just a text prompt) and convert it into a full blown 3D mesh — the same 3D meshes that CAD engineers use to model their objects (like cars, airplanes, etc). In a collaboration between [CSM.ai](http://csm.ai/) and Inductiva, we showed that you can upload an image, automatically convert it into a 3D object, which Inductiva then inserts into a virtual wind tunnel. The computational fluid dynamics (CFD) simulation is then run by [OpenFOAM](https://inductiva.ai/simulators/openfoam-foundation) , and is capable of estimating the pressure in the surface of the car, as well as the drag coefficient, etc. It is basically “image to CFD”!

- **Creating input config files for simulators** : Large Language Models excel at generating text, including structured text like code in some programming language. It so happens that most numerical simulators take as inputs a set of files, following some formal rules, where the geometry of the problem and a large number of configurable parameters are specified. Numerical simulators commonly require input files that adhere to specific formatting rules. These files define the problem’s geometry and contain a wide array of adjustable parameters. Imagine an engineer could say: “I want to simulate a 60m high off-shore wind turbine with [OpenFAST](https://inductiva.ai/simulators/openfast) , based on the picture I am attaching, under a variety of wind and wave conditions” and the LLM would generate a set of input files, and calls to API (e.g. Inductiva) to run those simulations?

Many other points of interface between classical numerical simulation and Machine Learning are being explored (e.g. numerical algorithms that are optimized by ML techniques to run faster on specific hardware components, agents optimizing engineering workflows, etc). We expect this to be a very active area in the coming years.

## 🎭 Hype vs Reality (as of mid 2025)

If you read up until here, you can notice my enthusiasm for the area at the intersection of simulation and AI — but is all the buzz justified? What is hype and what is reality? Here I would like to make some clarifications, by contrasting specific statements:

**Hype** – “a generic, autonomous AI system will make a breakthrough in my scientific or engineering problem”

**Reality** – “a highly qualified team of Machine Learning engineers and scientists, with access to good quality data, compute power, and enough resources to run ML experiments for several weeks or months — can potentially make a breakthrough in my scientific or engineering problem”

**Hype** – “I will use an out-of-the-box Physics-Informed Neural Network (PINN) to solve your Partial Differential Equation (PDE) thousands of times faster than your numerical solver”

**Reality** – “I will carefully craft a neural network architecture and input representation to encode the geometry of the problem, generate a large dataset of solutions found using a state of the art numerical solver, and devote significant amount of compute to pre-train a neural network, possibly including the PDE in the loss function. If you then use it in inference time, on samples coming from the same distribution as the training data — the prediction will probably have enough accuracy for some practical applications, and will in some cases be orders of magnitude faster”

**Hype** – “We can train a self-driving car or humanoid robot purely on simulated environments and deploy it safely to the real-word”.

**Reality** – “We can use carefully crafted simulators for self-driving cars or humanoid robotics, to greatly reduce the amount of real data needed to train the autonomous system, and safely test new algorithms, “what if scenarios” and failure modes. However, before deploying to the real world, we will still need to fill the “ [sim2real gap](https://www.agilityrobotics.com/content/crossing-sim2real-gap-with-isaaclab) ” with real data and experience, because: 1) simulators use a model of reality that makes simplifying assumptions and don’t include all aspects of reality 2) the simulated data will often follow a distribution that is different from real data distribution, sometimes in subtle ways, and there would be a risk of overfitting to simulation data.”

## 🔮 Conclusion

The future of scientific computing and Physical-AI seems to be bright, but at Inductiva we believe that we need to make a stronger push to bring the two communities together. Developers of numerical simulators often come from fields like Physics, Civil or Mechanical Engineering, and Computational Biology. In contrast, the AI field is largely composed of Computer Scientists, who excel at large-scale machine learning and software systems but typically have less familiarity with physical world modeling. Currently, the separation between these fields could be limiting progress; however, there’s significant enthusiasm for bridging this gap. We recently organized the [Inductiva Machine Learning for Science & Engineering Summer School](https://inductiva.ai/events/machine-learning-summer-school) — and it was awesome! You can see the [recordings](https://www.youtube.com/playlist?list=PLsk2BKvYvK9a210W9VFgKye8_bI1Ewda5) of the open sessions online.

At Inductiva we believe that the missing component has so far been a platform that is appealing for both communities and naturally blends with their workflows. That’s what we have been busy building — [try it for free](https://console.inductiva.ai/) and let us know what you think, we are just getting started!
