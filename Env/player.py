from hand_evaluator import evaluate_hand
from deck import Deck

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.folded = False
        self.current_bet = 0
        self.best_hand = None

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def fold(self):
        self.folded =True

    def reset_hand(self):
        self.hand = []
        self.folded = False
        self.current_bet = 0
        self.best_hand = []

    def bet(self, amount):
        if amount >= self.chips:
            amount = self.chips
            self.chips = 0
        else:
            self.chips -= amount

        self.current_bet += amount

    def call(self, highest_bet):
        amount_to_call = highest_bet - self.current_bet
        self.bet(amount_to_call)

    def check(self, round_bet):
        if round_bet == 0:
            return True
        else:
            return False

    def raise_to(self, raise_amount):
        if raise_amount <= self.current_bet:
            pass
        else:
            self.bet(raise_amount)

    def __str__(self):
        return f'name: {self.name} | current cards: {self.hand} | chips: {self.chips}'

    def evaluate_best_hand(self, board_cards):
        cards = self.hand + board_cards
        self.best_hand = evaluate_hand(cards)
