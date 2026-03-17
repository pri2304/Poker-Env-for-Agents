from card import Card
import random

class Deck:
    def __init__(self, num=52):
        self.num = num
        self.cards = []
        self.build_deck()

    def build_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '❤', '♦', '♣']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num=1):
        if num > len(self.cards):
            raise ValueError("Not enough cards in the deck!")
        dealt = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt
