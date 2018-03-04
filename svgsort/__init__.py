#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""svgsort

Usage:
  svgsort <in> <out> [--sw=<s>] [--split|--split-all] [--reverse]
                     [--rnd] [--repeat] [-nv]
  svgsort --center <in> <out> [--nv]
  svgsort -h

Options:
  --reverse    attempt to reverse path directions.
  --split      split paths into continous sub paths.
  --split-all  split all paths into primitives
                 (probably not what you want).
  --center     center drawing on the canvas (does not sort).
  --rnd        random initial position.
  --repeat     repeat every path, and draw it in the opposite direction.
  --sw=s       stroke width.
  --nv         not verbose. it is verbose by default.

Examples:
  svgsort input.svg out.svg
  svgsort input.svg out.svg --split --reverse
"""


__ALL__ = ['Svgsort']

import sys
import traceback

from svgsort.svgsort import Svgsort



def run():

  from docopt import docopt
  args = docopt(__doc__, version='svgsort 0.0.3')
  main(args)


def main(args):

  try:
    _in = args['<in>']
    out = args['<out>']
    reverse = args['--reverse']
    verbose = not args['--nv']

    svgs = Svgsort(verbose=verbose).load(_in)

    if args['--split-all']:
      svgs.eager_split()
    if args['--split']:
      svgs.split()

    if args['--center']:
      # this option does not sort
      res = svgs
    else:
      res = svgs.sort(reverse, rnd=args['--rnd'])

    if args['--repeat']:
      res.repeat()

    res.save(out, sw=args['--sw'])

    print('wrote: ', out)

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)


if __name__ == '__main__':
  run()

