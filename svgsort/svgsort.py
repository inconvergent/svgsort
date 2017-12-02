# -*- coding: utf-8 -*-

from os import getcwd
from os.path import sep

from svgpathtools import svg2paths2
from svgpathtools import wsvg

from svgsort.utils import get_sort_order
from svgsort.utils import get_length
from svgsort.utils import reorder



class Svgsort():
  def __init__(self):
    self.cwd = getcwd()
    self.paths = None
    self.attributes = None
    self.initial_length = -1

  def load(self, fn):
    paths, attributes, vals = svg2paths2(self.cwd + sep + fn)
    self.paths = paths
    self.attributes = attributes

    self.initial_length = get_length(paths)
    print('initial length: {:0.1f}'.format(self.initial_length))

    return self

  def save(self, fn):
    wsvg(self.paths, attributes=self.attributes, filename=fn)
    return self

  def sort(self, reverse=False):

    order, flip = get_sort_order(self.paths, reverse)

    self.paths = list(reorder(self.paths, order, flip=flip))
    self.attributes = list(reorder(self.attributes, order))

    length = get_length(self.paths)

    print('sorted length: {:0.1f}'.format(length))
    print('improvement: {:0.1f}'.format(length/self.initial_length))

    return self

