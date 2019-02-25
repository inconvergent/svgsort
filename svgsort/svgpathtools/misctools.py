"""This submodule contains miscellaneous tools that are used internally, but
aren't specific to SVGs or related mathematical objects."""

# External dependencies:
from __future__ import division, absolute_import, print_function


# stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
def hex2rgb(value):
  """Converts a hexadeximal color string to an RGB 3-tuple

  EXAMPLE
  -------
  >>> hex2rgb('#0000FF')
  (0, 0, 255)
  """
  value = value.lstrip('#')
  lv = len(value)
  return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))


# stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
def rgb2hex(rgb):
  """Converts an RGB 3-tuple to a hexadeximal color string.

  EXAMPLE
  -------
  >>> rgb2hex((0,0,255))
  '#0000FF'
  """
  return ('#%02x%02x%02x' % tuple(rgb)).upper()


def isclose(a, b, rtol=1e-5, atol=1e-8):
  """This is essentially np.isclose, but slightly faster."""
  return abs(a - b) < (atol + rtol * abs(b))

