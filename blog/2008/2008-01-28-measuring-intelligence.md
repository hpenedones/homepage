# Measuring Intelligence

**Date:** January 28, 2008

**Original URL:** https://aboutintelligence.blogspot.com/2008/01/measuring-intelligence.html

---

In order to develop artificial intelligence further, it would be important to have a formal and quantitative way to measure intelligence of an agent, being it a human or a machine.  
The most famous test for artificial intelligence is the so-called [Turing Test](http://en.wikipedia.org/wiki/Turing_test), in which "a human judge engages in a natural language conversation with one human and one machine, each of which try to appear human; if the judge cannot reliably tell which is which, then the machine is said to pass the test". There is even a competition, the [Loebner Prize](https://en.wikipedia.org/wiki/Loebner_Prize) which really evaluates different chatbots and choses the one who most resembles a human. However, this test is nowadays considered to be anthropomorphically biased, because an agent can be intelligent and still not be able to respond exactly like a human. Marcus Hutter as recently proposed a new way of measuring intelligence, based on the concepts of Kolmogorov Complexity and Minimum Description Length, in which compression = learning = intelligence. The [Hutter Prize](https://en.wikipedia.org/wiki/Hutter_Prize) measures how much one can compress the first 100MB of wikipedia. The idea is that intelligence is the ability to detect patterns and make predictions, which in turn allows one to compress data a lot.  
In my opinion this is not yet a totally satisfactory way of measuring general intelligence, for at least two reasons:  
- the fact that method A compressed the dataset more than method B, does not necessarily mean that method A is more intelligent. It may simply mean that the developer of the method exploited some characteristic of the (previously known) data. Or it can mean that the method is good to find regularities in such dataset, but not being able to learn other structures in other environments.  
- it can not be applied to humans (or animals).  

For these reasons, I guess measuring intelligence is still a fundamental open problem in AI.