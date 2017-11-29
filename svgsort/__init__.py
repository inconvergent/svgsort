#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""svgsort

Usage:
  fn <in> <out>
  fn -h

Examples:

  fn input.svg out.svg     Process input.svg and write to out.svg
  -h                       Show this screen.
  --version                Show version.
"""


__ALL__ = ['Svgsort']

import sys
import traceback

from svgsort.svgsort import Svgsort




def run():

  from docopt import docopt
  args = docopt(__doc__, version='svgsort 0.0.1')
  main(args)


def main(args):


  try:

    fn = args['<in>']
    res = args['<out>']
    Svgsort().load(fn).sort().save(res)
    print('wrote: ', res)

  except Exception:
    traceback.print_exc(file=sys.stdout)
    exit(1)

if __name__ == '__main__':
  run()

