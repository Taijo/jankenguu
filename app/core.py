import random
from typing import Literal, Tuple

import pandas as pd
from fastapi import status

from .models import POSSIBLE_HAND_VALUES, Hand, Play


def create_ai_hand(
    df_previous_plays: pd.DataFrame, previous_plays_exists: bool
) -> Hand:
    if not previous_plays_exists:
        """
        RANDOM STRATEGY
        """
        ai_random_hand = list(POSSIBLE_HAND_VALUES)[random.randint(0, 2)]
        return Hand(myHand=ai_random_hand)

    player_hand_sorted_by_most_played = (
        df_previous_plays["player_hand"].value_counts().index.tolist()
    )

    player_hand_count_sorted_by_most_played = (
        df_previous_plays["player_hand"].value_counts().values.tolist()
    )

    """
    BASIC STRATEGY : Trying to counter the most played hand by the player
    Very efficient if player plays always the same hand
    """
    # player_hand_most_played = player_hand_sorted_by_most_played[0]
    # counter_play_dict = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    # ai_hand = counter_play_dict[player_hand_most_played]

    """
    OTHER STRATEGY : WEIGHTED RANDOM -> random influenced by previous player hands 
    """
    most_predictable_player_hand_from_previous_play = random.choices(
        player_hand_sorted_by_most_played,
        weights=player_hand_count_sorted_by_most_played,
        k=1,
    )[0]
    counter_play_dict = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    ai_hand = counter_play_dict[most_predictable_player_hand_from_previous_play]
    return Hand(myHand=ai_hand)


def calculate_result(player_hand: Hand, ai_hand: Hand) -> str:
    """3 trees of play possibilities : root is first hand, leaf is second hand
    result equal RULES[root][leaf] -> 0 = tie / 1 = root win / -1 = root lose
    return 0 = tie or 1 = player win or -1 = player lose"""

    RULES = {
        "rock": {"rock": 0, "scissors": 1, "paper": -1},
        "paper": {"rock": 1, "scissors": -1, "paper": 0},
        "scissors": {"rock": -1, "scissors": 0, "paper": 1},
    }

    return RULES[player_hand.value][ai_hand.value]


def calculate_results_from_previous_plays(
    df_previous_plays: pd.DataFrame,
) -> Tuple[int, int]:
    number_of_wins_and_losses_series = df_previous_plays["result"].value_counts()
    player_wins_count = number_of_wins_and_losses_series.get(1, default=0)
    player_losses_count = number_of_wins_and_losses_series.get(-1, default=0)
    return int(player_wins_count), int(player_losses_count)


def adding_play_to_previous_plays(
    play: Play, df_previous_plays: pd.DataFrame
) -> pd.DataFrame:
    data = {
        "player_hand": play.player_hand.value,
        "ai_hand": play.ai_hand.value,
        "result": play.result,
    }

    df_play = pd.DataFrame(data=[data])
    df = pd.concat([df_previous_plays, df_play], ignore_index=True)
    return df


def display_previous_results(player_wins_count: int, player_losses_count: int) -> dict:
    return {
        "player": player_wins_count,
        "computer": player_losses_count,
    }


def choose_http_status_response_from_result(result: int) -> Literal:
    http_status_from_result = {
        0: status.HTTP_418_IM_A_TEAPOT,
        1: status.HTTP_201_CREATED,
        -1: status.HTTP_202_ACCEPTED,
    }
    return http_status_from_result[result]


def choose_result_message_from_result(play: Play) -> str:
    result_message_from_result = {
        0: f"You played {play.player_hand.value}, I played {play.ai_hand.value}, it's a tie",
        1: f"You played {play.player_hand.value}, I played {play.ai_hand.value}, you win",
        -1: f"You played {play.player_hand.value}, I played {play.ai_hand.value}, you lose",
    }
    return result_message_from_result[play.result]
