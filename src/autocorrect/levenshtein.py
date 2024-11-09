import numpy as np

from autocorrect.abstract import SingleWordLookup
from data import load_valid_words


class LevenshteinAutoCorrect(SingleWordLookup):
    def fix_word(self, word: str) -> str:
        dictionary = load_valid_words()

        closest_word = None
        min_distance = float("inf")

        for dict_word in dictionary:
            distance = self._levenshtein_distance(word, dict_word)

            if distance < min_distance:
                min_distance = distance
                closest_word = dict_word

        return closest_word

    def _levenshtein_distance(self, word: str, dict_word: str):
        dp = np.zeros((len(word) + 1, len(dict_word) + 1), dtype=int)

        for i in range(len(word) + 1):
            dp[i][0] = i
        for j in range(len(dict_word) + 1):
            dp[0][j] = j

        for i in range(1, len(word) + 1):
            for j in range(1, len(dict_word) + 1):
                if word[i - 1] == dict_word[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[len(word)][len(dict_word)]

    @property
    def name(self) -> str:
        return "Levenshtein"
