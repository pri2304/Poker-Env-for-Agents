import random

from hand_evaluator import evaluate_hand

class Player:
    def __init__(self, name, decisionmaker, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.folded = False
        self.current_bet = 0
        self.best_hand = None
        self.decisionmaker = decisionmaker
        self.allin = False

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def fold(self):
        self.folded = True

    def reset_hand(self):
        self.hand = []
        self.folded = False
        self.current_bet = 0
        self.best_hand = []

    def bet(self, amount):
        if amount >= self.chips:
            amount = self.chips
            self.chips = 0
            self.allin = True
        else:
            self.chips -= amount

        self.current_bet += amount

    def call(self, highest_bet):
        amount_to_call = highest_bet - self.current_bet
        if amount_to_call > self.chips:
            amount_to_call = self.chips
        self.bet(amount_to_call)
        return amount_to_call

    def check(self, round_bet):
        if round_bet == 0:
            return True
        elif round_bet == self.current_bet:
            return True
        else:
            return False

    def raise_to(self, raise_amount, current_bet):
        min_amount = current_bet - self.current_bet
        if raise_amount <= min_amount:
            return None
        else:
            final_bet = raise_amount - self.current_bet
            if raise_amount > self.chips:
                raise_amount = self.chips + self.current_bet
            self.bet(final_bet)
            return raise_amount

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def evaluate_best_hand(self, board_cards):
        cards = self.hand + board_cards
        if len(cards) == 7:
            self.best_hand = evaluate_hand(cards)
            return self.best_hand
        else:
            return None


class DecisionMaker:
    def __init__(self):
        self.state = None
    def get_action(self, state):
        self.state = state

class RandomDecisionMaker(DecisionMaker):
    def get_action(self, state):
        print(f"Player Name: {state['Player']}")
        select = random.choice(['call', 'check', 'fold', 'raise'])
        if select == 'raise':
            amount = random.randint(0, state['Chips'])
            return select, amount
        else:
            return select, 0

class HumanDecisionMaker(DecisionMaker):
    def get_action(self, state):
        print(f"Player Name: {state['Player']}")
        print(f"Your Hand is {state['Hand']}. \nYour current bet is {state['Player Bet']}. \nCurrent table bet is {state['Table Current Bet Amount']}. \nYou have {state['Chips']} chips. \nCommunity Cards are {state['Community Cards']}. \nCurrent main pot is {state['Main Pot']}.")
        if state['Side Pots']:
            print("Side Pots are:")
        for pot in state['Side Pots']:
            print(f"Players in side pot are {pot['Players']} and side pot amount is {pot['Pot']}")
        for player in state['Player Details']:
            if not player['Player Folded']:
                print(f"Player {player['Player Name']} has currently bet {player['Player Bet']} and has {player['Player Chips']} chips")
        select = input("Please select an option (Check/Fold/Call/Raise): ").strip().lower()
        if select == 'raise':
            amount = int(input("Please enter amount you want to raise to: "))
            return select, amount
        else:
            return select, 0