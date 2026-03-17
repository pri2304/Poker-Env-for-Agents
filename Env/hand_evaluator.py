from card import Card
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
    for suit in suit_counts:
        if len(suit_counts[suit]) >= 5:
            flush_suit = suit_counts[suit]
            suit = suit
            continue
    if 14 in flush_suit:
        flush_suit.append(1)

    flush_suit.sort(reverse=True)
    counter = 0
    index = 0
    final_run = []
    for i in flush_suit:
        try:
            if counter < 4:
                if i - 1 == flush_suit[index+1]:
                    counter += 1
                    final_run.append(i)
                else:
                    counter = 0
                    final_run = []
            elif counter == 4:
                final_run.append(i)
                counter += 1
            index += 1
        except IndexError:
            final_run = []
    final_run_ranks = {x: y for x, y in Card.rank_values.items() if y in final_run}

    if final_run:
        if 1 in final_run:
            ranks = list(final_run_ranks.keys())
            ranks.reverse()
            ranks.append('A')
            final_cards = [Card(suit, i) for i in ranks]
        else:
            ranks = list(final_run_ranks.keys())
            ranks.reverse()
            final_cards = [Card(suit, i) for i in ranks]
        return final_cards[0].value, final_cards
    else:
        return None

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

    if quad:
        return remaining_card.value, hand
    else:
        return None
