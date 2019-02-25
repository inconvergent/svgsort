# -*- coding: utf-8 -*-

from os import getcwd
from os.path import sep

from copy import deepcopy

from numpy.random import random
from numpy import array

from svgsort.svgpathtools import svg2paths
from svgsort.svgpathtools import disvg

from svgsort.utils import attempt_reverse
from svgsort.utils import flip_reorder
from svgsort.utils import get_cont_paths
from svgsort.utils import get_length
from svgsort.utils import get_sort_order
from svgsort.utils import reorder
from svgsort.utils import split_all

LARGE = 1e10

PAPER = {
    'a4': {'short': 210, 'long': 297, 'r': 297.0/210.0, 'name': 'A4'},
    'a3':{'short': 297, 'long': 420, 'r': 420.0/297.0, 'name': 'A3'}
    }

def make_paper(xy):
  short = min(*xy)
  long = max(*xy)
  return {
      'short': short,
      'long': long,
      'r': long/short,
      'name': '{:d} x {:d}'.format(long, short)
      }


def bbox(paths):
  xmin, xmax, ymin, ymax = paths[0].bbox()
  for p in paths:
    xmi, xma, ymi, yma = p.bbox()
    xmin = min(xmin, xmi)
    xmax = max(xmax, xma)
    ymin = min(ymin, ymi)
    ymax = max(ymax, yma)
  return xmin, xmax, ymin, ymax


def get_long_short(paths, pad, padAbs=False):
  xmin, xmax, ymin, ymax = bbox(paths)
  width = xmax-xmin
  height = ymax-ymin
  portrait = width < height

  if not padAbs:
    b = pad*min(width, height)
  else:
    b = pad

  if portrait:
    return {
        'longDim': 'y',
        'portrait': True,
        'longmin': ymin-b,
        'shortmin': xmin-b,
        'long': height+2*b,
        'short': width+2*b,
        'r': height/width,
        }
  return {
      'longDim': 'x',
      'portrait': False,
      'longmin': xmin-b,
      'shortmin': ymin-b,
      'long': width+2*b,
      'short': height+2*b,
      'r': width/height,
      }


def vbox_paper(ls, p):
  lsnew = {k:v for k, v in ls.items()}

  if ls['r'] < p['r']:
    # resize limited by short
    lsnew['long'] = ls['short']*p['r']
    diff = lsnew['long'] - ls['long']
    lsnew['longmin'] -= diff*0.5
  else:
    # resize limted by long
    lsnew['short'] = ls['long']/p['r']
    diff = lsnew['short'] - ls['short']
    lsnew['shortmin'] -= diff*0.5

  lsnew['r'] = lsnew['long'] / lsnew['short']

  # xmin, ymin, width, height
  if ls['longDim'] == 'x':
    res = lsnew['longmin'], lsnew['shortmin'], lsnew['long'], lsnew['short']
  else:
    res = lsnew['shortmin'], lsnew['longmin'], lsnew['short'], lsnew['long']

  size = {
      'width': p['short'],
      'height': p['long']
      } if ls['portrait'] else {
          'width': p['long'],
          'height': p['short']
          }
  return ls['portrait'], res, {k:str(v)+'mm' for k, v in size.items()}


def get_init_pos(bb, rnd):
  xmin, xmax, ymin, ymax = bb
  if rnd:
    return array([
        xmin + random()*(xmax-xmin),
        ymin + random()*(ymax-ymin)])
  return array([0, 0], 'float')


class Svgsort():
  def __init__(self, verbose=False):
    self.attributes = None
    self.bbox = None
    self.cwd = getcwd()
    self.initial_length = -1
    self.paths = None
    self.stroke = 'black'
    self.stroke_width = 1.0
    self.verbose = verbose

  def load(self, fn):
    # TODO: handle non-center option
    paths, _, vals = svg2paths(self.cwd + sep + fn, return_svg_attributes=True)
    self.paths = paths

    length, pen_length = get_length(paths)
    self.initial_length = length
    self.bbox = bbox(paths)
    if self.verbose:
      print('initial:')
      print('  number of paths: {:d}'.format(len(paths)))
      print('  total path length: {:0.2f}\n  pen move ratio: {:0.2f}'\
          .format(length, pen_length/length))
      print('  bbox', self.bbox)

    return self

  def split(self):
    if self.verbose:
      print('splitting paths:')
    self.paths = list(get_cont_paths(self.paths))
    if self.verbose:
      print('  new number of paths: {:d}'.format(len(self.paths)))
    return self

  def eager_split(self):
    if self.verbose:
      print('splitting into primitives:')
    self.paths = list(split_all(list(get_cont_paths(self.paths))))
    if self.verbose:
      print('  new number of paths (primitives): {:d}'.format(len(self.paths)))
    return self

  def sort(self, reverse=False, rnd=False):
    order, flip = get_sort_order(self.paths, reverse,
                                 get_init_pos(self.bbox, rnd))

    if reverse:
      self.paths = list(flip_reorder(self.paths, order, flip))
    else:
      self.paths = list(reorder(self.paths, order))

    if self.verbose:
      length, pen_length = get_length(self.paths)

      print('sort:')
      print('  number of paths: {:d}'.format(len(self.paths)))
      print('  total path length: {:0.2f}\n  pen move ratio: {:0.2f}'\
          .format(length, pen_length/length))

      df = self.initial_length-length
      ratio = df/self.initial_length

      print('  bbox', bbox(self.paths))
      print('  improvement: {:0.2f}'.format(ratio))

      if ratio < 0.0:
        print('WARNING: the result is less efficient than the original.')
      elif ratio < 0.05:
        print('WARNING: there was very little improvement.')

    return self

  def repeat(self):
    self.paths.extend([attempt_reverse(deepcopy(p))
                       for p in reversed(self.paths)])
    if self.verbose:
      length, pen_length = get_length(self.paths)
      print('adding all primitives in reverse:')
      print('  number of paths: {:d}'.format(len(self.paths)))
      print('  total path length: {:0.2f}\n  pen move ratio: {:0.2f}'\
          .format(length, pen_length/length))
    return self

  def save(self, fn, paper, pad=None, padAbs=False, sw=None):

    atr = {}

    ls = get_long_short(self.paths, pad, padAbs)
    portrait, vb, size = vbox_paper(ls, paper)
    if self.verbose:
      print('centering on paper: {:s}:'.format(paper['name']))
      print('  pad: {:0.5f} ({:s})'.format(pad, 'abs' if padAbs else 'rel'))
      print('  format: {:s}'.format('portrait' if portrait else 'landscape'))

    atr['viewBox'] = ' '.join([str(s) for s in vb])

    # TODO: handle non-center option
    disvg(self.paths,
          filename=fn,
          attributes=[{
              'stroke': self.stroke,
              'stroke-width': sw if sw is not None else self.stroke_width,
              'fill': 'none'
              }]*len(self.paths),
          dimensions=(size['width'], size['height']),
          svg_attributes=atr)
    return self

