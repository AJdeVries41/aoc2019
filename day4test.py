import unittest
import day4 

class Day4test(unittest.TestCase):

    def test1(self):
        num = 112233
        self.assertTrue(day4.meets_part2_criteria(num))

    def test2(self):
        num = 223450
        self.assertFalse(day4.meets_part2_criteria(num))

    def test3(self):
        num = 123789
        self.assertFalse(day4.meets_part2_criteria(num))

    def test4(self):
        num = 123444
        self.assertFalse(day4.meets_part2_criteria(num))

    def test5(self):
        num = 111122
        self.assertTrue(day4.meets_part2_criteria(num))

if __name__ == '__main__':
    unittest.main()
