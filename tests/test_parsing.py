"""

"""

import unittest
from gencomp.parsing import square


class TestParsing(unittest.TestCase):
    """ """

    def setUp(self):
        print("setting up parsing test")

    def tearDown(self):
        pass

    def test_square(self):
        """ assert we get acutal squares """
        for i in range(10):
            self.assertAlmostEqual(square(i), i * i)
