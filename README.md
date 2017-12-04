# Svg Spatial Sort


Reasonably efficient greedy path planning for plotting svg files.


## Install

Global install (as sudo):


    ./setup.py install


Local install:

    ./setup.py install --user


## Use

    svgsort input.svg output.svg

Your best bet is probably

    svgsort input.svg output.svg --split --reverse

This will break down paths into continous sub paths. it will also allow
travelling along paths in both directions (but only once).

For other options, see:

    svgsort --help


## Note

Currently the result will probably not have the same scale as the input. I
might fix this but at the moment I recommend checking and re-scaling the result
in eg. Inkscape.

