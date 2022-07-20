from app.models import Hand

from ..core import calculate_result


class TestCalculateResult:
    """testing games rules"""

    rock_hand = Hand(myHand="rock")
    paper_hand = Hand(myHand="paper")
    scissors_hand = Hand(myHand="scissors")

    def test_calculate_result_should_be_a_tie(self):
        assert calculate_result(self.rock_hand, self.rock_hand) == 0
        assert calculate_result(self.paper_hand, self.paper_hand) == 0
        assert calculate_result(self.scissors_hand, self.scissors_hand) == 0

    def test_calculate_result_player_should_win(self):
        assert calculate_result(self.rock_hand, self.scissors_hand) == 1
        assert calculate_result(self.paper_hand, self.rock_hand) == 1
        assert calculate_result(self.scissors_hand, self.paper_hand) == 1

    def test_calculate_result_player_should_loses(self):
        assert calculate_result(self.rock_hand, self.paper_hand) == -1
        assert calculate_result(self.paper_hand, self.scissors_hand) == -1
        assert calculate_result(self.scissors_hand, self.rock_hand) == -1
