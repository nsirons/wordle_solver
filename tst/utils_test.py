import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.utils import CharState, pattern_value_to_pattern_arr, word_to_pattern_value


class UtilsTest(unittest.TestCase):

    def test_pattern(self):
        exp1 = (CharState.GREEN, CharState.GREEN, CharState.GREEN, CharState.GREEN, CharState.GREEN)
        exp2 = (CharState.GREY, CharState.GREY, CharState.GREY, CharState.GREY, CharState.GREY)
        exp3 = (CharState.YELLOW, CharState.YELLOW, CharState.YELLOW, CharState.YELLOW, CharState.YELLOW)
        exp4 = (CharState.GREY, CharState.GREEN, CharState.GREEN, CharState.GREY, CharState.GREEN)
        exp5 = (CharState.YELLOW, CharState.YELLOW, CharState.GREY, CharState.YELLOW, CharState.GREEN)
        exp6 = (CharState.GREEN, CharState.YELLOW, CharState.GREY, CharState.GREEN, CharState.GREY)
        word_pair1 = "abcde", "abcde"
        word_pair2 = "aaaaa", "bbbbb"
        word_pair3 = "abcde", "bcdea"
        word_pair4 = "crane", "grape"
        word_pair5 = "allee", "eagle"
        word_pair6 = "sassy", "spasm"
        test_cases = ((word_pair1, exp1), (word_pair2, exp2), (word_pair3, exp3), (word_pair4, exp4),
                      (word_pair5, exp5), (word_pair6, exp6))
        for word_pair, exp in test_cases:
            self.assertEqual(pattern_value_to_pattern_arr(word_to_pattern_value(word_pair[0], word_pair[1])), exp)


if __name__ == '__main__':
    unittest.main()
