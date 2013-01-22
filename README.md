idetc-2013-paper
================

The repo for the paper:
Constrained Multibody Dynamics with Python: From Symbolic Equation Generation
to Publication

by
Gilbert Gede, Dale L. Peterson, Angadh Nanjangud, Jason K. Moore


There is a 10 page limit.
LaTeX template: http://www.asme.org/kb/proceedings/proceedings/author-templates
Draft paper info: http://www.asmeconferences.org/IDETC2013/DraftPaperPrep.cfm
Paper types: http://www.asmeconferences.org/IDETC2013/PaperTypes.cfm
Conference website: http://www.asmeconferences.org/IDETC2013

Things to perhaps address:
Motivate the need for streamlining the comprehensive study of a system.
Explain ‘symbolic’ dynamics. People may not know. Reference AutoLev and MotionGenesis. There are probably other packages for motorcycle  dynamics.
Michael Sayers wrote the original code that AutoSim/VehicleSim/BikeSim etc are based on. It is a Kane’s based symbolic manipulator for multibody EoMs.
MBDyn is an example of a numerical open source mutlibody (and flexible i think) dynamics package.
Include a code sample for a problem.
PLoS One software paper guidelines: http://www.plosone.org/static/guidelines#software

-------------
Paper Outline
-------------

* Abstract

* Introduction
    * What do we mean by analytical dynamics?
    * Why do we need a tool for symbolic dynamics?
    * Who benefits from this?
    * What follows in this paper?

* Demonstration Problem
    * What is the problem, and what does it look like?
    * Why did we pick it?
    * How do you (start to) write the problem by hand?
    * What does the code look like to generate the equations of motion?
    * What do the equations look like?
    * What can you do next?
        * Simulate & Visualize
        * Pretty/Latex Printing
    * Workflow for problem
        * sympy.physics.mechanics Code
        * SciPy (or ndsolve code)
        * plotting code
        * visualization code (we could potentially use something like d3.js to have an animation inside the IPython notebook...will take a little more effort, but be badass).
    * Results of problem
        * Plots
        * Example of 3D
    * It’d be pretty cool to have this whole problem in an IPython Notebook that you can easily download and run and play with. This could be included as supplementary materials.

* Software Validation (Why should I trust you?)
    * tests within sympy
        * ensures stability/consistency during development
    * benchmark validations (rolling disc, bicycle, other...)

* Software Design (How does it work?)
    * How do I get it?
        * Download and installation (keep it simple and short)
            * sympy (talk about usefulness and stability of dev branch)
            * basic PyDy tools: i.e. the SciPy stack
            * http://scipy.github.com/install.html
            * http://numfocus.org/projects-2/software-distributions/
    * How do I learn to use it?
        * SymPy Docs for sympy.physics.mechanics
        * PyDy.org for start to finish problems (and accompanying pydyexamples git repo)
    * What is it made of (modules, classes, and functions)?
        * SymPy basics that it uses?? Just a sentence or two. cite Sympy for more info.
        * list or simple figure
        * how about a definition list: name of item + plus sentence or two describing it. A list alone seems like too little info. sure
    * How do these classes interact with each other (probably figures)?
        * ReferenceFrame/Vector & Dyadic interactions (detailing essential.py, visually)
        * ReferenceFrame Tree (how a tree is formed, possible pitfalls)
        * Vector Assemblage (vector is a list of parts of frames and frames - shown visually)
        * Point Tree (similar to RF)
    * How is this translated into equations?
        * container classes (Particle, RigidBody)
        * KanesMethod/LagrangesMethod
            * Describe the classes and their methods, probably a page for each class. At least give the basic understanding of how the classes work.
            * Talk about the methods for constraints and auxiliary speeds.
            * mass matrix
            * cite the paper that Luke and Gilbert wrote about linearization instead of writing about those methods here
            * Explain the form of the EoMs that these methods produce and speak some on solving them for the u dots and the pitfalls associate with that, why it may be better to do it numerically
    * What else can it do?
        * Custom indices for RefereneFrames
    * What can’t it do?
        * problem size limitations - unknown
        * defining problems visually (future problem design a graphical body assembler that builds mechanics code dynamically)
        * fast translation to 3D visualization

* Conclusions
* Acknowledgements
* NSF

