# Svg Spatial Sort


Reasonably efficient greedy path planning for plotting svg files.


## Install

Install locally using:

    ./setup.py install --user

## Use

Use it like this:

    svgsort input.svg out.svg

This will break down paths into continous sub paths. it will also allow
travelling along paths in both directions (but only once).

To ensure every path is drawn twice (once in each direction), you can use

    svgsort input.svg out.svg --repeat

You can disable splitting and reversing using these two options

    svgsort input.svg out.svg --no-split
    svgsort input.svg out.svg --no-reverse

The default behaviour is to fit the result inside the dimensions of an A3 sheet
of paper. It will automatically rotate the paper orientation for the best possible fit.
You can override the paper size this as well. Eg. by doing

    svgsort input.svg out.svg --a4
    svgsort input.svg out.svg --dim=30x40


To see other options, use

    svgsort --help


## CONTRIBUTING

This code is a tool that I have written for my own use. I release it publicly
in case people find it useful. It is not however intended as a
collaboration/Open Source project. As such I am unlikely to accept PRs, reply
to issues, or take requests.

