import cards 

class Deck:
    #Initializes the object with a copy of the cards dictionary
    def __init__(self):
        self._initialDeck = cards.cards.copy()
        
    # Removes one of the specified card from the dictionary, eg. (A = 3 -> A=2)
    # Updates the overall number of cards
    # Returns a boolean value that indicates whether it worked properly or not
    def removeCard(self, card):
        #Some basic error checking, ensuring that a card still remains
        if self._initialDeck.get(card) > 0:
            self._initialDeck[card] -= 1
            self._initialDeck["remaining"] -= 1
            return True
        return False
    
    # Returns the number of remaining cards 
    def numCardsLeft(self):
        return self._initialDeck.get("remaining")
    
    # Gets the number of cards remaining of a given value, eg. On a full deck card = "9" returns 4
    def getCard(self, card):
        return self._initialDeck.get(card)
