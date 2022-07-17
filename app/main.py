from ast import Constant
from random import randint

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, validator

app = FastAPI()

POSSIBLE_HAND_VALUES = ("rock", "paper", "scissors")


class Hand(BaseModel):
    myHand: str

    @validator("myHand")
    def hand_must_match_correct_values(cls, v):

        if v not in POSSIBLE_HAND_VALUES:
            raise HTTPException(
                status_code=400,
                detail=f"Incorrect hand value, should be either: {POSSIBLE_HAND_VALUES} ",
            )
        return v


def create_ai_hand():
    ai_random_hand = list(POSSIBLE_HAND_VALUES)[randint(0, 2)]
    return Hand(myHand=ai_random_hand)


def calculate_result(player_hand: Hand, ai_hand: Hand) -> str:
    """return 0 : a tie, 1 : player win or -1 player lose"""
    if player_hand.myHand == ai_hand.myHand:
        return 0

    if player_hand.myHand == "rock":
        if ai_hand.myHand == "paper":
            return -1
        elif ai_hand.myHand == "scissors":
            return 1

    if player_hand.myHand == "paper":
        if ai_hand.myHand == "scissors":
            return -1
        elif ai_hand.myHand == "rock":
            return 1

    if player_hand.myHand == "scissors":
        if ai_hand.myHand == "rock":
            return -1
        elif ai_hand.myHand == "paper":
            return 1


def choose_http_status_response_from_result(result: int) -> Constant:
    http_status_from_result = {
        0: status.HTTP_418_IM_A_TEAPOT,
        1: status.HTTP_201_CREATED,
        -1: status.HTTP_202_ACCEPTED,
    }
    return http_status_from_result[result]


def choose_result_message_from_result(
    result: int, player_hand: Hand, ai_hand: Hand
) -> str:
    result_message_from_result = {
        0: f"You played {player_hand.myHand}, I played {ai_hand.myHand}, it's a tie",
        1: f"You played {player_hand.myHand}, I played {ai_hand.myHand}, you win",
        -1: f"You played {player_hand.myHand}, I played {ai_hand.myHand}, you lose",
    }
    return result_message_from_result[result]


@app.get("/")
def root() -> dict:
    return {"Message": "Welcome to 'Rock, Paper, Scissor' Game"}


@app.post("/play")
def play(player_hand: Hand, response: Response) -> dict:

    ai_hand = create_ai_hand()
    result = calculate_result(player_hand, ai_hand)
    result_http_status = choose_http_status_response_from_result(result)
    result_message = choose_result_message_from_result(result, player_hand, ai_hand)
    response.status_code = result_http_status
    return result_message
