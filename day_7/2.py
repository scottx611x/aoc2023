import enum
import time
from functools import cached_property

start = time.time()


class CamelCardHandType(str, enum.Enum):
    FIVE_OF_A_KIND = "FIVE_OF_A_KIND"
    FOUR_OF_A_KIND = "FOUR_OF_A_KIND"
    FULL_HOUSE = "FULL_HOUSE"
    THREE_OF_A_KIND = "THREE_OF_A_KIND"
    TWO_PAIR = "TWO_PAIR"
    ONE_PAIR = "ONE_PAIR"
    HIGH_CARD = "HIGH_CARD"


CARD_RANK = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
HAND_RANK = [hand for hand in CamelCardHandType]


class CamelCardHand:
    def __init__(self, hand: str, bid: str):
        self.hand = hand
        self.bid = int(bid)

    def __repr__(self):
        return f"<🐪🃏: hand: {self.hand} type: {self.type} bid: {self.bid}>"

    def __lt__(self, other: "CamelCardHand") -> bool:
        hand_rank = HAND_RANK.index(self.type)
        other_hand_rank = HAND_RANK.index(other.type)

        if hand_rank == other_hand_rank:
            for idx, card in enumerate(self.hand):
                if card == other.hand[idx]:
                    continue

                card_rank = CARD_RANK.index(card)
                other_card_rank = CARD_RANK.index(other.hand[idx])

                return card_rank > other_card_rank

        return HAND_RANK.index(self.type) < HAND_RANK.index(other.type)

    @cached_property
    def type(self) -> CamelCardHandType:
        card_counts = {i: self.hand.count(i) for i in self.hand}
        jokers = card_counts.get("J", 0)

        if any(i == 5 for i in card_counts.values()):
            return CamelCardHandType.FIVE_OF_A_KIND

        for k, v in reversed(sorted(card_counts.items(), key=lambda item: item[1])):
            if k == "J":
                continue

            if v + jokers == 5:
                return CamelCardHandType.FIVE_OF_A_KIND
            if v + jokers == 4:
                return CamelCardHandType.FOUR_OF_A_KIND
            if v + jokers == 3:
                if any(j == 2 and i not in [k, "J"] for i, j in card_counts.items()):
                    return CamelCardHandType.FULL_HOUSE
                else:
                    return CamelCardHandType.THREE_OF_A_KIND
            if v + jokers == 2:
                if any(j == 3 and i not in [k, "J"] for i, j in card_counts.items()):
                    return CamelCardHandType.FULL_HOUSE
                elif any(j == 2 and i != k for i, j in card_counts.items()):
                    return CamelCardHandType.TWO_PAIR
                else:
                    return CamelCardHandType.ONE_PAIR
        return CamelCardHandType.HIGH_CARD


with open("input.txt") as f:
    camel_card_hands = [
         CamelCardHand(*line.split()) for line in f.readlines()
    ]


total_winnings = 0

for idx, hand in enumerate(reversed(sorted(camel_card_hands))):
    total_winnings += hand.bid * (idx + 1)

print(f'Total winnings: {total_winnings}')
print('It took', time.time() - start, 'seconds.')