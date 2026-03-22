from card import Card
def evaluate_hand(cards):
    rank_counts = get_rank_counts(cards)
    suit_counts = get_suit_counts(cards)

    result = check_straight_flush(cards, suit_counts)
    if result:
        return 8, result[0], result[1]

    result = check_four_of_a_kind(cards, rank_counts)
    if result:
        return 7, result[0], result[1]

    result = check_full_house(cards, rank_counts)
    if result:
        return 6, result[0], result[1]

    result = check_flush(cards, suit_counts)
    if result:
        return 5, result[0], result[1]

    result = check_straight(cards)
    if result:
        return 4, result[0], result[1]

    result = check_three_of_a_kind(cards, rank_counts)
    if result:
        return 3, result[0], result[1]

    result = check_two_pair(cards, rank_counts)
    if result:
        return 2, result[0], result[1]

    result = check_one_pair(cards, rank_counts)
    if result:
        return 1, result[0], result[1]

    top5 = sorted(cards, key=lambda Card:Card.value, reverse=True)[:5]
    return 0, [c.value for c in top5], top5

def get_rank_counts(cards):
    rank_counts = {}
    for card in cards:
        rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
    return rank_counts

def get_suit_counts(cards):
    suit_counts = {}
    for card in cards:
        suit_counts.setdefault(card.suit, []).append(card.value)
    return suit_counts

def check_straight_flush(cards, suit_counts):
    flush_suit = []
    hand = []
    for suit in suit_counts:
        if len(suit_counts[suit]) >= 5:
            flush_suit = suit_counts[suit]
            continue
    if 14 in flush_suit:
        flush_suit.append(1)

    flush_suit.sort(reverse=True)
    for i in range(len(flush_suit) - 1):
        run = flush_suit[i:i + 5]

        if max(run) - min(run) == 4 and len(run) == 5:
            run_val = run
            if 1 in run_val:
                run_val.append(14)
                run_val.remove(1)
            for c in cards:
                if c.value in run_val:
                    hand.append(c)
            break
    hand.sort(key=lambda Card: Card.value, reverse=True)
    rank_counts = get_rank_counts(hand)
    for rank in rank_counts:
        if rank_counts[rank] > 1:
            for c in hand:
                if c.value == rank:
                    hand.remove(c)
                    break

    if hand:
        if hand[0].value == 14 and hand[1].value == 5:
            hand.append(hand[0])
            hand = hand[1:]
        return hand[0].value, hand

def check_four_of_a_kind(cards, rank_counts):
    hand = []
    quad = None
    for rank in rank_counts:
        if rank_counts[rank] == 4:
            quad = rank
            break
        else:
            quad = None
    for card in cards:
        if quad == card.value:
            hand.append(card)

    remaining_card = max([card for card in cards if card.value != quad], key=lambda card: card.value)

    hand.append(remaining_card)

    tiebreakers = [quad] + [remaining_card.value]

    if quad:
        return tiebreakers, hand
    else:
        return None

def check_full_house(cards, rank_counts):
    hand = []
    triple = None
    pair = None
    triple_candidates = []
    pair_candidates = []

    for rank in rank_counts:
        if rank_counts[rank] == 3:
            triple_candidates.append(rank)
        if rank_counts[rank] >= 2:
            pair_candidates.append(rank)

    triple_candidates.sort(reverse=True)
    if triple_candidates:
        triple = triple_candidates[0]
    else:
        return None

    pair_candidates = [p for p in pair_candidates if p != triple]
    pair_candidates.sort(reverse=True)

    if pair_candidates:
        pair = pair_candidates[0]
    else:
        return None

    triple_cards = [card for card in cards if card.value == triple]
    pair_cards = [card for card in cards if card.value == pair]
    pair_cards = pair_cards[:2]

    hand = triple_cards + pair_cards

    if triple and pair:
        return [triple, pair], hand

def check_flush(cards, suit_counts):
    flush_suit = []
    suit_selected = None

    for suit in suit_counts:
        if len(suit_counts[suit]) >= 5:
            flush_suit = suit_counts[suit]
            suit_selected = suit

    if not suit_selected:
        return None

    flush_suit.sort(reverse=True)
    flush_suit = flush_suit[:5]

    hand = [card for card in cards if card.suit == suit_selected]
    hand.sort(key=lambda Card: Card.value, reverse=True)
    hand = hand[:5]

    if flush_suit:
        return flush_suit, hand

