# Svg Spatial Sort


Reasonable efficient greedy path planning for plotting svg files.


## Install

Global install (as sudo):


    ./setup.py install


Local install:

    ./setup.py install --user


## Use

    svgsort input.svg output.svg


## Note

Currently the result will probably not have the same scale as the input. I
might fix this but at the moment I recommend checking and re-scaling the result
in eg. Inkscape.

DO NOT USE --reverse. It does not work.


## Todo

 - Handle document sizes
 - Enable reversing of paths/splines/lines

