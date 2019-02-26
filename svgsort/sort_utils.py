# -*- coding: utf-8 -*-

from math import sqrt
from numpy import zeros
from numpy.linalg import norm
from scipy.spatial import cKDTree as kdt

from .svgpathtools.path import Line
from .svgpathtools import Path


def ct(c):
  return (c.real, c.imag)


def build_pos_index(paths):
  num = len(paths)
  xs = zeros((2*num, 2), 'float')
  x_path = zeros(2*num, 'int')

  for i, (start, stop) in enumerate(paths):
    xs[i, :] = start
    xs[num+i, :] = stop
    x_path[i] = i
    x_path[num+i] = i

  tree = kdt(xs)
  unsorted = set(range(2*num))
  return tree, xs, x_path, unsorted


def spatial_sort(paths, init_pos, init_rad=0.01):
  tree, xs, x_path, unsorted = build_pos_index(paths)

  num = len(paths)
  pos = init_pos

  flip = []
  order = []
  count = 0
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
      curr = cands[cp]
      break

    path_ind = x_path[curr]
    start, stop = paths[path_ind]

    if curr >= num:
      flip.append(True)
      pos = start
      unsorted.remove(curr)
      unsorted.remove(curr-num)
    else:
      flip.append(False)
      pos = stop
      unsorted.remove(curr)
      unsorted.remove(curr+num)

    order.append(path_ind)
    count += 1

  return order, flip


def attempt_reverse(path):
  try:
    if path.iscontinuous():
      rpath = path.reversed()
      if rpath.iscontinuous():
        return rpath
    print('''WARNING: unable to reverse path segment; this might give unintended
results. try without --reverse.''')
    return path
  except Exception:
    print('ERROR: when reversing path. try without --reverse.')


def flip_reorder(l, order, flip):
  for i, f in zip(order, flip):
    li = l[i]
    if f:
      li = attempt_reverse(li)
    yield li


def pen_moves(paths):
  if paths:
    curr = paths[0]
    for p in paths[1:]:
      yield Line(curr.end, p.start)
      curr = p


def get_sort_order(paths, init_pos):
  coords = []
  for p in paths:
    coords.append([ct(p.point(0)), ct(p.point(1))])
  return spatial_sort(coords, init_pos=init_pos)


def get_length(paths):
  pos = (0.0, 0.0)
  tot = 0.0
  pen = 0.0

  for p in get_cont_paths(paths):
    ox, oy = pos
    cx, cy = ct(p.point(0))
    tmp = sqrt(pow(ox-cx, 2.0) + pow(oy-cy, 2.0))
    pen += tmp
    tot += tmp

    try:
      tot += p.length()
    except ZeroDivisionError:
      print('WARN: /0 error in get_length. this is probably ok.')
    pos = ct(p.point(1))

  return tot, pen


def split_all(paths):
  for p in paths:
    for e in p:
      yield Path(e)


def get_cont_paths(paths):
  for p in paths:
    if not p.iscontinuous():
      for sp in p.continuous_subpaths():
        yield sp
    else:
      yield p

