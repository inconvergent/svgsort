#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""svgsort

Usage:
  svgsort <in> <out> [--split|--split-all] [--reverse] [--rnd]
  svgsort -h

Options:
  --reverse    attempt to reverse path directions
  --split      split paths into continous sub paths
  --split-all  split all paths into primitives
                 (probably not what you want)
  --rnd        random initial position

Examples:
  svgsort input.svg out.svg
  svgsort input.svg out.svg --reverse
"""


__ALL__ = ['Svgsort']

import sys
import traceback

from svgsort.svgsort import Svgsort


VERBOSE = True



def run():

  from docopt import docopt
  args = docopt(__doc__, version='svgsort 0.0.2')
  main(args)


def main(args):

  try:
    _in = args['<in>']
    out = args['<out>']
    reverse = args['--reverse']

    svgs = Svgsort().load(_in, verbose=VERBOSE)

    if args['--split-all']:
      svgs.eager_split()
    if args['--split']:
      svgs.split()
    svgs.sort(reverse, rnd=args['--rnd'], verbose=VERBOSE).save(out)

    print('wrote: ', out)
  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)



if __name__ == '__main__':
  run()

