# Svg Spatial Sort


Reasonably efficient greedy path planning for plotting svg files.


## Install

Install locally using:

    ./setup.py install --user

## Use

Some examples of use:

    svgsort input.svg output.svg
    svgsort input.svg out.svg
    svgsort input.svg out.svg --dim=30x40
    svgsort input.svg out.svg --a3
    svgsort input.svg out.svg --repeat

This will break down paths into continous sub paths. it will also allow
travelling along paths in both directions (but only once).

You can override this using these two options

    svgsort input.svg out.svg --no-split
    svgsort input.svg out.svg --no-reverse

The default behaviour is to fit the result inside the dimensions of an A4 sheet
of paper. You can override this as well. To see the options, use

    svgsort --help

