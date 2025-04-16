# This is the dealer ruleset for standing on any 17
# The dealer's move is determined by the sum of their hand
# We don't worry about 1 2 or 3 because they won't occur as they all deal with aces, which will take on the 11 value with a 2 or an ace
dealerstand17 = {
    "21" : "stand",
    "20" : "stand",
    "19" : "stand",
    "18" : "stand",
    "17" : "stand",
    "16" : "hit",
    "15" : "hit",
    "14" : "hit",
    "13" : "hit",
    "12" : "hit",
    "11" : "hit",
    "10" : "hit",
    "9" : "hit",
    "8" : "hit",
    "7" : "hit",
    "6" : "hit",
    "5" : "hit",
    "4" : "hit",
}