# Standard
from unittest import TestCase

# Project
from walleter.utils import base58

# Tests borrowed from https://gist.github.com/ianoxley/865912
# to make sure I knew what I was doing.


class Base58Tests(TestCase):

  def test_encode_1(self):
    self.assertEqual('Tgmc', base58.encode(10002343))

  def test_decode_1(self):
    self.assertEqual(10002343, base58.decode('Tgmc'))

  def test_encode_1(self):
    self.assertEqual('if', base58.encode(1000))

  def test_decode_2(self):
    self.assertEqual(1000, base58.decode('if'))

  def test_encode_3(self):
    self.assertEqual('', base58.encode(0))

  def test_encode_4(self):
    self.assertEqual('', base58.encode(-100))
