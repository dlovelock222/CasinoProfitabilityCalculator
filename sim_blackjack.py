# region : Imports
import random
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import time
# endregion

# region : Game and Simulation Settings

# Define table rules and people
NUM_PLAYERS = int(input("Enter in # of players: "))
#NUM_PLAYERS = 5
BLACKJACK_PAYOUT = 1.2
MAX_SPLITS_ALLOWED = 3
DECKS = 6

#CHANGE THESE TO RUN DIFF SIM
HANDS_IN_NIGHT = int(input("Enter in how many hands per night including dealer: "))
SIM_NIGHTS = int(input("Enter the number of simulation nights: "))
printing_nights = input("Print nightly results? (Yes/No): ").lower() == 'yes'
#HANDS_IN_NIGHT = 200 #INCLUDING DEALER
#SIM_NIGHTS = 100
#printing_nights = False

#BANKROLL / BUYIN INFO
BANK_PUSH = int(input("Enter the bank push amount: "))
BUYIN = int(input("Enter the total buy-in amount: "))
MIN_PUSH = int(input("Enter the minimum push amount: "))
print('\n\n')
#BANK_PUSH = 4000
#BUYIN = 6000
#MIN_PUSH = 2000
EXTRA_BACKUP_CHIPS = BUYIN - BANK_PUSH
bankroll_points = []

# endregion

# region : Create Basic Strategy Charts

