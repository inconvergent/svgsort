#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn <in> <out>
  fn -h

Examples:

  fn input.svg             Process this file
  -h                       Show this screen.
  --version                Show version.
"""


__ALL__ = ['Fn']

from svgsort.svgsort import Svgsort



def run():

  from docopt import docopt
  args = docopt(__doc__, version='svgsort 0.1.1')
  main(args)


def main(args):

  from sys import stderr

  print(args)

  try:

    fn = args['<in>']
    res = args['<out>']
    s = Svgsort().load(fn).sort().save(res)
    # s = Svgsort().load(fn).save(res)

    print('wrote: ', res)

  except Exception as e:
    print(e, file=stderr)
    # from traceback import print_exc
    # print_exc(file=stderr)
    exit(1)


if __name__ == '__main__':
  run()

