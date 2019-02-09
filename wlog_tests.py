import unittest
from wlog import *


class TestWLOG(unittest.TestCase):
    def test02_single_identifier(self):
        x = 1
        y = 2

        with out_loss_of_generality(lambda x: x == 2):
            self.assertEqual(2, x)
            self.assertEqual(2, y)

        self.assertEqual(1, x)
        self.assertEqual(2, y)

    def test01_basic_integers(self):
        x = 1
        y = 2

        with out_loss_of_generality(lambda x, y: x > y):
            self.assertEqual(2, x)
            self.assertEqual(1, y)

        self.assertEqual(1, x)
        self.assertEqual(2, y)

    def test03_unchanged(self):
        x = 1
        y = 2

        with out_loss_of_generality(lambda x, y: x < y):
            self.assertEqual(1, x)
            self.assertEqual(2, y)

        self.assertEqual(1, x)
        self.assertEqual(2, y)

    def test04_extra_locals(self):
        x = 1
        y = 2
        z = None

        with out_loss_of_generality(lambda x, y: x > y):
            self.assertEqual(2, x)
            self.assertEqual(1, y)
            self.assertIsNone(z)

        self.assertEqual(1, x)
        self.assertEqual(2, y)
        self.assertIsNone(z)

    def test05_unbound(self):
        y = 1
        z = 2

        with self.assertRaises(Exception):
            with out_loss_of_generality(lambda x, y: x < y):
                self.fail()

    def test06_global_binding(self):
        global w
        w = 4

        with self.assertRaises(Exception):
            with out_loss_of_generality(lambda w: w == 1):
                self.fail()

    def test07_global_value(self):
        global w
        w = 4

        x = 1
        y = 2

        with out_loss_of_generality(lambda x: x == 4):
            self.assertEqual(4, x)
            self.assertEqual(2, y)
            self.assertEqual(4, w)

        self.assertEqual(1, x)
        self.assertEqual(2, y)
        self.assertEqual(4, w)

    def test08_three_bindings(self):
        x = 1
        y = 2
        z = 3

        with out_loss_of_generality(lambda x, y, z: x >= y + z and y > z):
            self.assertEqual(3, x)
            self.assertEqual(2, y)
            self.assertEqual(1, z)

        self.assertEqual(1, x)
        self.assertEqual(2, y)
        self.assertEqual(3, z)

    def test09_strings(self):
        x = "foo"
        y = "bar"

        with out_loss_of_generality(lambda x: x.startswith('b')):
            self.assertEqual("bar", x)
            self.assertEqual("bar", y)

        self.assertEqual("foo", x)
        self.assertEqual("bar", y)

    def test10_lists(self):
        x = [1, 2, 3]
        y = ['a', 'b']

        with out_loss_of_generality(lambda x, y: len(x) < len(y)):
            self.assertEqual(['a', 'b'], x)
            self.assertEqual([1, 2, 3], y)

        self.assertEqual([1, 2, 3], x)
        self.assertEqual(['a', 'b'], y)


if __name__ == "__main__":
    unittest.main()
