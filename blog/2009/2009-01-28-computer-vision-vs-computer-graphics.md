# Computer Vision vs Computer Graphics

**Date:** January 28, 2009

**Original URL:** https://aboutintelligence.blogspot.com/2009/01/computer-vision-vs-computer-graphics.html

---

If I had to explain what computer vision is all about, in just one snapshot, I would show you this:  
  
  
[

![](/images/blogger-AVvXsEhNUz9RHEUF-computer_vision_graphics.png)

](/images/blogger-AVvXsEhNUz9RHEUF-computer_vision_graphics.png)  
  
Computer Graphics algorithms go from the parameter space to the image space (rendering), computer vision algorithms do the opposite (inverse-rendering). Because of this, computer vision is basically a (very hard) problem of statistical inference.  
The common approach nowadays is to build a classifier for each kind of object and then search over (part of) the parameter space explicitly, normally by scanning the image for all possible locations and scales. The remaining challenge is still huge: how can a classifier learn and generalize, from a finite set of examples, what are the fundamental characteristics of an object (shape, color) and what is irrelevant (changes in illumination, rotations, translations, occlusions, etc.).  
This is what is keeping us busy! ;)  
  
PS - Note that changes in illumination induce apparent changes in the color of the object and rotations induce apparent changes in shape!