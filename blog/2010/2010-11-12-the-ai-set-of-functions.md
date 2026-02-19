# The AI set of functions

**Date:** November 12, 2010

**Original URL:** https://aboutintelligence.blogspot.com/2010/11/ai-set-of-functions.html

---

I recently read an article from Y. Bengio and Y. LeCun named "Scaling Learning Algorithms to AI". You can also find it as a book chapter in "Large-Scale Kernel Machines"L. Bottou, O. Chapelle, D. DeCoste, J. Weston (eds) MIT Press, 2007.  
  
In some aspects it is an "opinion paper" where the authors advocate for deep learning architectures and their vision of the Machine Learning. However, I think the main message is extremely relevant. I was actually surprised to see how much it agrees with my own opinions.  
Here is how I would summarize it:  
  
- no learning algorithm can be completely universal, due to the "No free lunch theorem"  
- that's not such a big problem: we don't care about the set of all possible functions  
- we care about the "AI set", which contains the functions useful for vision, language, reasoning, etc.  
- we need to create learning algorithms with an inductive bias towards the AI set  
- the models should "efficiently" represent the functions of interest, in terms of having low Kolmogorov complexity  
- researchers have exploited the "smoothness" prior extensively with non-parametric methods. However many manifolds of interest have strong local variations.  
- we need to explore other types of priors, more appropriate to the AI set.  
  
The authors then give examples of two "broad" priors, such as the sharing of weights in convolutional networks (inspired by translation invariance in vision) and the use of multi-layer architectures (which can be seen as levels of increasing abstraction).  
  
Of course here is where many alternatives are open! Many other useful inductive-bias could be found. That's where I think we should focus our research efforts! :)