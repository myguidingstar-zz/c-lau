#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from clau import *

class Test(unittest.TestCase):
  def test_normalizeDiacritics(self):
      cases = [
      # source           converter               result
      (u"uỳ oà ùy òa",   normalizeDiacritics,    u"ùy òa ùy òa"),
      ]

      for (source, converter, result) in cases:
          self.assertEqual(result, converter(source))

if __name__ == '__main__':
    unittest.main()
