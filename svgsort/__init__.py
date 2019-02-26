#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""svgsort

Usage:
  svgsort <in> [<out>] [--no-split | --split-all]
                       [--dim=<d>]
                       [--pad-abs]
                       [--pad=<p>]
                       [--pen-moves]
                       [--sw=<s>]
                       [--rnd] [--repeat]
  svgsort <in> [<out>] --no-adjust [--no-split | --split-all]
                                   [--pen-moves]
                                   [--sw=<s>]
                                   [--rnd] [--repeat]
  svgsort <in> [<out>] --no-sort [--dim=<d>]
                                 [--pad-abs]
                                 [--pad=<p>]
                                 [--pen-moves]
                                 [--sw=<s>]
                                 [--rnd] [--repeat]

Options:
  --no-split    do not split paths into continous sub paths.
                (by default it will split.)

  --no-adjust   do not change paper layout. experimental.
  --no-sort     do not sort paths.

  --pen-moves   draw pen moves in red. to see sort result.

  --dim=<d>     paper size. use A4, A3 (default), or eg. 100x200.
                in the latter case the unit is in millmeters [default: A3].

  --pad=<p>     padding in percentage of shortest side [default: 0.01].
  --pad-abs     if this flag is used, the padding is an absolute value
                in the same units as the initial svg width/height properties.

  --repeat      repeat every path, and draw it in the opposite direction.

  --sw=<s>      stroke width [default: 1.0].

  --split-all   split all paths into primitives. (probably not what you want.)

  --rnd         random initial position.

  -h --help   show this screen.
  --version   show version.

Examples:
  svgsort input.svg
  svgsort input.svg out.svg
  svgsort input.svg out.svg --dim=30x40
  svgsort input.svg out.svg --dim=A4
  svgsort input.svg out.svg --repeat
"""


__ALL__ = ['Svgsort']

import sys
import traceback

from docopt import docopt

from .svgsort import Svgsort
from .paper_utils import PAPER
from .paper_utils import make_paper



def main():
  args = docopt(__doc__, version='svgsort 3.0.0')
  try:
    _in = args['<in>']
    out = args['<out>'] if args['<out>'] else args['<in>']+'-srt'
    adjust = not args['--no-adjust']
    penmoves = args['--pen-moves']

    svgs = Svgsort(sw=args['--sw']).load(_in)

    if args['--no-split']:
      pass
    elif args['--split-all']:
      svgs.eager_split()
    else:
      # default
      svgs.split()

    if args['--no-sort']:
      # do not sort
      pass
    else:
      svgs.sort(rnd=args['--rnd'])

    if args['--repeat']:
      svgs.repeat()

    if penmoves:
      svgs.make_pen_move_paths()

    dim = args['--dim'].strip().lower()
    paper = PAPER.get(dim, None)
    if paper is None:
      try:
        paper = make_paper(tuple([int(d) for d in args['--dim'].split('x')]))
      except Exception:
        raise ValueError('wrong dim/paper size')

    if adjust:
      svgs.save(out, paper=paper, pad=float(args['--pad']),
                padAbs=bool(args['--pad-abs']))
    else:
      svgs.save_no_adjust(out)

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)


if __name__ == '__main__':
  main()

