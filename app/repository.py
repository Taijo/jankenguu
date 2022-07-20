import os
from typing import Optional, Tuple

import pandas as pd

# FILE RESPONSIBLE TO LOAD, SAVE AND DELETE DATA

FILE_PATH = "previous_plays.json"


def delete_previous_plays() -> None:
    if os.path.isfile(FILE_PATH):
        os.remove(FILE_PATH)


def load_previous_plays() -> Tuple[bool, Optional[pd.DataFrame]]:
    if not os.path.isfile(FILE_PATH):
        return None, None
    return True, pd.read_json(FILE_PATH)


def save_play(df: pd.DataFrame) -> None:
    df.to_json(FILE_PATH)
