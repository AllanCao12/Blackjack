from deck import Deck, Card

class Hand:
    def __init__(self, cards: list[Card] = None):
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def add(self, card: Card):
        self.cards.append(card)

    def getUpCard(self) -> Card:
        return self.cards[0]

    def copy(self):
        return Hand(self.cards)
    
    # converts current hand to usable input for basic strategy dictionary
    # returns int if hard total. returns str if pair or soft 
    def getHand(self):
        # if we're on first 2 cards
        if len(self.cards) == 2:
            # pair
            if self.can_split():
                if self.cards[0].rank == 1:
                    return "AA"
                elif self.cards[0].rank == 10:
                    return "TT"
                else:
                    return f"{self.cards[0].rank}{self.cards[0].rank}"
            # soft total
            elif self.cards[0].rank == 1 or self.cards[1].rank == 1:
                total = self.value()
                return f"{total}s" 
        # hard total
        return self.value()
    
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
    
    def is_soft(self) -> bool:
        total = sum(card.rank for card in self.cards)   # Aces counted as 1
        return any(card.rank == 1 for card in self.cards) and self.value() == total + 10
    
    def is_BJ(self) -> bool:
        if len(self.cards) == 2 and self.value() == 21:
            return True
        else:
            return False
        
    def is_bust(self) -> bool:
        return self.value() > 21
    
    def can_split(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank