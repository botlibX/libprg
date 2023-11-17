# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"none"


import unittest


class TestNone(unittest.TestCase):

    def test_none(self):
        self.assertTrue(not None)
