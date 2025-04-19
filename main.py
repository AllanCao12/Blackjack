from deck import Deck, Card
import dealerhit17
import basic_strategy
import dealerstand17
from hand import Hand
import sys

sys.setrecursionlimit(500000)

def main():
    # Making the objects for the house rules and player strategies 
    dealer_hit_soft_17 = dealerhit17.dealerhit17.copy()
    dealer_stand_17 = dealerstand17.dealerstand17.copy()
    player_basic_strategy = basic_strategy.basic_strategy.copy()

    print("Given the nature of this program, running it will take a bit of time | Estimated: --h --mins")


    ###############################################################
    #
    # This is the analysis for dealer stands any 17 vs basic strategy
    #
    ############################################################
    print("The anaylsis of basic strategy when dealer stands on every 17 resulted in: \n")
    print("House Edge: ", end='\r')
    # getHouseEdge() runs the state machine with the given house ruleset and player strategy and returns the resulting house edge
    house_edge = getHouseEdge(player_basic_strategy, dealer_stand_17)
    print(house_edge)

    ###############################################################
    #
    # This is the analysis for: dealer hits on soft 17 vs basic strategy
    #
    ############################################################
    print("The anaylsis of basic strategy when dealer hits on soft 17 resulted in: \n")
    print("House Edge: ", end='\r')
    # getHouseEdge() runs the state machine with the given house ruleset and player strategy and returns the resulting house edge
    house_edge = getHouseEdge(player_basic_strategy, dealer_hit_soft_17)
    print(house_edge)


def getHouseEdge(strategy, dealer_strategy):
    totalEV = 0
    deck = Deck()
    probability = 1
    for pcard1 in list(deck._initialDeck.keys()):
        probabilityP1 = probability * (deck.getCard(pcard1) / deck.numCardsLeft()) # should just be 1/13
        deck.removeCard(pcard1)
        for dcard1 in list(deck._initialDeck.keys()):
            probabilityD1 = probabilityP1 * (deck.getCard(dcard1) / deck.numCardsLeft())
            deck.removeCard(dcard1)
            for pcard2 in list(deck._initialDeck.keys()):
                probabilityP2 = probabilityD1 * (deck.getCard(pcard2) / deck.numCardsLeft())
                deck.removeCard(pcard2)
                for dcard2 in list(deck._initialDeck.keys()):
                    probabilityD2 = probabilityP2 * (deck.getCard(dcard2) / deck.numCardsLeft())
                    deck.removeCard(dcard2)

                    player_hand = Hand([Card(pcard1), Card(pcard2)])
                    dealer_hand = Hand([Card(dcard1), Card(dcard2)])

                    totalEV += calculateEV(player_hand, dealer_hand, deck, probabilityD2, strategy, dealer_strategy)
                    deck._initialDeck[dcard2] += 1
                    deck.cardsLeft += 1
                deck._initialDeck[pcard2] += 1
                deck.cardsLeft += 1
            deck._initialDeck[dcard1] += 1
            deck.cardsLeft += 1
        deck._initialDeck[pcard1] += 1
        deck.cardsLeft += 1
    return totalEV

def determineAction(player_hand: Hand, dealer_upcard: Card, strategy) -> int:
    return strategy[player_hand.getHand()][dealer_upcard.rank]
    
def calculateEV(player_hand: Hand, dealer_hand: Hand, deck: Deck, currentProb: float, strategy, dealer_strategy) -> float:
    #currentProb is the probability we are in the current state we are in

    # Hitting, Splitting are our Recursive cases
    # Blackjack, busting standing are our base cases. Doubling is just kinda there
    
    if player_hand.is_BJ():
        if not dealer_hand.is_BJ():
            return (1.5 * currentProb) # We are assuming blackjack pays 3:2
        else: # dealer has a BJ
            return 0
    
    if player_hand.is_bust() or dealer_hand.is_BJ():
        return (-1 * currentProb)

    action = determineAction(player_hand, dealer_hand.getUpCard(), strategy) # Determine if we're hitting, standing, splitting, or doubling. Basic Strat

    stateEV = 0 # We will we adding up all the EVs from the various substates into this value

    if action == 1: # Hitting
        for rank in list(deck._initialDeck.keys()):
            if deck.getCard(rank) > 0:
                newProb = currentProb * (deck.getCard(rank) / deck.numCardsLeft())
                new_player_hand = Hand(player_hand.cards + [Card(rank)])
                deck.removeCard(rank)
                stateEV += calculateEV(new_player_hand, dealer_hand, deck, newProb, strategy, dealer_strategy)
                deck._initialDeck[rank] += 1
                deck.cardsLeft += 1
            else:
                continue
    elif action == 2: # Standing
        stateEV += dealer_draw(dealer_hand, player_hand, currentProb, deck)
    
    elif action == 3: # Doubling
        stateEV += 2 * calculateEV(player_hand, dealer_hand, deck, currentProb, strategy, dealer_strategy)
    elif action == 4: # Splitting
        stateEV += calculateEV(Hand([player_hand.cards[0]]), dealer_hand, deck, currentProb, strategy, dealer_strategy) # can do this cause when you split you will only ever have 2 cards
        stateEV += calculateEV(Hand([player_hand.cards[1]]), dealer_hand, deck, currentProb, strategy, dealer_strategy)
    else: # should never get to here
        print("ERROR IN DETERMINE_ACTION")

    return stateEV
    

def dealer_draw(dealer_hand, player_hand, currentProb, deck):
    EV = 0
    if dealer_hand.value() >= 17: # Dealer stands on soft 17
        if dealer_hand.value() > player_hand.value():
            return (-1 * currentProb)
        elif dealer_hand.value() == player_hand.value(): # Push
            return 0
        else: # Player won
            return (1 * currentProb)
        
    for rank in list(deck._initialDeck.keys()):
        if deck.getCard(rank) > 0:
            newProb = currentProb * (deck.getCard(rank) / deck.numCardsLeft())
            new_dealer_hand = Hand(dealer_hand.cards + [Card(rank)])

            deck.removeCard(rank)

            if new_dealer_hand.is_bust():
                deck._initialDeck[rank] += 1
                deck.cardsLeft += 1
                return (1 * newProb)
            # We've drawn a card and the dealer didn't bust. Time to recursive call and find out if we won or keep hitting
                    
            EV += dealer_draw(new_dealer_hand, player_hand, newProb, deck)

            deck._initialDeck[rank] += 1
            deck.cardsLeft += 1
    # For those cases that haven't returned yet, return the total EV of all substates
    return EV

if __name__ == "__main__":
    main()