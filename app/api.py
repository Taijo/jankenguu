import pandas as pd
from fastapi import FastAPI, Response

from .core import (
    adding_play_to_previous_plays,
    calculate_result,
    calculate_results_from_previous_plays,
    choose_http_status_response_from_result,
    choose_result_message_from_result,
    create_ai_hand,
    display_previous_results,
)
from .models import Hand, Play
from .repository import delete_previous_plays, load_previous_plays, save_play

app = FastAPI()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to 'Rock, Paper, Scissor' Game"}


@app.post("/play")
def play(player_hand: Hand, response: Response) -> dict:

    previous_plays_exists, df = load_previous_plays()
    if not previous_plays_exists:
        df = pd.DataFrame()

    ai_hand = create_ai_hand(df, previous_plays_exists)
    result = calculate_result(player_hand, ai_hand)
    play = Play(player_hand=player_hand, ai_hand=ai_hand, result=result)
    df = adding_play_to_previous_plays(play, df_previous_plays=df)
    save_play(df)
    response.status_code = choose_http_status_response_from_result(play.result)
    return choose_result_message_from_result(play)


@app.get("/results")
def results() -> dict:
    previous_plays_exists, df = load_previous_plays()
    if previous_plays_exists:
        return display_previous_results(*calculate_results_from_previous_plays(df))

    return {
        "player": 0,
        "computer": 0,
    }


@app.get("/reset")
def reset() -> dict:
    delete_previous_plays()
    return
