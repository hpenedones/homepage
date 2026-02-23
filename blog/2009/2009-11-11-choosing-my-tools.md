# Choosing my tools

**Date:** November 11, 2009

**Original URL:** https://aboutintelligence.blogspot.com/2009/11/choosing-my-tools.html

---

I'm doing research in the fields of Machine Learning and Computer Vision, so each time we have an idea for a new algorithm, I have to write code, run experiments and compare results. I have realized that the experimental part is really the bottleneck, we have more ideas than we can test. For this reason, it's critical to chose a good set of tools you can work with. This is a list of my current choices, but I am continuously looking for more efficient tools.

**Operating system:**

[Snow Leopard](https://en.wikipedia.org/wiki/Mac_OS_X_Snow_Leopard) - In my opinion, Mac OS X has an excellent balance between control and usability. You have beautiful graphical interfaces, that just work, but still have a fully functional Unix shell.

**Update:** Lately my preference is to use [Ubuntu Linux](http://www.ubuntu.com/) because I have much fewer problems with apt-get than with macports. Sometimes, professionally I also use Windows. It seems that is hard to stick to one OS, when you change project, job, etc.

**Text Editor / Programming Environment:**

[Textmate](http://macromates.com/) - again, it's an excellent compromise between simplicity, usability and customizability. You can create your own code snippets (using shell commands, ruby, python and more), but to me it seems much easier to learn than vim or emacs.

**Update:** Again, went back to the basics, and started using [vim](http://www.vim.org/) and gvim. It is available in all the platforms, there is a much bigger user base and I really like the power of the command mode. In addition, recently I learnt how to write simple vi plugins using python, which literally means I can do whatever I want with my editor.

**Programming Language:**

[C++](http://en.wikipedia.org/wiki/C%2B%2B) - absolute power. So powerful that one must be very careful using it. [Some people say](http://en.wikipedia.org/wiki/Scott_Meyers), C++ is actually a federation of languages, which includes C, object oriented stuff, templates and standard libraries. Although I've been using it for while, I feel there is always more to learn about it.

**Update:** In addition to C++ (and C which I really love), I also started using some scripting languages. First I learnt Lua, so that I could use the [Torch](http://www.torch.ch/) Machine Learning Library. Then, I started using python, which I really love due to the wide availability of (easily installable) libraries. Ah, I look forward to learn the new C++11 standard, which seems to be quite neat.

**Build System (new):**

[cmake](http://www.cmake.org/) - it's cross platform and simple enough to start using it. I don't know the advanced features, but it's pretty easy to create a project that generates libraries and executables and links properly with other dependencies (like OpenCV).

**Source control system:**

[git](http://git-scm.com/) - I was using [subversion](https://en.wikipedia.org/wiki/Apache_Subversion) before, but I guess the idea of distributed repositories makes sense. You can work locally and still commit changes that you can synchronize later. So far, I use less than 2% of the commands!

**Update:** git is definitely here to stay. Now I use private and public hosted repositories with Github or Bitbucket.

**Cloud Computing (new):**

[Amazon EC2](http://aws.amazon.com/) - I also used the IBM Smart Cloud, but Amazon has more features and better APIs. Recently, with the introduction of the spot instances, things also got a lot cheaper when you need to process large amounts of data.

**NoSQL Databases (new):**

[redis](http://redis.io/) - redis is what we can call a "data structure server" and it's probably the nicest piece of software I started using recently. It is just beautiful. Simple. Intuitive. Fast. I can not recommend it enough.

**Computer Vision Library:**

[OpenCV](https://opencv.org/) - it's quite useful for the low and intermediate level things (load and save images, convert color spaces, edge detection, SURF descriptors etc.). It also has higher level algorithms, but when you're doing research in the field, these are not so useful. It lacks some object-oriented design, but version 2.0 is starting to move in that direction.

**Machine Learning library:**

None. Here I'm re-inventing the wheel, because I want to know everything about wheels. I do my own implementations of AdaBoost, EM algorithm, Kmeans and stuff like that. See my C++ code at: https://github.com/hpenedones/lakeml

**Object Serialization Library:**

[boost-serialization](http://www.boost.org/doc/libs/release/libs/serialization/) - I need to save the models to files in order to load them later. If I were using OpenCV for Machine Learning, I could also use the functions they provide for serialization, but I'm not. With boost I can serialize objects to xml or binary format. It's a bit tricky to use, because it uses C++ templates and when you have compile time errors it's really hard to understand why. I'm not specially happy with this choice, but once you get your code right, it works pretty well.

**Debugging:**

[gdb](http://www.gnu.org/software/gdb/) - pretty much of a standard. I haven't yet chosen an interface for it... Maybe I don't even need one. I find [ddd](http://www.gnu.org/software/ddd/) look and feel really horrible! Maybe I will start using [xcode](https://developer.apple.com/xcode/) interface to gdb for debugging. Not sure. Actually, 90% of the times I will identify the bug by making some prints and looking at the code, so I don't even run gdb.

**Static code analysis:**

[cppcheck](http://sourceforge.net/apps/mediawiki/cppcheck/index.php?title=Main_Page) - this is a recent choice, but it seems to give some useful alerts.

**Run-time code analysis:**

[valgrind](http://valgrind.org/) - I'm not using it regularly yet, but it's on top of my priorities. This should be the ultimate tool to help you find memory leaks in your code. I didn't manage to install it in snow leopard, which can actually lead me to downgrade to leopard. Have to think about it.

**Plotting:**

[gnuplot](http://www.gnuplot.info/) - really powerful and configurable. This one is a safe bet, although I heard there is nice python software as well.

**Image Processing:**

[ImageMagick](http://www.imagemagick.org/) (convert command) - good to resize pictures, convert colors, etc. I mean, from the shell, this is not to replace [gimp](http://www.gimp.org/) or the like.

**Video Processing:**

Here I should be using [mplayer / mencoder](http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.html) from the command line, but again I still have to solve some compatibility problems with snow leopard. [ffmpeg](http://ffmpeg.org/) is also useful.

**Terminal multiplexer:**

[screen](http://www.gnu.org/software/screen/) - sometimes one needs to run experiments remotely, and you want your processes to continue running smoothly when you log off. Use screen for this.

**Screen sharing:**

[synergy](http://synergy2.sourceforge.net/) - I work directly on my macbook and I connect another screen to it. However, I also want to interact with my linux desktop at work. I use synergy to have an extended desktop, share the mouse and the keyboard across different computers over the network. It's really cool!

**Automated backups:**

[Time Machine](https://en.wikipedia.org/wiki/Time_Machine_(macOS)) - I have an external hardisk which backs up pretty much everything automatically when I connect it to my macbook. Things in my desktop are backed up by a central procedure implemented in [my research institute](http://www.idiap.ch/).

**Update:** I still use Time Machine in one computer, but now I rely more on cloud storage. I use Google Drive for some documents, PicasaWeb for pictures and use either Github or Bitbucket for source code or latex papers.

**Shell tools:**

cat, head, tail, cut, tr, grep, sort, uniq.... sometimes sed and awk... I mostly use this to manipulate data files before feeding them to gnuplot and make some graphics.

**Document preparation system:**

[latex](http://www.latex-project.org/) - this is the standard in the scientific community and there are good reasons for that. [bibtex](http://www.bibtex.org/) - to do proper citations to other people's articles or books.

**Source code documentation:**

[doxygen](http://www.doxygen.org/) - I don't really develop libraries for other people to use, but generating documentation automatically from your source code can help you improve it. If you use doxygen with [graphviz](http://www.graphviz.org/) you can for example see the class hierarchies and dependencies of your code.

What tools do you use? Do you have any recommendations for me? I guess that the OS, editor and programming language are the most polemic! But, what about the others? Any ideas?