def check_straight(cards):
    ranks = sorted({card.value for card in cards}, reverse=True)
    hand = []
    if 14 in ranks:
        ranks.append(1)
    for i in range(len(ranks) -1):
        run = ranks[i:i + 5]

        if max(run) - min(run) == 4 and len(run) == 5:
            run_val = run
            if 1 in run_val:
                run_val.append(14)
                run_val.remove(1)
            for c in cards:
                if c.value in run_val:
                    hand.append(c)
            break
    hand.sort(key=lambda Card: Card.value, reverse=True)
    rank_counts = get_rank_counts(hand)
    for rank in rank_counts:
        if rank_counts[rank] > 1:
            for c in hand:
                if c.value == rank:
                    hand.remove(c)
                    break

    if hand:
        if hand[0].value == 14 and hand[1].value == 5:
            hand.append(hand[0])
            hand = hand[1:]
        return hand[0].value, hand

def check_three_of_a_kind(cards, rank_counts):
    hand = []
    triple = None
    for rank in rank_counts:
        if rank_counts[rank] == 3:
            triple = rank

    for card in cards:
        if card.value == triple:
            hand.append(card)

    kicker_cards = [card for card in cards if card.value != triple]
    kicker_cards.sort(key= lambda Card:Card.value, reverse=True)
    kicker_cards = kicker_cards[:2]
    hand = hand + kicker_cards
    tiebreaker = [triple] + [c.value for c in kicker_cards]

    if triple:
        return  tiebreaker, hand

def check_two_pair(cards, rank_counts):
    hand = []
    pairs = []
    for rank in rank_counts:
        if rank_counts[rank] == 2:
            pairs.append(rank)

    pairs.sort(reverse=True)
    pairs = pairs[:2]

    for pair in pairs:
        for card in cards:
            if card.value == pair:
                hand.append(card)

    kickers = [card for card in cards if card.value not in pairs]
    kickers.sort(key=lambda Card:Card.value, reverse=True)
    kicker = kickers[0]

    hand.append(kicker)

    tiebreakers = pairs + [kicker.value]

    if len(pairs) > 1:
        return tiebreakers, hand

def check_one_pair(cards, rank_counts):
    pair = None
    hand = []
    for rank in rank_counts:
        if rank_counts[rank] == 2:
            pair = rank

    for card in cards:
        if card.value == pair:
            hand.append(card)

    kickers = [card for card in cards if card.value != pair]
    kickers.sort(key = lambda Card:Card.value, reverse=True)
    kickers = kickers[:3]

    kicker_values = [card.value for card in kickers]

    tiebreaker = [pair] + kicker_values

    hand = hand + kickers

    if pair:
        return tiebreaker, hand

def format_hand(rank_value, tiebreakers):
    RANK_NAMES = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
                  11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}

    def name_card(value):
        return RANK_NAMES.get(value, str(value))

    if rank_value == 8:
        if tiebreakers == 14:
            return f"Royal Flush"
        return f"Straight Flush, {name_card(tiebreakers)}-high"

    if rank_value == 7:
        return f"Four of a Kind, {name_card(tiebreakers[0])}s with {name_card(tiebreakers[1])} kicker"

    if rank_value == 6:
        return f"Full House, {name_card(tiebreakers[0])}s over {name_card(tiebreakers[1])}s"

    if rank_value == 5:
        cards = ', '.join(name_card(v) for v in tiebreakers)
        return f"Flush, high cards {cards}"

    if rank_value == 4:
        return f"Straight, {name_card(tiebreakers)}-high"

    if rank_value == 3:
        kickers = ', '.join(name_card(v) for v in tiebreakers[1:])
        return f"Three of a Kind, {name_card(tiebreakers[0])}s with kickers {kickers}"

    if rank_value == 2:
        kicker = name_card(tiebreakers[2])
        return f"Two Pair, {name_card(tiebreakers[0])}s and {name_card(tiebreakers[1])}s with kicker {kicker}"

    if rank_value == 1:
        kickers = ', '.join(name_card(v) for v in tiebreakers[1:])
        return f"One Pair, {name_card(tiebreakers[0])}s with kickers {kickers}"

    if rank_value == 0:
        cards = ', '.join(name_card(v) for v in tiebreakers)
        return f"High Card, {cards}"

    return None