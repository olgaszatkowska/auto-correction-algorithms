from abc import ABC, abstractmethod

from pandas import DataFrame

from data import (
    load_single_word_lookup_data_set,
    load_context_data_set,
    load_valid_sentences,
    load_valid_words,
)


class AutoCorrect(ABC):
    @abstractmethod
    def fix_word(self, word: str) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplemented

    @abstractmethod
    def load_test_set(self, n: str) -> DataFrame:
        raise NotImplemented

    @abstractmethod
    def load_valid_words(self) -> list[str]:
        raise NotImplemented


class SingleWordLookup(AutoCorrect):
    def load_test_set(self, n: str) -> DataFrame:
        df = load_single_word_lookup_data_set()
        return df.sample(n=n)

    def load_valid_words(self) -> list[str]:
        return load_valid_words()


class ContextAutoCorrect(AutoCorrect):
    def load_test_set(self, n: str) -> DataFrame:
        df = load_context_data_set()
        return df.sample(n=n)

    def load_valid_words(self) -> list[str]:
        corpus = load_valid_sentences()
        unique_words = set()
        for sentence in corpus:
            unique_words.update(sentence.lower().split())

        return unique_words

    def load_valid_sentences(self) -> list[str]:
        return load_valid_sentences()

    def is_correct(self, word: str) -> list[str]:
        return word in self.load_valid_words()
