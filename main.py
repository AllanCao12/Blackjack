import deck
import dealerhit17
import basic_strategy
import dealerstand17

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



if __name__ == "__main__":
    main()