# -*- coding: utf-8 -*-

from os import getcwd
from os.path import sep

from svgpathtools import svg2paths2
from svgpathtools import wsvg

from svgsort.utils import get_sort_order
from svgsort.utils import get_length
from svgsort.utils import reorder
from svgsort.utils import flip_reorder



class Svgsort():
  def __init__(self):
    self.cwd = getcwd()
    self.paths = None
    self.attributes = None
    self.initial_length = -1

  def load(self, fn, verbose=False):
    paths, attributes, vals = svg2paths2(self.cwd + sep + fn)
    self.paths = paths
    self.attributes = attributes

    self.initial_length = get_length(paths)
    if verbose:
      print('initial length: {:0.2f}'.format(self.initial_length))

    return self

  def save(self, fn):
    wsvg(self.paths, attributes=self.attributes, filename=fn)
    return self

  def sort(self, reverse=False, verbose=False):

    if reverse:
      print('WARNING: --reverse is experimental.')
    order, flip = get_sort_order(self.paths, reverse)

    if reverse:
      self.paths = list(flip_reorder(self.paths, order, flip))
    else:
      self.paths = list(reorder(self.paths, order))
    self.attributes = list(reorder(self.attributes, order))

    if verbose:
      length = get_length(self.paths)
      print('number of paths: {:d}'.format(len(self.paths)))
      print('sorted length: {:0.2f}'.format(length))
      df = self.initial_length-length
      print('estimated improvement: {:0.2f}'.format(df/self.initial_length))

    return self

