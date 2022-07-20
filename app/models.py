from fastapi import HTTPException
from pydantic import BaseModel, Field, validator

POSSIBLE_HAND_VALUES = ("rock", "paper", "scissors")
POSSIBLE_RESULT_VALUES = (1, 0, -1)


class Hand(BaseModel):
    value: str = Field(alias="myHand")

    @validator("value")
    def hand_must_match_correct_values(cls, v):

        if v not in POSSIBLE_HAND_VALUES:
            raise HTTPException(
                status_code=400,
                detail=f"Incorrect hand value, should be either: {POSSIBLE_HAND_VALUES} ",
            )
        return v


class Play(BaseModel):
    player_hand: Hand
    ai_hand: Hand
    result: int

    @validator("result")
    def result_must_match_correct_values(cls, v):
        if v not in POSSIBLE_RESULT_VALUES:
            raise ValueError(
                f"Incorrect result value, should be either: {POSSIBLE_RESULT_VALUES}",
            )
        return v
