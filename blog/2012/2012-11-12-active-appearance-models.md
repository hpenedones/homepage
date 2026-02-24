# Active Appearance Models

**Date:** November 12, 2012

**Original URL:** https://aboutintelligence.blogspot.com/2012/11/active-appearance-models.html

---

Lately, I have been working with Deformable Models and I am surprised by how well they can work.

<iframe width="560" height="315" src="https://www.blogger.com/video.g?token=AD6v5dyi_BHZNkMU3IMKgIsDJRhH4x2AySZf0wCJrXl0Xjw4kug2cf9tdpTBt4bFCXp8ZeokYU0iBomKwQwtsHhI1-zs3oDFj4g-597b6C4tApj_KUJ1didxF7laJDhJOWn0FdIoG6Qq" frameborder="0" allowfullscreen title="Active Appearance Models face tracking demo"></iframe>

In the video above I am using an Inverse Compositional Active Appearance Model, which was trained with images of myself. It's specially tuned for my face, but I still find it quite impressive how well it can track my face in realtime!  
 On the other hand, this model is quite sensitive to lighting conditions and partial occlusions. Training it, is also somehow of an art, because, as opposed to discriminative models, increasing the amount of training data might actually decrease performance. This happens because we use PCA to learn the linear models of shape and texture, which will degrade if data has too much variation or noise.  
 Still, it's quite impressive what one can achieve by annotating a few images (about 50, in this case). In addition, as one annotates images, one can start training models that will help us landmark the next ones (in a process of "bootstrapping", similar to the one in compilers).