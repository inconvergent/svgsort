# -*- coding: utf-8 -*-

from os import getcwd
from os.path import sep

from copy import deepcopy

from numpy.random import random
from numpy import array

from .svgpathtools import svg2paths
from .svgpathtools import disvg

from .sort_utils import attempt_reverse
from .sort_utils import flip_reorder
from .sort_utils import get_cont_paths
from .sort_utils import get_length
from .sort_utils import get_sort_order
from .sort_utils import split_all
from .sort_utils import pen_moves

from .paper_utils import get_bbox
from .paper_utils import get_long_short
from .paper_utils import vbox_paper


STROKE_WIDTH = 1.0


def get_init_pos(bb, rnd):
  xmin, xmax, ymin, ymax = bb
  if rnd:
    return array([
        xmin + random()*(xmax-xmin),
        ymin + random()*(ymax-ymin)])
  return array([0, 0], 'float')


class Svgsort():
  def __init__(self, sw=None):
    self.sw = sw if sw is not None else STROKE_WIDTH
    self.initial_length = -1
    self.svg_atr = {}
    self.attributes = None
    self.pen_move_paths = None
    self.bbox = None
    self.paths = None

  def _load_report(self, length, pen_length):
    print('initial:')
    print('  number of paths: {:d}'.format(len(self.paths)))
    print('  total path length: {:0.2f}\n  pen move ratio: {:0.2f}'\
        .format(length, pen_length/length))
    print('  bbox', self.bbox)

  def _sort_report(self):
    length, pen_length = get_length(self.paths)
    print('sort:')
    print('  number of paths: {:d}'.format(len(self.paths)))
    print('  total path length: {:0.2f}\n  pen move ratio: {:0.2f}'.format(
        length, pen_length/length))

    df = self.initial_length-length
    ratio = df/self.initial_length

    print('  bbox', get_bbox(self.paths))
    print('  improvement: {:0.2f}'.format(ratio))

    if ratio < 0.0:
      print('WARNING: the result is less efficient than the original.')
    elif ratio < 0.05:
      print('WARNING: there was very little improvement.')

  def _repeat_report(self):
    length, pen_length = get_length(self.paths)
    print('adding all primitives in reverse:')
    print('  number of paths: {:d}'.format(len(self.paths)))
    print('  total path length: {:0.2f}\n  pen move ratio: {:0.2f}'\
        .format(length, pen_length/length))

  def _save_report(self, paper, pad, padAbs, portrait):
    print('centering on paper: {:s}:'.format(paper['name']))
    print('  pad: {:0.5f} ({:s})'.format(pad, 'abs' if padAbs else 'rel'))
    print('  format: {:s}'.format('portrait' if portrait else 'landscape'))

  def load(self, fn):
    paths, _, svg_atr = svg2paths(getcwd() + sep + fn,
                                  return_svg_attributes=True)
    self.paths = paths
    self.svg_atr = svg_atr

    length, pen_length = get_length(paths)
    self.initial_length = length
    self.bbox = get_bbox(paths)
    self._load_report(length, pen_length)
    return self

  def split(self):
    print('splitting paths:')
    self.paths = list(get_cont_paths(self.paths))
    print('  new number of paths: {:d}'.format(len(self.paths)))
    return self

  def eager_split(self):
    print('splitting into primitives:')
    self.paths = list(split_all(list(get_cont_paths(self.paths))))
    print('  new number of paths (primitives): {:d}'.format(len(self.paths)))
    return self

  def make_pen_move_paths(self):
    self.pen_move_paths = list(pen_moves(self.paths))
    return self

  def sort(self, rnd=False):
    order, flip = get_sort_order(self.paths, get_init_pos(self.bbox, rnd))
    self.paths = list(flip_reorder(self.paths, order, flip))
    self._sort_report()
    return self

  def repeat(self):
    self.paths.extend([attempt_reverse(deepcopy(p))
                       for p in reversed(self.paths)])
    self._repeat_report()
    return self

  def _path_attr(self):
    sw = self.sw
    atr = {'stroke': 'black', 'stroke-width': sw, 'fill': 'none'}
    move_atr = {'stroke': 'red', 'stroke-width': sw, 'fill': 'none'}

    paths = self.paths
    attributes = [atr]*len(self.paths)
    if self.pen_move_paths is not None:
      paths = paths + self.pen_move_paths
      attributes = attributes + [move_atr]*len(self.pen_move_paths)
    return paths, attributes

  def save_no_adjust(self, fn):
    paths, attributes = self._path_attr()
    keys = ['width', 'height', 'viewBox']
    disvg(paths=paths,
          filename=fn,
          attributes=attributes,
          svg_attributes=dict({k:self.svg_atr[k] for k in keys
                               if k in self.svg_atr}))
    print('wrote:', fn)
    return self

  def save(self, fn, paper, pad=None, padAbs=False):
    ls = get_long_short(self.paths, pad, padAbs)
    portrait, vb, size = vbox_paper(ls, paper)
    self._save_report(paper, pad, padAbs, portrait)

    paths, attributes = self._path_attr()
    disvg(paths=paths,
          filename=fn,
          attributes=attributes,
          dimensions=(size['width'], size['height']),
          svg_attributes={'viewBox': ' '.join([str(s) for s in vb])})
    print('wrote:', fn)
    return self

