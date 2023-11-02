# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0611,R0903


"mixin"


import unittest


from prg.object import Object, read, update, write


class Test:

    pass


class TestMixin(unittest.TestCase):

    def test_mixin(self):
        class Mixin(Test, Object):
            pass
        mixin = Mixin()
        mixin.aaa = "b"
        write(mixin, ".test/mixin")
        mixin2 = Mixin()
        mixin3 = Mixin()
        update(mixin3, mixin)
        read(mixin2, ".test/mixin")
        self.assertEqual(mixin2.aaa, mixin3.aaa)
