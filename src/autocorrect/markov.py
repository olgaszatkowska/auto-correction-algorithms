import random
from collections import defaultdict

from autocorrect.abstract import ContextAutoCorrect
from data import load_valid_sentences

class MarkovModel:
    def __init__(self, n: int=1):
        self.n = n 
        self.model = defaultdict(lambda: defaultdict(int))

    def train(self, corpus: str) -> None:
        for line in corpus:
            words = line.strip().split()
            for i in range(len(words) - self.n):
                state = tuple(words[i : i + self.n])
                next_word = words[i + self.n]
                self.model[state][next_word] += 1

    def predict(self, current_state):
        next_word_counts = self.model[tuple(current_state)]
        if not next_word_counts:
            return None
        total_count = sum(next_word_counts.values())
        probabilities = {
            word: count / total_count for word, count in next_word_counts.items()
        }
        return random.choices(
            list(probabilities.keys()), weights=probabilities.values()
        )[0]

    def suggest_correction(self, context):
        suggestions = {}
        for next_word in self.model[tuple(context)]:
            suggestions[next_word] = self.model[tuple(context)][next_word]

        if suggestions:
            sorted_suggestions = sorted(
                suggestions.items(), key=lambda x: x[1], reverse=True
            )
            return [word for word, _ in sorted_suggestions]
        else:
            return []


class MarkovAutoCorrect(ContextAutoCorrect):
    def __init__(self, order: int = 1):
        corpus = load_valid_sentences()
        self.markov_model = MarkovModel(n=order)
        self.markov_model.train(corpus)

    def fix_word(self, sentence: str) -> str:
        words = sentence.split()
        corrected_sentence = []

        for i, word in enumerate(words):
            if not self.is_correct(word):
                context = words[max(0, i - 1) : i]
                suggestions = self.markov_model.suggest_correction(context)
                if suggestions:
                    corrected_word = suggestions[0]
                    corrected_sentence.append(corrected_word)
                else:
                    corrected_sentence.append(word)
            else:
                corrected_sentence.append(word)
        return " ".join(corrected_sentence)

    @property
    def name(self) -> str:
        return "Markov"