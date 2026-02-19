# Gmail Machine Learning

**Date:** October 14, 2009

**Original URL:** https://aboutintelligence.blogspot.com/2009/10/gmail-machine-learning.html

---

I just quickly tried the new Gmail Labs feature "Got the wrong Bob"? and it actually works quite nicely! I put some email addresses of family members, followed by the address of an old professor, who has the same first name of one of my cousins, and... Gmail found it! :) It suggested right way to change to the correct person, based on context!The other new feature, called "Don't forget Bob", is probably simpler, but quite useful as well. As I typed names of some close friends, I got more suggestions of friends I often email jointly with the previous ones.I wonder if the models to run this feature are very complicated. Probably they are not. I guess one just has to estimate the probability of each email address in our contacts to appear in the "To:" field, given the addresses we have already typed. To estimate these, you just have to use a frequentist approach and count how many times this happened in the past. With this in hands, "Got the wrong Bob?" will notice unlikely email addresses and "Don't forget Bob" will suggest likely ones that are missing.  
  
I think it's a really cool idea, in the same spirit of "Forgotten Attachement Detector". A bit of machine learning helping daily life!