# -*- coding: utf-8 -*-

from os import getcwd
from os.path import sep

from copy import deepcopy

from svgpathtools import Path

from numpy.random import random
from numpy import array

from svgpathtools import svg2paths2
from svgpathtools import wsvg

from svgsort.utils import attempt_reverse
from svgsort.utils import flip_reorder
from svgsort.utils import get_cont_paths
from svgsort.utils import get_length
from svgsort.utils import get_sort_order
from svgsort.utils import reorder
from svgsort.utils import split_all

LARGE = 1e10

def bbox(paths):

  xmin, xmax, ymin, ymax = paths[0].bbox()

  for p in paths:
    xmi, xma, ymi, yma = p.bbox()
    xmin = min(xmin, xmi)
    xmax = max(xmax, xma)
    ymin = min(ymin, ymi)
    ymax = max(ymax, yma)

  return xmin, xmax, ymin, ymax

def get_init_pos(bb, rnd):
  xmin, xmax, ymin, ymax = bb

  if rnd:
    return array([
        xmin + random()*(xmax-xmin),
        ymin + random()*(ymax-ymin)])
  return array([0, 0], 'float')


class Svgsort():
  def __init__(self):
    self.cwd = getcwd()
    self.paths = None
    self.attributes = None
    self.initial_length = -1

    self.stroke_width = 1.0
    self.stroke = 'black'

    self.bbox = None

  def load(self, fn, verbose=False):
    paths, _, vals = svg2paths2(self.cwd + sep + fn)
    self.paths = paths

    length, pen_length = get_length(paths)
    self.initial_length = length
    self.bbox = bbox(paths)
    if verbose:
      print('initial:')
      print('--number of paths: {:d}'.format(len(paths)))
      print('--total path length: {:0.2f}\n--pen move ratio: {:0.2f}'\
          .format(length, pen_length/length))
      print('--bbox', self.bbox)

    return self

  def split(self):
    print('splitting paths:')
    self.paths = list(get_cont_paths(self.paths))
    print('--number of new paths: {:d}'.format(len(self.paths)))
    return self

  def eager_split(self):
    print('splitting into primitives:')
    self.paths = list(split_all(list(get_cont_paths(self.paths))))
    print('--number of new paths (primitives): {:d}'.format(len(self.paths)))
    return self

  def save(self, fn):
    atr = {
        'stroke': self.stroke,
        'stroke-width': self.stroke_width,
        'fill': 'none'
        }
    wsvg(self.paths, attributes=[atr]*len(self.paths), filename=fn)
    return self

  def sort(self, reverse=False, rnd=False, verbose=False):
    order, flip = get_sort_order(self.paths, reverse, get_init_pos(self.bbox, rnd))

    if reverse:
      self.paths = list(flip_reorder(self.paths, order, flip))
    else:
      self.paths = list(reorder(self.paths, order))

    if verbose:
      length, pen_length = get_length(self.paths)

      print('sort:')

      print('--number of paths: {:d}'.format(len(self.paths)))
      print('--total path length: {:0.2f}\n--pen move ratio: {:0.2f}'\
          .format(length, pen_length/length))

      df = self.initial_length-length
      ratio = df/self.initial_length

      print('--bbox', bbox(self.paths))
      print('--improvement: {:0.2f}'.format(ratio))

      if ratio < 0.0:
        print('WARNING: there was negative improvement.')
      elif ratio < 0.05:
        print('WARNING: there was very little improvement.')

    return self

  def repeat(self, verbose=False):
    self.paths.extend([attempt_reverse(deepcopy(p))
                       for p in reversed(self.paths)])
    if verbose:
      length, pen_length = get_length(self.paths)
      print('adding all primitives in reverse:')
      print('--number of paths: {:d}'.format(len(self.paths)))
      print('--total path length: {:0.2f}\n--pen move ratio: {:0.2f}'\
          .format(length, pen_length/length))
    return self

