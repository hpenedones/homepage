# Computer Vision vs Computer Graphics

**Date:** January 28, 2009

**Original URL:** https://aboutintelligence.blogspot.com/2009/01/computer-vision-vs-computer-graphics.html

---

If I had to explain what computer vision is all about, in just one snapshot, I would show you this:  
  
  
[

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNUz9RHEUFcyE791h96sqgew9KDg7kkoWv6vLgYH7H1QIf48Vdcgib0q7_WyUOXNub6gI4PY0lFlvIcPWTCXKNBWjmHmApVhQAjsyb8H60brLuylUjp9EmK6i9fyd5JfURdjgje-QUNvY/s200/computer_vision_graphics.png)

](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNUz9RHEUFcyE791h96sqgew9KDg7kkoWv6vLgYH7H1QIf48Vdcgib0q7_WyUOXNub6gI4PY0lFlvIcPWTCXKNBWjmHmApVhQAjsyb8H60brLuylUjp9EmK6i9fyd5JfURdjgje-QUNvY/s1600-h/computer_vision_graphics.png)  
  
Computer Graphics algorithms go from the parameter space to the image space (rendering), computer vision algorithms do the opposite (inverse-rendering). Because of this, computer vision is basically a (very hard) problem of statistical inference.  
The common approach nowadays is to build a classifier for each kind of object and then search over (part of) the parameter space explicitly, normally by scanning the image for all possible locations and scales. The remaining challenge is still huge: how can a classifier learn and generalize, from a finite set of examples, what are the fundamental characteristics of an object (shape, color) and what is irrelevant (changes in illumination, rotations, translations, occlusions, etc.).  
This is what is keeping us busy! ;)  
  
PS - Note that changes in illumination induce apparent changes in the color of the object and rotations induce apparent changes in shape!