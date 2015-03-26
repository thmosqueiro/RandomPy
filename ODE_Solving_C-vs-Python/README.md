ODE Solving - C vs Python
=====

Depending on the application, solving ODE may require quite complex
techniques and ellaborate numerical methods. Especially for stiff
problems. I wanted to compare two implementations of the Lorentz
system tuned into parameters that show the famous butterfly strange
attractor.

The idea, however, is not to compare an ODE integration in C against
its counterpart in python - C obviously outperforms python. What I
wanted to test (and keep track of) is how efficient are some of the
libraries python offers to solve ODEs.

The C implementation uses the (in)famous CVODE from Sundials. For now,
with python I'm only testing scipy's ode function.

This is still in very early stage. If you feel you may contribute,
please feel free to do so! I also want to test a stiff problem in the
near future.


Tests
------

I'll keep a simple record of how C and python are doing. Below are the
last results.

* Intel(R) Core(TM) i7 CPU 970 @ 3.20GHz *
* Fedora 21, kernel 3.19.1-201.fc21.x86_64 *

C:      0.519s
Python: 3.96s



License
------

Everything in this repository is under the WTFLP, which reads as follows.

```
	     DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.
```

**tl;dr** version: use it as you please, just don't sue me.
