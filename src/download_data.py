import os

import kagglehub
import pandas as pd
import random

from env_keys import (
    SINGLE_WORD_LOOKUP_DATA_PATH_KEY,
    CONTEXT_DATA_FILENAME_KEY,
)

CONTEXT_DATA_FILENAME = "misspelled_sentences.csv"


def misspell_sentence(sentence: str, misspelled_df: pd.DataFrame) -> str | None:
    as_list = sentence.split(" ")

    indices = list(range(len(as_list)))
    random.shuffle(indices)

    for i in indices:
        word = as_list[i]
        misspellings = misspelled_df[misspelled_df["label"] == word]["input"]

        if not misspellings.empty:
            as_list[i] = random.choice(misspellings.tolist())
            return " ".join(as_list)

    return None


def create_misspelled_sentences(
    SINGLE_WORD_LOOKUP_DATA_path: str, english_sentences_path: str
):
    with open(english_sentences_path, "r") as english_sentences_file:
        english_sentences = english_sentences_file.readlines()

    misspelled_df = pd.read_csv(SINGLE_WORD_LOOKUP_DATA_path)

    with open(CONTEXT_DATA_FILENAME, "w") as misspelled_sentences_file:
        misspelled_sentences_file.write(",label,input\n")
        for i, sentence in enumerate(english_sentences):
            sentence = sentence.replace("\n", "")
            sentence = sentence.replace(",", "")
            misspelled_sentence = misspell_sentence(sentence, misspelled_df)

            if misspelled_sentence:
                line = f"{i},{sentence},{misspelled_sentence}"
                misspelled_sentences_file.write(line + "\n")


def download_data():
    misspelled_path = kagglehub.dataset_download("fazilbtopal/misspelled-words")
    sentences_path = kagglehub.dataset_download("nikitricky/random-english-sentences")
    env_file = ".env"

    SINGLE_WORD_LOOKUP_DATA_FILE_PATH = os.path.join(misspelled_path, "misspelled.csv")
    SENTENCES_DATA_FILE_PATH = os.path.join(sentences_path, "sentences.txt")

    with open(env_file, "w") as file:
        file.write(
            f'{SINGLE_WORD_LOOKUP_DATA_PATH_KEY}="{SINGLE_WORD_LOOKUP_DATA_FILE_PATH}"\n'
        )
        file.write(f'{CONTEXT_DATA_FILENAME_KEY}="{CONTEXT_DATA_FILENAME}"\n')

    print("Successfully created .env file with data paths.")

    create_misspelled_sentences(
        SINGLE_WORD_LOOKUP_DATA_FILE_PATH, SENTENCES_DATA_FILE_PATH
    )

    print("Successfully crated file with misspelled sentences.")


if __name__ == "__main__":
    download_data()
