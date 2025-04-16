from deck import Deck, Card

class Hand:
    def __init__(self, cards: list[Card] = None):
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def add(self, card: Card):
        self.cards.append(card)

    def copy(self):
        return Hand(self.cards)
    
    def value(self) -> int:
        ace_num = 0
        total = 0
        for card in self.cards:
            if card.rank == 1:
                ace_num += 1
            else:
                total += card.rank
        
        total += ace_num
        if ace_num > 0 and total + 10 <= 21:
            total += 10

        return total
    
    def is_BJ(self) -> bool:
        if len(self.cards) == 2 and self.value() == 21:
            return True
        else:
            return False
        
    def is_bust(self) -> bool:
        return self.value() > 21
    
    def can_split(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank