# -*- coding: utf-8 -*-


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


def get_bbox(paths):
  xmin, xmax, ymin, ymax = paths[0].bbox()
  for p in paths:
    xmi, xma, ymi, yma = p.bbox()
    xmin = min(xmin, xmi)
    xmax = max(xmax, xma)
    ymin = min(ymin, ymi)
    ymax = max(ymax, yma)
  return xmin, xmax, ymin, ymax


def get_long_short(paths, pad, padAbs=False):
  xmin, xmax, ymin, ymax = get_bbox(paths)
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

