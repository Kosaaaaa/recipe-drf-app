from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Tests the calc module"""

    def test_add_ints(self):
        res = calc.add(5, 9)

        self.assertEqual(res, 14)

    def test_add_floats(self):
        res = calc.add(5.5, 3.14)

        self.assertAlmostEqual(res, 8.64)

    def test_add_numbers(self):
        res = calc.add(5, 3.14)

        self.assertAlmostEqual(res, 8.14)

    def test_subtract_ints(self):
        res = calc.subtract(9, 3)

        self.assertEqual(res, 6)

    def test_subtract_floats(self):
        res = calc.subtract(9.99, 3.1)

        self.assertAlmostEqual(res, 6.89)

    def test_subtract_numbers(self):
        res = calc.subtract(9.99, 3)

        self.assertAlmostEqual(res, 6.99)

    def test_factorial(self):
        correct_results = [
            (1, 1),
            (5, 120),
            (6, 720),
            (10, 3_628_800),
        ]

        for x, res in correct_results:
            self.assertEqual(calc.factorial(x), res)

