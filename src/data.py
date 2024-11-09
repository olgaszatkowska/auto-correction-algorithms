import os

import pandas as pd
from dotenv import load_dotenv

from env_keys import (
    SINGLE_WORD_LOOKUP_DATA_PATH_KEY,
    CONTEXT_DATA_FILENAME_KEY,
)


load_dotenv()

missing_file_msg = "Data path not set please run 'make prepare' first"


def _load_data_set(path: str) -> None:
    file_path = os.getenv(path)

    if not file_path:
        print(missing_file_msg)
        exit()
    
    train_data = pd.read_csv(file_path, sep=",")

    return train_data

def load_context_data_set() -> pd.DataFrame:
    return _load_data_set(CONTEXT_DATA_FILENAME_KEY)

def load_valid_sentences() -> pd.DataFrame:
    df = load_context_data_set()
    return df["label"].tolist()

def load_single_word_lookup_data_set() -> pd.DataFrame:
    return _load_data_set(SINGLE_WORD_LOOKUP_DATA_PATH_KEY)

def load_valid_words() -> pd.DataFrame:
    df = load_single_word_lookup_data_set()
    return df["label"].tolist()
