# Svg Spatial Sort


Reasonably efficient, greedy, path planning for plotting svg files.


## Install

Install locally using:

    ./setup.py [install | develop] --user


## Use

Use from the terminal like this:

    svgsort input.svg out.svg

This will break down paths into continous sub paths before sorting. it will
also allow travelling along paths (once) in both directions.

The default behaviour is to fit the result into an A3 sheet of paper. It will
automatically rotate the paper orientation for the best possible fit, as well
as align the drawing to the center. You can override the paper size by using
`--dim=A4` or, eg., `--dim=30x40`. To disable centering entirely use
`--no-adjust`.

To ensure every path is drawn twice (once in each direction), you can use
`--repeat`

You can disable splitting with `--no-split`. To see other options:

    svgsort --help


## Credits

The code in `svgsort/svgpaththools` is from
https://github.com/mathandy/svgpathtools. With only minor changes by me. I had
a number of strange issues when installing it via `pip`, so I decided to
include it here. See the LICENSE file.


## Todo

Strip out larger parts of svgpathtools, and refactor?


## Contributing

This code is a tool for my own use. I release it publicly in case people find
it useful. It is not however intended as a collaboration/Open Source project.
As such I am unlikely to accept PRs, reply to issues, or take requests.

