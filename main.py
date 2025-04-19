from deck import Deck
import dealerhit17
import basic_strategy
import dealerstand17
from hand import Hand
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
    for pcard1 in deck._initialDeck:
        probability = probability * (deck.getCard(dcard1) / deck.numCardsLeft()) # should just be 1/13
        deck.removeCard(pcard1)
        for dcard1 in deck._initialDeck:
            probability = probability * (deck.getCard(dcard1) / deck.numCardsLeft())
            deck.removeCard(dcard1)
            for pcard2 in deck._initialDeck:
                probability = probability * (deck.getCard(dcard1) / deck.numCardsLeft())
                deck.removeCard(pcard2)
                for dcard2 in deck._initialDeck:
                    probability = probability * (deck.getCard(dcard1) / deck.numCardsLeft())
                    deck.removeCard(dcard2)

                    player_hand = Hand([pcard1, pcard2])
                    dealer_hand = Hand([dcard1, dcard2])

                    totalEV += calculateEV(player_hand, dealer_hand, deck, probability, strategy, dealer_strategy)
    return totalEV

def calculateEV(player_hand: Hand, dealer_hand: Hand, deck: Deck, currentProb: float, strategy, dealer_strategy) -> float:
    #currentProb is the probability we are in the current state we are in

    # Hitting, Splitting are our Recursive cases
    # Blackjack, busting standing are our base cases. Doubling is just kinda there
    
    if player_hand.is_BJ:
        if not dealer_hand.is_BJ:
            return (1.5 * currentProb) # We are assuming blackjack pays 3:2
        else: # dealer has a BJ
            return 0
    
    if player_hand.is_bust:
        return (-1 * currentProb)
    
    action = determineAction(player_hand, dealer_hand) # Determine if we're hitting, standing, splitting, or doubling. Basic Strat

    stateEV = 0 # We will we adding up all the EVs from the various substates into this value

    if action == 1: # Hitting
        for card in deck._initialDeck:
            if deck.getCard(card) > 0:
                currentProb = currentProb * (deck.getCard(card) / deck.numCardsLeft())
                player_hand.add(card)
                deck.removeCard(card)
            stateEV += calculateEV(player_hand, dealer_hand, deck, currentProb, strategy, dealer_strategy) 
if __name__ == "__main__":
    main()