# -*- coding: utf-8 -*-

from math import sqrt
from numpy import array
from numpy import zeros
from numpy.linalg import norm
from scipy.spatial import cKDTree as kdt


def ct(c):
  return (c.real, c.imag)


def spatial_sort(paths, init_rad=0.01):

  num = len(paths)
  flip = []
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
  pos = array([0, 0], 'float')

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
      flip.append(True)
      pos = paths[path_ind][0, :]
      unsorted.remove(uns)
      unsorted.remove(uns-num)

    else:
      flip.append(False)
      pos = paths[path_ind][-1, :]
      unsorted.remove(uns)
      unsorted.remove(uns+num)

    order.append(path_ind)
    count += 1

  return order, flip


def reorder(l, order, flip=None):
  for i in order:
    if flip:
      li = l[i]
      li.reverse()
      yield li
    else:
      yield l[i]


def get_sort_order(paths, reverse):

  coords = []

  for p in paths:
    start = ct(p.point(0))
    if reverse:
      stop = ct(p.point(1))
    else:
      stop = ct(p.point(0))

    coords.append(array([start, stop]))

  order, flip = spatial_sort(coords)

  if reverse:
    return order, flip
  return order, [False]*len(order)


def get_length(paths):
  pos = (0.0, 0.0)
  tot = 0
  for p in paths:

    ox, oy = pos
    cx, cy = ct(p.point(0))
    tot += sqrt(pow(ox-cx, 2.0) + pow(oy-cy, 2.0))

    tot += p.length()
    pos = ct(p.point(1))

  return tot