player_values_hard = list(range(4, 21))
dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Basic strategy decisions: H (Hit), S (Stand), D (Double), SUR (Surrender), SP (Split)
basic_strategy_hard = [
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 4
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 5
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 6
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 7
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 8
['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 9
['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # Player value 10
['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],  # Player value 11
['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 12
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 13
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 14
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 15
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value 16
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],   # Player value 17
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],   # Player value 18
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],   # Player value 19
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']   # Player value 20
]

player_values_soft = list(range(13, 21))
# Basic strategy decisions: H (Hit), S (Stand), D (Double), SUR (Surrender), SP (Split)
basic_strategy_soft = [
['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value A,2
['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value A,3
['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value A,4
['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value A,5
['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # Player value A,6 #done until this point
['D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H', 'H', 'H', 'H'],   # Player value A,7
['S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],   # Player value A,8
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],   # Player value A,9
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']   # Player value A,10/J/Q/K
]

player_values_pairs = list(range(4, 21))
# Basic strategy decisions: H (Hit), S (Stand), D (Double), SUR (Surrender), SP (Split)
basic_strategy_pair = [
['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # Player value 2,2
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 5
['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # Player value 3,3
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 7
['N', 'N', 'N', 'SP', 'SP', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # Player value 4,4
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 9
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # Player value 5,5
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 11
['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP'],  # Player value A,A
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 13
['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # Player value 7,7
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 15
['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP'],  # Player value 8,8
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 17
['SP', 'SP', 'SP', 'SP', 'SP', 'N', 'SP', 'SP', 'N', 'N', 'N', 'N', 'N'],  # Player value 9,9
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # DUMMY ROW 19
['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  # Player value 10,10 (J/Q/K also)
]

# Create the 2D array for basic strategy decisions
basic_strategy_hard_array = dict(zip(player_values_hard, basic_strategy_hard))
basic_strategy_soft_array = dict(zip(player_values_soft, basic_strategy_soft))
basic_strategy_pair_array = dict(zip(player_values_pairs, basic_strategy_pair))

# endregion

# region : Bet sizes and helper functions

def create_shoe():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = ranks * DECKS * 4 #4 is for the suits
    random.shuffle(deck)
    return deck

def calculate_drop(total_bet):
    drop = 0
    if total_bet < 25:
        drop = -2
    elif total_bet >= 25 and total_bet <= 300:
        drop = -3
    elif total_bet >= 300 and total_bet <= 500:
        drop = -4
    else:
        drop = -5
    return drop

# Function to calculate the value of a hand PLAYER
def calculate_hand_value(hand):
    value = 0
    num_11_aces = 0
    num_aces = 0
    hard_or_soft = 'Hard'
    
    for card in hand:
        if card in ['J', 'Q', 'K']:
            value += 10
        elif card == 'A':
            num_11_aces += 1
            num_aces += 1
            value += 11
        else:
            value += int(card)
    
    while value > 21 and num_11_aces > 0:
        value -= 10
        num_11_aces -= 1
    
    if num_aces >= 1 and num_aces - num_11_aces == 0 and value != 21 and value < 21:
        hard_or_soft = 'Soft'

    return value, hard_or_soft

def generate_bj_bet_size():
    buster_bet_size = {
    100: 1
    # 5: 0.2,
    # 10: 0.1,
    # 15: 0.1,
    # 20: 0.1,
    # 30: 0.1,
    # 40: 0.1,
    # 50: 0.1,
    # 60: 0.1,
    # 80: 0.05,
    # 100: 0.05
    }
    
    random_number = random.choices(list(buster_bet_size.keys()), weights=list(buster_bet_size.values()))[0]
    return(random_number)

def generate_buster_bet_size():
    buster_bet_size = {
    50: 1
    # 0: 0.2,
    # 5: 0.2,
    # 10: 0.3,
    # 15: 0.1,
    # 20: 0.1,
    # 30: 0.1
    }

    random_number = random.choices(list(buster_bet_size.keys()), weights=list(buster_bet_size.values()))[0]
    return(random_number)

def is_blackjack(hand):
    return len(hand) == 2 and 'A' in hand and any(card in ['10', 'J', 'Q', 'K'] for card in hand)

def buster_payout_calc(bet, hand):
    bust_cards = len(hand)
    if bust_cards == 3 or bust_cards == 4:
        multiplier = 2
    elif bust_cards == 5:
        multiplier = 4
    elif bust_cards == 6:
        multiplier = 12
    elif bust_cards == 7:
        multiplier = 50
    elif bust_cards >= 8:
        multiplier = 200
    else:
        multiplier = 0

    payout = bet * multiplier
    return payout

# endregion

# Main game loop
def play_blackjack():

    # region : Basic Strategy Functions using Deck (must stay inside play_blackjack function)

    def basic_strategy(player_hands, player_hand_value, dealer_hand):

        dealer_up = dealer_hand[0]
        decisions = []
        played_hands = []
        i = 0

        for hand in player_hands:

            player_hand = hand[0]
            player_hand_value = hand[1]  #Reassign the hand and value while iterating. Remove it from tuple.

            if len(player_hand) == 1: 
                player_hand = [player_hand[0], (deck.pop())]
                player_hand_value = calculate_hand_value(player_hand)
            
            if len(player_hand) == 2 and player_hand[0] == player_hand[1] and len(player_hands) <= MAX_SPLITS_ALLOWED:  #CASINO HAS MAX SPLIT
                    if bs_pairs(player_hand, player_hand_value, dealer_up) == "SP":
                        player_hands.append([player_hand[1], calculate_hand_value(player_hand[1])]) #adding a new hand and have to also add the value because the hand is a tuple. [1] is the second card
                        player_hand = [player_hand[0], (deck.pop())] #only take the first card of the pair
                        player_hand_value = (calculate_hand_value(player_hand)) #recalc value
            

            # THE POINT OF NO RETURN
            decision = 'Play'
            decisions.append('Play')

            while decisions[i] not in ['S', 'SUR', 'D'] and player_hand_value[0] < 21:
        
                if player_hand_value[1] == "Soft":
                    player_hand, player_hand_value, decision = bs_soft_totals(player_hand, player_hand_value, dealer_up)
                    decisions[i] = decision

                elif (player_hand_value[0] == 16 and len(player_hand) == 2 and dealer_up in ['9', '10', 'J', 'Q', 'K', 'A']) or (player_hand_value[0] == 15 and len(player_hand) == 2 and dealer_up in ['10', 'J', 'Q', 'K']):
                    decisions[i] = 'SUR'
                else:
                    player_hand, player_hand_value, decision = bs_hard_totals(player_hand, player_hand_value, dealer_up)
                    decisions[i] = decision
            
            played_hands.append((player_hand, player_hand_value))

            if is_blackjack(player_hand):
                decisions[i] = 'BJ Already'

            i += 1




        # print("PLAYED_HANDS:", played_hands)
        # print("PLAYED HANDS VALUE", player_hand_value)
        # print("DECISIONS", decisions)
        return played_hands, player_hand_value, decisions

    def bs_pairs(player_hand, player_hand_value, dealer_up):
        return basic_strategy_pair_array[player_hand_value[0]][dealer_upcards.index(dealer_up)]
        
    def bs_soft_totals(player_hand, player_hand_value, dealer_up):
        # Simulate a decision based on player value and dealer up card
        decision = basic_strategy_soft_array[player_hand_value[0]][dealer_upcards.index(dealer_up)]
        if decision == "H" or (decision == 'D' and len(player_hand) != 2):
            player_hand.append(deck.pop())
            player_hand_value = calculate_hand_value(player_hand)
            decision = "H"

        elif decision == "D" and len(player_hand) == 2: #can only double when you have two cards
            player_hand.append(deck.pop())
            player_hand_value = calculate_hand_value(player_hand)

        else:
            decision = 'S'

        return(player_hand, player_hand_value, decision)
    
    def bs_hard_totals(player_hand, player_hand_value, dealer_up):

        # Simulate a decision based on player value and dealer up card
        decision = basic_strategy_hard_array[player_hand_value[0]][dealer_upcards.index(dealer_up)]

        if decision == "H" or (decision == 'D' and len(player_hand) != 2):
            player_hand.append(deck.pop())
            player_hand_value = calculate_hand_value(player_hand)
            decision = "H"

        elif decision == "D" and len(player_hand) == 2: #can only double when you have two cards
            player_hand.append(deck.pop())
            player_hand_value = calculate_hand_value(player_hand)

        elif decision == "SUR":
            decision = 'SUR'

        else:
            decision = 'S'

        return(player_hand, player_hand_value, decision)
    # endregion
    
    # region : Sim wide statistics and variables
    nights = 0
    sim_bankrupts = []
    sim_total_profits = []
    sim_bj_profit = []
    sim_buster_profit = []
    sim_buster_data = []

    sim_bj_counter = []
    sim_wins_counter = []
    sim_losses_counter = []
    sim_pushes_counter = []
    sim_surrender_counter = []
    sim_bjpush_counter = []
    # endregion

    while nights < SIM_NIGHTS:

        # region : 1 Night Variables 
        number_bank_hands = 0
        night_profit = 0
        total_drop = 0
        total_profit = 0
        total_buster_profit = 0
        total_bj_profit = 0
        number_blackjacks = 0
        number_wins = 0
        number_losses = 0
        number_push = 0
        number_bj_push = 0
        number_splits = 0
        number_surrenders = 0
        bj_profit = 0
        buster_profit = 0
        bust_cards = []
        bj_results = []
        buster_results = []
        hand_results = []
        bankrupts = 0
        global BANK_PUSH
        STACK = BANK_PUSH
        BACKUP_CHIPS = EXTRA_BACKUP_CHIPS
        BANKRUPT = False
        deck = create_shoe()
        hand_counter = 0

        # endregion

        while hand_counter < HANDS_IN_NIGHT and BANKRUPT == False:

            # region : Creating dealers hand + print statements
            # Dealer's hand
            dealer_hand = [deck.pop(), deck.pop()]
            #dealer_hand = ['6','4']
            dealer_hand_value = calculate_hand_value(dealer_hand)
            while dealer_hand_value[0] < 17 or (dealer_hand_value[0] == 17 and dealer_hand_value[1] == 'Soft'):
                dealer_hand.append(deck.pop())
                dealer_hand_value = calculate_hand_value(dealer_hand)

            number_player = 1
            total_bet = 0
            buster_profit = 0 #reset
            bj_profit = 0 #reset for each hand
            hand_profit = 0

            # if hand_counter % 4 == 0 or hand_counter % 4 == 1: #THIS MEANS IT"S PLAYER! ALTERNATE EVERY TWO HANDS
            #     print("========================================================")
            #     print("Start of Hand #", hand_counter, "\n")
            #     print("Dealer hand:", dealer_hand, "Value:", dealer_hand_value[1], dealer_hand_value[0],"\n")
            
            #endregion

            for _ in range(NUM_PLAYERS):
                
                # region : Creating a player, bet size, and hand based off of strategy
                player_bj_bet = generate_bj_bet_size()
                player_buster_bet = generate_buster_bet_size()
                player_hands = [] #need a list because you might split
                player_hand = [deck.pop(), deck.pop()]
                #player_hand = ["A", "10"]
                player_hand_value = calculate_hand_value(player_hand)
                original_hand = (player_hand, player_hand_value)
                player_hands.append(original_hand)
                player_hands, player_hand_value, decisions = basic_strategy(player_hands, player_hand_value, dealer_hand)
                total_bet += (player_bj_bet + player_buster_bet)
                # endregion

                # region : Compare each player hand (if splits) against dealer hand
                if hand_counter % 4 == 0 or hand_counter % 4 == 1: #THIS MEANS IT"S PLAYER! ALTERNATE EVERY TWO HANDS

                    player_hand_number = 1
            
                    for hand in player_hands:

                        decision = decisions[player_hand_number - 1]

                        if player_hand_number > 1:
                            number_splits += 1

                        player_hand = hand[0]
                        player_hand_value = hand[1]
            
                        if decision == "D":
                            player_bj_bet *= 2

                        if decision == "BJ Already" and is_blackjack(dealer_hand):
                            result = "BJ Push"
                            number_bj_push += 1

                        elif decision == "BJ Already":
                            result = "Player Blackjack"
                            bj_profit -= player_bj_bet * BLACKJACK_PAYOUT
                            number_blackjacks += 1

                        elif decision == 'SUR':
                            result = "Player surrenders"
                            bj_profit += (player_bj_bet / 2)
                            number_surrenders += 1

                        elif player_hand_value[0] > 21:
                            result = "Player busts"
                            bj_profit += player_bj_bet
                            number_wins += 1
                        
                        elif dealer_hand_value[0] > 21 and player_hand_value[0] <= 21:
                            result = "Dealer busts"
                            bj_profit -= player_bj_bet
                            number_losses += 1

                        elif player_hand_value[0] > dealer_hand_value[0]:
                            result = "Player wins"
                            bj_profit -= player_bj_bet
                            number_losses += 1

                        elif player_hand_value[0] < dealer_hand_value[0]:
                            result = "Dealer wins"
                            bj_profit += player_bj_bet
                            number_wins += 1
                        
                        elif player_hand_value[0] == dealer_hand_value[0]:
                            result = "Push"
                            number_push += 1

                        else:
                            result = "ERROR"


                        if dealer_hand_value[0] > 21 and player_hand_number == 1: #This makes sure we dont pay multiple busters if they have mutliple hands (splitting)
                            buster_profit -= buster_payout_calc(player_buster_bet, dealer_hand)  
                        elif dealer_hand_value[0] <= 21 and player_hand_number == 1:
                            buster_profit += player_buster_bet
                        else:
                            buster_profit = buster_profit
                        

                        #Print game results
                        # print("Player Bet BJ: $", player_bj_bet, '--', "Buster: $", player_buster_bet)
                        # print("Player", number_player,"hand #",player_hand_number, ":", player_hand, "Value:", player_hand_value[1], player_hand_value[0])
                        # print(f"Result: {result}")
                        # print("DECISION: ", decision)
                        # print("----------")

                        

                        player_hand_number += 1

                number_player += 1
                # endregion

            # region : Profit / Loss Calculations and Stack management
            if hand_counter % 4 == 0 or hand_counter % 4 == 1: #THIS MEANS IT"S PLAYER! ALTERNATE EVERY TWO HANDS
                
                # print("Dealer hand:", dealer_hand, "Value:", dealer_hand_value[1], dealer_hand_value[0])
                # print(f"BJ Win/Loss: ${bj_profit}")
                # print(f"Buster Win/Loss: ${buster_profit}")
                # print(f"Drop: ${drop}")
                # print("\n")

                number_bank_hands += 1

                if dealer_hand_value[0] > 21:
                    bust_cards.append(len(dealer_hand)) # this means he didn't bust!
                else:
                    bust_cards.append(0)

                total_buster_profit += buster_profit
                total_bj_profit += bj_profit
                bj_results.append(bj_profit)
                buster_results.append(buster_profit)
                drop = calculate_drop(total_bet)  
                total_drop += drop

                hand_profit = (buster_profit + bj_profit + drop)
                hand_results.append(hand_profit)

                
                total_profit += hand_profit

                STACK += hand_profit

                if hand_profit > 0 and (STACK > BANK_PUSH):
                    #if you make money on the hand, you add to bankroll, not pushing stack if ur above min push
                    rathole = (STACK) - BANK_PUSH
                    BACKUP_CHIPS += rathole
                    STACK = BANK_PUSH

                elif hand_profit > 0 and STACK < BANK_PUSH:
                    STACK += hand_profit

                elif hand_profit < 0:
                    #NEED TO CHECK MAX LOSS HERE!
                    #if you lose money, you have to reload pushing stack, or give up if you don't meet 

                    if STACK <= 0: #you went bankrupt from a big loss in one hand                        
                        STACK = 0

                    stack_refill = (BANK_PUSH - STACK)

                    if BACKUP_CHIPS > stack_refill: # you can refill like normal
                        BACKUP_CHIPS -= stack_refill
                        STACK = BANK_PUSH

                    elif BACKUP_CHIPS + STACK >= MIN_PUSH: # Took all backup chips and put into stack. all in for more than min
                        STACK += BACKUP_CHIPS
                        BACKUP_CHIPS = 0
                    
                    elif BACKUP_CHIPS < MIN_PUSH:
                        STACK += BACKUP_CHIPS
                        BACKUP_CHIPS = 0
                        bankrupts += 1
                        BANKRUPT = True
                


                bankroll_points.append(STACK + BACKUP_CHIPS)

            if len(deck) < 40:
                #print("\n\nEMPTY SHOE, RESHUFFLE! \n\n")
                deck = create_shoe()

            hand_counter += 1

            # endregion

        # region : Per night printing

        night_profit = (STACK + BACKUP_CHIPS) - BUYIN

        #Table of buster distribution
        unique_elements = list(set(bust_cards))
        element_frequencies = [bust_cards.count(element) for element in unique_elements]
        num_buster_cards = [(element, bust_cards.count(element)) for element in set(bust_cards)]
        buster_frequency_table = pd.DataFrame(num_buster_cards, columns=['# Bust Cards', 'Frequency'])
        total_events = buster_frequency_table['Frequency'].sum()
        buster_frequency_table['%'] = (buster_frequency_table['Frequency'] / total_events) * 100
        buster_frequency_table['%'] = buster_frequency_table['%'].round(4)

        if printing_nights:
            #We hit the total hands in sim, time to print summary stats.
            print("Summary Statistics: \n")
            print("Total # Hands:",number_bank_hands,"out of", hand_counter, "total")
            print("Total $ Dropped:", total_drop)
            print("Total Buster Profit: $", total_buster_profit)
            print("Total BJ Profit: $", total_bj_profit)
            print("Total Profit: $", total_profit)
            

            total_hands = number_bj_push + number_surrenders+ number_blackjacks + number_push + number_losses + number_wins
            print(f"Blackjacks: {number_blackjacks} ({(number_blackjacks / total_hands) * 100:.2f}%)")
            print(f"Wins: {number_wins} ({(number_wins / total_hands) * 100:.2f}%)")
            print(f"Losses: {number_losses} ({(number_losses / total_hands) * 100:.2f}%)")
            print(f"Pushes: {number_push} ({(number_push / total_hands) * 100:.2f}%)")
            print(f"Surrenders: {number_surrenders} ({(number_surrenders / total_hands) * 100:.2f}%)")
            print(f"BJ Pushes: {number_bj_push} ({(number_bj_push / total_hands) * 100:.2f}%)")
            print(f"Splits: {number_splits} ({(number_splits / total_hands) * 100:.2f}%)")
            print("TOTAL HANDS: ", total_hands)
            print("\nBJ Profit / Hand:", total_bj_profit / number_bank_hands)
            print("\nBuster Profit / Hand:", total_buster_profit / number_bank_hands)
            
            print("\n==================================")
            print("==================================\n")

            print("Rat Hole total:", STACK + BACKUP_CHIPS)
            print("Bankrupts: ", bankrupts)
            print(buster_frequency_table.to_string(index=False))


        sim_bankrupts.append(BANKRUPT)
        sim_total_profits.append(night_profit)
        sim_bj_profit.append(total_bj_profit)
        sim_buster_profit.append(total_buster_profit)
        sim_buster_data.append(bust_cards)

        sim_bj_counter.append(number_blackjacks)
        sim_wins_counter.append(number_wins)
        sim_losses_counter.append(number_losses)
        sim_pushes_counter.append(number_push)
        sim_surrender_counter.append(number_surrenders)
        sim_bjpush_counter.append(number_bj_push)

        # endregion

        nights += 1 #increment

    # region : Sim wide printing and data management
    data = {
    "Night": list(range(1, len(sim_bankrupts) + 1)),
    "Bankrupt?": sim_bankrupts,
    "Total Profits": sim_total_profits,
    "Blackjack Profit": sim_bj_profit,
    "Buster Profit": sim_buster_profit,
    #"Blackjack Counter": sim_bj_counter,
    #"Wins Counter": sim_wins_counter,
    #"Losses Counter": sim_losses_counter,
    #"Pushes Counter": sim_pushes_counter,
    #"Surrender Counter": sim_surrender_counter,
    #"BJ Push Counter": sim_bjpush_counter
    }

    # Create a DataFrame
    df = pd.DataFrame(data)
    df.set_index("Night", inplace=True)
        # endregion
    print(df)

    # Calculate the count of bankrupts
    print("=============================\nSummary Statistics: \n")
    bankrupt_count = df["Bankrupt?"].sum()
    bankrupt_percentage = (bankrupt_count / SIM_NIGHTS) * 100
    print(f"Bankrupts: {bankrupt_count} out of {SIM_NIGHTS} ({bankrupt_percentage:.2f}%)")
    average_profit = df["Total Profits"].mean()
    print(f"Average profit per night: ${average_profit:.2f}\n")

# Start the game
play_blackjack()
