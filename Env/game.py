from deck import Deck
from player import Player, DecisionMaker, HumanDecisionMaker, RandomDecisionMaker

class PokerGame:
    def __init__(self, players, small_blind=10, big_blind=20):
        self.players = [player for player in players]
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.dealer = 0
        self.pot = 0
        self.pots = []
        self.current_bet = 0
        self.street = "preflop"
        self.small_blind_amount = small_blind
        self.big_blind_amount = big_blind

    def deal_initial_hands(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def deal_flop(self):
        self.street = "flop"
        self.deck.deal(1)
        self.community_cards.extend(self.deck.deal(3))

    def deal_turn(self):
        self.street = "turn"
        self.deck.deal(1)
        self.community_cards.extend(self.deck.deal(1))

    def deal_river(self):
        self.street = "river"
        self.deck.deal(1)
        self.community_cards.extend(self.deck.deal(1))

    def post_blinds(self):
        num_players = len(self.players)
        sb_pos = (self.dealer + 1) % num_players
        bb_pos = (self.dealer + 2) % num_players

        self.players[sb_pos].bet(self.small_blind_amount)
        self.pot += self.small_blind_amount
        print(f"{self.players[sb_pos].name} posted small blind for {self.small_blind_amount}")

        self.players[bb_pos].bet(self.big_blind_amount)
        self.pot += self.big_blind_amount
        print(f"{self.players[bb_pos].name} posted big blind for {self.big_blind_amount}")

        print(f"Pot: {self.pot}")
        self.current_bet = self.big_blind_amount

    def hand_end(self):
        num_players = len(self.players)
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.dealer = (self.dealer + 1) % num_players
        self.players = self.players[self.dealer:] + self.players[:self.dealer]
        self.pot = 0
        self.pots = []
        self.current_bet = 0
        self.street = "preflop"
        for player in self.players:
            player.reset_hand()

    def player_action(self, player, action, amount):
        if action == 'fold':
            player.fold()
            return 0
        elif action == 'check':
            if self.current_bet == self.big_blind_amount:
                if player.check(self.current_bet) is True:
                    return 0
                else:
                    return None
            else:
                if player.check(self.current_bet) is True:
                    return 0
                else:
                    return None
        elif action == 'call':
            return player.call(self.current_bet)
        elif action == 'raise':
            amount = player.raise_to(amount, self.current_bet)
            self.current_bet = player.current_bet
            return amount

    def player_state(self, player_name):
        player_details = []
        hand = None
        chips = 0
        player_current_bet = 0
        best_hand = None
        for player in self.players:
            if player.name == player_name:
                hand = player.hand
                chips = player.chips
                player_current_bet = player.current_bet
                best_hand = player.best_hand
            else:
                player_dict = {"Player Name": player.name, "Player Folded":player.folded, "Player Bet": player.current_bet, "Player Chips": player.chips}
                player_details.append(player_dict)
        state = {"Player" : player_name,
                 "Hand" : hand,
                 "Chips" : chips,
                 "Player Bet" : player_current_bet,
                 "Best Hand" : best_hand,
                 "Community Cards" : self.community_cards,
                 "Main Pot" : self.pot,
                 "Side Pots" : self.pots,
                 "Table Current Bet Amount" : self.current_bet,
                 "Player Details" : player_details,
                 "Current Street" : self.street}
        return state

    def player_response(self, player):
        response = player.decisionmaker.get_action(self.player_state(player.name))
        amount = self.player_action(player, response[0], response[1])
        if amount is None:
            print("Invalid Response")
            return self.player_response(player)
        else:
            if response[0] == 'call':
                print(f"Player {response[0]}ed for {amount}")
            elif response[0] == 'raise':
                print(f"Player {response[0]}d to {amount}")
            else:
                print(f"Player {response[0]}ed")
            return amount

    def create_side_pots(self, players):
        for p in players:
            leftover = 0
            player_list = []
            if p.allin:
                bet_to_match = p.current_bet
                for player in players:
                    if player.current_bet >= p.current_bet:
                        player_list.append(player)
                        leftover += player.current_bet - bet_to_match
                        player.current_bet -= bet_to_match
                pot = {'Players': player_list, 'Pot': self.pot}
                self.pots.append(pot)
                self.pot = leftover



    def player_betting_round(self):
        players_in = [player for player in self.players if not player.folded or player.chips <= 0 and not player.allin]
        c = 0
        if self.street == 'preflop':
            self.post_blinds()
            player_order = self.players[self.dealer+3:] + self.players[:self.dealer+3]
        else:
            player_order = self.players[self.dealer+1:] + self.players[:self.dealer+1]
        for p in player_order:
            if p.folded or p.chips <=0:
                player_order.remove(p)
        while c != len(player_order) and len(players_in) > 1:
            running_table_bet = self.current_bet
            for p in player_order:
                self.pot += self.player_response(p)
                if p.folded or p.chips <= 0:
                    player_order.remove(p)
                if p.folded:
                    players_in.remove(p)
                if p.current_bet == running_table_bet:
                    c += 1
                else:
                    c = 0
                if c == len(player_order):
                    break
        self.create_side_pots(players_in)
        for p in players_in:
            if p.folded or p.chips <= 0:
                players_in.remove(p)
        self.current_bet = 0
        for p in self.players:
            p.current_bet = 0

        if self.street == 'river':
            if len(players_in) == 1:
                players_in[0].chips += self.pot
            else:
                self.final_showdown(players_in)

    def hand_evaluation(self, players):
        for p in players:
            p.evaluate_best_hand(self.community_cards)
        winning_hand = max((p.best_hand[0], p.best_hand[1]) for p in players)
        winners = [p for p in players if (p.best_hand[0], p.best_hand[1]) == winning_hand]
        return winners

    def final_showdown(self, players):
        if self.pots:
            for pot in self.pots:
                winners = self.hand_evaluation(pot['Players'])
                winning_amount = pot['Pot'] / len(winners)
                winning_amount_remainder = pot['Pot'] % len(winners)

                for winner in winners:
                    winner.chips += winning_amount

                if winning_amount_remainder:
                    order = [p for p in self.players if p in winners]
                    while winning_amount_remainder != 0:
                        for w in order:
                            w.chips += 1
                            if winning_amount_remainder == 0:
                                break

        winners = self.hand_evaluation(players)
        winning_amount = self.pot / len(winners)
        winning_amount_remainder = self.pot % len(winners)

        for winner in winners:
            winner.chips += winning_amount

        if winning_amount_remainder:
            order = [p for p in self.players if p in winners]
            while winning_amount_remainder != 0:
                for w in order:
                    w.chips += 1
                    if winning_amount_remainder == 0:
                        break









players_ = [Player('pri', HumanDecisionMaker(), chips=100), Player('het', HumanDecisionMaker()), Player('meet', HumanDecisionMaker())]
game = PokerGame(players_)
game.deal_initial_hands()
print(game.community_cards)
game.player_betting_round()
game.deal_flop()
print(game.community_cards)
game.player_betting_round()
game.deal_turn()
print(game.community_cards)
game.player_betting_round()
game.deal_river()
print(game.community_cards)
game.player_betting_round()
print(game.players)





