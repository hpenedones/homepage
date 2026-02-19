# Vapnik's picture explained

**Date:** January 28, 2009

**Original URL:** https://aboutintelligence.blogspot.com/2009/01/vapniks-picture-explained.html

---

[

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNsDKM24TbhSTujsJBpQ5Mk4a0SN6q1Me0uC7LT4FYIvaXIc4L5kH4oaeKVN1xkJmR2LxKWaM8TaDta6UG_cxSpF63Fzk85rUH34nan_e6sfSpizIXrxlVCV353ZYdHWdzl0YQNzyIjds/s320/vapnik.jpg)

](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNsDKM24TbhSTujsJBpQ5Mk4a0SN6q1Me0uC7LT4FYIvaXIc4L5kH4oaeKVN1xkJmR2LxKWaM8TaDta6UG_cxSpF63Fzk85rUH34nan_e6sfSpizIXrxlVCV353ZYdHWdzl0YQNzyIjds/s1600-h/vapnik.jpg)  
  
This is an extremely geek picture! :) Let's try to explain it:  
  
First of all, as many of you know, the gentleman in the picture is [Prof. Vladimir Vapnik](http://www.ccls.columbia.edu/Vapnik-Bio.html). He is famous for his fundamental contributions to the field of Statistical Learning Theory, such as the Empirical Risk Minimization (ERM) principle, VC-dimension and Support Vector Machines.  
  
Then we notice the sentence in the board: it resembles the famous "[All your base are belong to us](http://en.wikipedia.org/wiki/All_your_base_are_belong_to_us)"! This is a piece of geek culture that emerged after a "broken English" translation of a Japanese video game for Sega Mega Drive .  
  
[

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg1zC1k8Ig3Ml-peEqqIU_WKPyKCwYo4bfbnGG-7w7M5t_AaDqVXeAlUPn15rknDZPs3p3P-5uc4m4El-gNgNlJMXPWKwyifYNZQqQK_sNHEnlMWlasI8YVRCUCVQjgA_UXa_E31MhnVTY/s320/Aybabtu.png)

](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg1zC1k8Ig3Ml-peEqqIU_WKPyKCwYo4bfbnGG-7w7M5t_AaDqVXeAlUPn15rknDZPs3p3P-5uc4m4El-gNgNlJMXPWKwyifYNZQqQK_sNHEnlMWlasI8YVRCUCVQjgA_UXa_E31MhnVTY/s1600-h/Aybabtu.png)  
  
Wait, but they replaced the word "Base" by "Bayes"!?  
Yes, that [Bayes](http://en.wikipedia.org/wiki/Thomas_Bayes), the British mathematician known for the [Bayes' theorem](http://en.wikipedia.org/wiki/Bayes%27_theorem).  
Okay, seems fair enough, we are dealing with people from statistics...  
  
By the moment we think things can not get more geeky, we realize there is scary inequality written on the top of the white board:  
  
[

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg9A35AsgbtagiWfcACvF2Y6qGi1A88kB8jaaOzQBTHXEjMm1bMrgGbaeUNWsQYQVWF4YMQOlYxEwx0CfdU4msf12qXuJvq-Ezae11pRgO7zbgwEeVdDMvuhm-PxyUh1RBbtVXORDcVt5U/s400/bound.png)

](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg9A35AsgbtagiWfcACvF2Y6qGi1A88kB8jaaOzQBTHXEjMm1bMrgGbaeUNWsQYQVWF4YMQOlYxEwx0CfdU4msf12qXuJvq-Ezae11pRgO7zbgwEeVdDMvuhm-PxyUh1RBbtVXORDcVt5U/s1600-h/bound.png)My goodness, what's this?! Okay, that's when things get really technical:  
This is a probabilistic bound for the expected risk of a classifier under the ERM framework. In simple terms, it relates the classifier's expected test error with the training error on a dataset of size l and in which the cardinality of the set of loss functions is N.  
If I'm not mistaken, the bound holds with probability (1 - eta) and applies only to loss functions bounded above by 1.  
  
Sweet! Now that we got the parts, what's the big message?  
  
Well, it's basically a statement about the superiority of Vapnik's learning theory over the Bayesian alternative. In a nutshell, the Bayesian perspective is that we start with some prior distribution over a set of hypothesis (our beliefs) and we update these according to the data that we see. We then look for an optimal decision rule based on the posterior distribution.  
On the other hand, in Vapnik's framework there are no explicit priors neither we try to estimate the probability distribution of the data. This is motivated by the fact that density estimation is a [ill-posed](http://en.wikipedia.org/wiki/Ill-posed) problem, and therefore we want to avoid this intermediate step. The goal is to directly minimize the probability of making bad decision in the future. If implemented through [Support Vector Machines](http://en.wikipedia.org/wiki/Support_vector_machine), this boils down to finding the decision boundary with maximal margin to separate the classes.  
  
And that's it, folks! I hope you had fun decoding this image! :)