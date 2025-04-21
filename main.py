from deck import Deck, Card
import basic_strategy
from hand import Hand
import sys

sys.setrecursionlimit(50000)

def main():
    # Making the objects for the house rules and player strategies 
    basic_strategy_s_s17 = basic_strategy.basic_strategy_s_s17.copy()
    print("Given the nature of this program, running it will take a bit of time")


    ###############################################################
    #
    # This is the analysis for dealer stands any 17 vs basic strategy
    #
    ############################################################
    print("The anaylsis of basic strategy when dealer stands on every 17 resulted in: \n")
    print("House Edge: ", end='\r')
    stand_house_edge = getHouseEdge(basic_strategy_s_s17, "s_s17")
    print(stand_house_edge)

    print(f"The house edges we found are: when the dealer stands on s17 is {stand_house_edge * 100:.7f}%")


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
                    print(f"Player hand: {pcard1}, {pcard2} ; Dealer hand: {dcard1}, {dcard2}")
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

    if len(player_hand.cards) == 1: # You just splitm you have to take a card
        action = 1 # hit
    else:
        action = determineAction(player_hand, dealer_hand.getUpCard(), strategy) # Determine if we're hitting, standing, splitting, or doubling. Basic Strat

    stateEV = 0 # We will we adding up all the EVs from the various substates into this value

    if action == 1: # Hitting
        # with open("test.txt", "a") as f:
        #     f.write("hit\n")
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
        # with open("test.txt", "a") as f:
        #     f.write("stand\n")
        stateEV += dealer_draw(dealer_hand, player_hand, currentProb, deck, dealer_strategy)
    
    elif action == 3: # Doubling
        # with open("test.txt", "a") as f:
        #     f.write("doubling\n")
        for rank in deck._initialDeck.keys():
            if deck.getCard(rank) == 0:
                continue
            nextProb = currentProb * deck.getCard(rank) / deck.numCardsLeft()
            new_player_hand = Hand(player_hand.cards + [Card(rank)])

            deck.removeCard(rank)
            # After doubling the player stands
            ev_after = dealer_draw(dealer_hand, new_player_hand, nextProb, deck, dealer_strategy)
            stateEV += 2 * ev_after
            deck._initialDeck[rank] += 1
            deck.cardsLeft        += 1
    elif action == 4: # Splitting
        stateEV += calculateEV(Hand([player_hand.cards[0]]), dealer_hand, deck, currentProb, strategy, dealer_strategy) # can do this cause when you split you will only ever have 2 cards
        stateEV += calculateEV(Hand([player_hand.cards[1]]), dealer_hand, deck, currentProb, strategy, dealer_strategy)
        
    else: # should never get to here
        print("ERROR IN DETERMINE_ACTION")

    return stateEV
    

def dealer_draw(dealer_hand: Hand, player_hand: Hand, currentProb, deck, dealer_strategy):
    EV = 0
    if dealer_strategy == "s_s17":
        must_stand = dealer_hand.value() >= 17
    else: 
        val = dealer_hand.value()
        soft = dealer_hand.is_soft()
        must_stand = (val > 17) or (val == 17 and not soft)

    if must_stand:
        dealer_val = dealer_hand.value()
        player_val = player_hand.value()
        # Check player bust just in case, although should be caught earlier
        if player_hand.is_bust():
             return (-1 * currentProb)
        elif dealer_hand.is_bust(): # Dealer bust is win for player
            return (1 * currentProb)
        elif dealer_val > player_val: # Dealer wins
            return (-1 * currentProb)
        elif dealer_val == player_val: # Push
            return 0
        else: # Player wins
            return (1 * currentProb)

    # --- Recursive Case: Dealer Hits ---
    # Iterate through all possible cards the dealer can draw next
    for rank in list(deck._initialDeck.keys()):
        if deck.getCard(rank) > 0:
            drawProb = deck.getCard(rank) / deck.numCardsLeft()
            newProb = currentProb * drawProb 

            new_dealer_hand = Hand(dealer_hand.cards + [Card(rank)])

            deck.removeCard(rank)

            if new_dealer_hand.is_bust():
                EV += (1 * newProb) # Accumulate the EV contribution of this busting path
            else:
                # Dealer didn't bust, continue drawing recursively
                EV += dealer_draw(new_dealer_hand, player_hand, newProb, deck, dealer_strategy)

            deck._initialDeck[rank] += 1
            deck.cardsLeft += 1
    return EV

if __name__ == "__main__":
    main()