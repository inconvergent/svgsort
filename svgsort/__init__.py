#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""svgsort

Usage:
  svgsort <in> [<out>] [--no-split | --split-all]
                       [--no-reverse]
                       [--a4 | --a3 | --dim=<d>]
                       [--pad-abs]
                       [--pad=<p>]
                       [--sw=<s>]
                       [--rnd] [--repeat]
                       [--nv]
  svgsort <in> [<out>] --no-sort [--a4 | --a3 | --dim=<d>]
                                 [--pad-abs]
                                 [--pad=<p>]
                                 [--sw=<s>]
                                 [--repeat]
                                 [--nv]

Options:
  --no-reverse  DO NOT attempt to reverse path directions.
                  (by default it will attempt to reverse paths.)
  --no-split    DO NOT split paths into continous sub paths.
                  (by default it will split.)
  --no-sort    DO NOT sort paths
  --split-all   split all paths into primitives.
                  (probably not what you want.)
  --a4          center on an A4 paper with some padding.
  --a3          center on an A3 paper with some padding (default).
  --dim=<d>     center inside these dimensions (millimeters). eg. d=(100x200).
  --rnd         random initial position.
  --repeat      repeat every path, and draw it in the opposite direction.
  --pad=p       padding in percentage of shortest side [default: 0.01].
  --pad-abs     if this flag is used, the padding is an absolute value
                  in the same units as the initial svg width/height properties.
  --sw=s        stroke width.
  --nv          not verbose. (verbose is default.)

  -h --help   show this screen.
  --version   show version.

Examples:
  svgsort input.svg
  svgsort input.svg out.svg
  svgsort input.svg out.svg --dim=30x40
  svgsort input.svg out.svg --a4
  svgsort input.svg out.svg --repeat
"""


__ALL__ = ['Svgsort']

import sys
import traceback

from docopt import docopt

from svgsort.svgsort import Svgsort
from svgsort.svgsort import PAPER
from svgsort.svgsort import make_paper



def main():
  args = docopt(__doc__, version='svgsort 2.0.0')
  try:
    _in = args['<in>']
    out = args['<out>'] if args['<out>'] else args['<in>']+'-srt'
    reverse = not args['--no-reverse']
    verbose = not args['--nv']

    svgs = Svgsort(verbose=verbose).load(_in)

    if args['--no-split']:
      pass
    elif args['--split-all']:
      svgs.eager_split()
    else:
      # default
      svgs.split()

    if args['--no-sort']:
      # do not sort
      res = svgs
    else:
      res = svgs.sort(reverse, rnd=args['--rnd'])

    if args['--repeat']:
      res.repeat()

    # default
    paper = PAPER['a3']
    if args['--a4']:
      paper = PAPER['a4']
    elif args['--dim']:
      paper = make_paper(tuple([int(d) for d in args['--dim'].split('x')]))

    res.save(out,
             paper=paper,
             pad=float(args['--pad']),
             padAbs=bool(args['--pad-abs']),
             sw=args['--sw'])

    print('wrote: ', out)

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)


if __name__ == '__main__':
  main()

