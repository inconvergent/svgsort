#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""svgsort

Usage:
  svgsort <in> <out> [--no-split | --split-all]
                     [--no-reverse]
                     [--a4 | --a3 | --c | --dim=<d>]
                     [--pad=<p>]
                     [--sw=<s>]
                     [--rnd] [--repeat]
                     [--nv]
  svgsort -h

Options:
  --no-reverse  DO NOT attempt to reverse path directions.
                  (by default it will attempt to reverse paths.)
  --no-split    DO NOT split paths into continous sub paths.
                  (by default it will split.)
  --split-all   split all paths into primitives.
                  (probably not what you want.)
  --c           center canvas on the drawing.
  --a4          center on an A4 paper with some padding (default).
  --a3          center on an A3 paper with some padding.
  --dim=<d>     center inside these dimensions in mm. eg. d=(100x200).
  --rnd         random initial position.
  --repeat      repeat every path, and draw it in the opposite direction.
  --pad=p       padding. in percent of shortest side [default: 0.01].
  --sw=s        stroke width.
  --nv          not verbose. (verbose is default.)

Examples:
  svgsort input.svg out.svg
  svgsort input.svg out.svg --dim=30x40
  svgsort input.svg out.svg --a3
  svgsort input.svg out.svg --repeat
"""


__ALL__ = ['Svgsort']

import sys
import traceback

from svgsort.svgsort import Svgsort
from svgsort.svgsort import PAPER
from svgsort.svgsort import make_paper



def run():

  from docopt import docopt
  args = docopt(__doc__, version='svgsort 1.0.0')
  main(args)

  # import cProfile
  # cProfile.runctx('main(args)', globals(), locals(), '/tmp/prof')
  # import pstats
  # p = pstats.Stats('/tmp/prof')
  # p.sort_stats('cumulative').print_stats()


def main(args):
  # print(args)
  try:
    _in = args['<in>']
    out = args['<out>']
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

    res = svgs.sort(reverse, rnd=args['--rnd'])

    if args['--repeat']:
      res.repeat()

    paper = None
    if args['--dim']:
      paper = make_paper(tuple([int(d) for d in args['--dim'].split('x')]))
    elif args['--a3']:
      paper = PAPER['a3']
    elif not args['--c']:
      # default
      paper = PAPER['a4']

    res.save(out, paper=paper, pad=float(args['--pad']), sw=args['--sw'])

    print('wrote: ', out)

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)


if __name__ == '__main__':
  run()

