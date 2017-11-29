# -*- coding: utf-8 -*-

from os import getcwd
from os.path import sep

from svgpathtools import svg2paths2
from svgpathtools import wsvg

from numpy import array
from numpy import zeros
from numpy.linalg import norm
from scipy.spatial import cKDTree as kdt


def ct(c):
  return (c.real, c.imag)


def spatial_sort(paths, init_rad=0.01):

  num = len(paths)
  res = []
  unsorted = set(range(2*num))

  xs = zeros((2*num, 2), 'float')
  x_path = zeros(2*num, 'int')

  for i, path in enumerate(paths):
    xs[i, :] = path[0, :]
    xs[num+i, :] = path[-1, :]
    x_path[i] = i
    x_path[num+i] = i

  tree = kdt(xs)

  count = 0
  pos = array([1000, 0], 'float')

  order = []

  while count < num:

    rad = init_rad
    while True:
      near = tree.query_ball_point(pos, rad)
      cands = list(set(near).intersection(unsorted))
      if not cands:
        rad *= 2.0
        continue

      dst = norm(pos - xs[cands, :], axis=1)
      cp = dst.argmin()
      uns = cands[cp]
      break

    path_ind = x_path[uns]
    path = paths[path_ind]

    if uns >= num:
      res.append(path[::-1])
      pos = paths[path_ind][0, :]
      unsorted.remove(uns)
      unsorted.remove(uns-num)

    else:
      res.append(path)
      pos = paths[path_ind][-1, :]
      unsorted.remove(uns)
      unsorted.remove(uns+num)

    order.append(path_ind)
    count += 1

  return order



def do_sort(paths, attributes):

  coords = []

  for p in paths:
    start = ct(p.point(0))
    stop = ct(p.point(0))
    coords.append(array([start, stop]))

  order = spatial_sort(coords)

  new_path = []
  new_attrib = []
  for i in order:
    new_path.append(paths[i])
    new_attrib.append(attributes[i])

  return new_path, new_attrib



class Svgsort():
  def __init__(self):
    self.cwd = getcwd()
    self.paths = None
    self.attributes = None

  def load(self, fn):
    paths, attributes, vals = svg2paths2(self.cwd + sep + fn)
    self.paths = paths
    self.attributes = attributes

    sorted_paths, sorted_attributes = do_sort(self.paths, self.attributes)

    self.paths = sorted_paths
    self.attributes = sorted_attributes

    return self

  def save(self, fn):
    wsvg(self.paths, attributes=self.attributes, filename=fn)
    return self

  def sort(self):
    return self

