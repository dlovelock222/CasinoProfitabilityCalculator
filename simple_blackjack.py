import random

# Define constants
NUM_PLAYERS = 6
MIN_BJ_BET = 5
MAX_BJ_BET = 100
MIN_BUSTER_BET = 0
MAX_BUSTER_BET = 100
BLACKJACK_PAYOUT = 1.2
MAX_SPLITS_ALLOWED = 3
DECKS = 6




# Define player values (8-17) and dealer up cards (2-10, J, Q, K, A)
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



# Create a deck of cards
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = ranks * DECKS * 4 #4 is for the suits
random.shuffle(deck)


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
    5: 0.2,
    10: 0.1,
    15: 0.1,
    20: 0.1,
    30: 0.1,
    40: 0.1,
    50: 0.1,
    60: 0.1,
    80: 0.05,
    100: 0.05
    }
    
    random_number = random.choices(list(buster_bet_size.keys()), weights=list(buster_bet_size.values()))[0]
    return(random_number)


def generate_buster_bet_size():
    buster_bet_size = {
    0: 0.2,
    5: 0.2,
    10: 0.3,
    15: 0.1,
    20: 0.1,
    30: 0.1
    }

    random_number = random.choices(list(buster_bet_size.keys()), weights=list(buster_bet_size.values()))[0]
    return(random_number)


def basic_strategy(player_hands, player_hand_value, dealer_hand):

    dealer_up = dealer_hand[0]
    decision = 'Play'
    played_hands = []

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

        while decision not in ['S', 'SUR', 'D'] and player_hand_value[0] < 21:
    
            if player_hand_value[1] == "Soft":
                player_hand, player_hand_value, decision = bs_soft_totals(player_hand, player_hand_value, dealer_up)

            elif (player_hand_value[0] == 16 and len(player_hand) == 2 and dealer_up in ['9', '10', 'J', 'Q', 'K', 'A']) or (player_hand_value[0] == 15 and len(player_hand) == 2 and dealer_up in ['10', 'J', 'Q', 'K']):
                decision = 'SUR'

            else:
                player_hand, player_hand_value, decision = bs_hard_totals(player_hand, player_hand_value, dealer_up)
        
        played_hands.append((player_hand, player_hand_value))
        decision = 'Play'

    print("All hands:", played_hands)
    return played_hands, player_hand_value, decision
        


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




#if blackjack
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
        multipler = 200
    else:
        multiplier = 0

    payout = bet * multiplier
    return payout




# Main game loop
def play_blackjack():
    number_blackjacks = 0
    number_wins = 0
    number_losses = 0
    number_push = 0
    number_bj_push = 0
    house_balance = 0
    bj_profit = 0
    buster_profit = 0
    

    # Dealer's hand
    dealer_hand = [deck.pop(), deck.pop()]
    # TEST BLACKJACK 
    #dealer_hand = ['10','K']
    dealer_hand_value = calculate_hand_value(dealer_hand)
    while dealer_hand_value[0] < 17 or (dealer_hand_value[0] == 17 and dealer_hand_value[1] == 'Soft'):
        dealer_hand.append(deck.pop())
        dealer_hand_value = calculate_hand_value(dealer_hand)




    number_player = 1
    total_bet = 0
    
    for _ in range(NUM_PLAYERS):

        player_bj_bet = generate_bj_bet_size()
        player_buster_bet = generate_buster_bet_size()
        player_hands = [] #need a list because you might split
        player_hand = [deck.pop(), deck.pop()]
        #player_hand = ["A", "A"]
        player_hand_value = calculate_hand_value(player_hand)
        original_hand = (player_hand, player_hand_value)
        player_hands.append(original_hand)
        #player_hands[0] = ['4', '4', '3']
        player_hands, player_hand_value, decision = basic_strategy(player_hands, player_hand_value, dealer_hand)

        player_hand_number = 1
        for hand in player_hands:

            player_hand = hand[0]
            player_hand_value = hand[1]
 
            if decision == "D":
                player_bj_bet *= 2

            if is_blackjack(player_hand) and is_blackjack(dealer_hand):
                result = "BJ Push"
                number_bj_push += 1

            elif is_blackjack(player_hand):
                if is_blackjack(player_hand):
                    result = "Player Blackjack"
                    bj_profit -= player_bj_bet * BLACKJACK_PAYOUT
                    number_blackjacks += 1

            elif decision == 'SUR':
                result = "Player surrenders"
                bj_profit += (player_bj_bet / 2)
                number_wins += 1

            elif player_hand_value[0] > 21:
                result = "Player busts"
                bj_profit += player_bj_bet
                number_wins += 1
            
            elif dealer_hand_value[0] > 21:
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

            else:
                result = "Push"
                number_push += 1


            if dealer_hand_value[0] > 21:
                #print("BUSTER BET PAYS!")
                buster_profit -= buster_payout_calc(player_buster_bet, dealer_hand)   #ONLY CASE WHERE BUSTER PAYS!
            else:
                buster_profit += player_buster_bet
            

        
            
            # Print game results
            print("Player Bet BJ: $", player_bj_bet, '--', "Buster: $", player_buster_bet)
            print("Player", number_player,"hand #",player_hand_number, ":", player_hand, "Value:", player_hand_value[1], player_hand_value[0])
            print(f"Result: {result}")
            print("----------")

            total_bet += (player_bj_bet + player_buster_bet)

            player_hand_number += 1

        number_player += 1

    house_balance += buster_profit
    house_balance += bj_profit  
    drop = calculate_drop(total_bet)  
    house_balance += drop

    print("Dealer hand:", dealer_hand, "Value:", dealer_hand_value[1], dealer_hand_value[0])



    print(f"BJ Win/Loss: ${bj_profit}")
    print(f"Buster Win/Loss: ${buster_profit}")
    print(f"Drop: ${drop}")
    print(f"Bank Win/Loss: ${house_balance}")



    print("Blackjacks:", number_blackjacks)
    print("Wins:", number_wins)
    print("Losses:", number_losses)
    print("Pushes:", number_push)
    print("BJ Pushes:", number_bj_push)



# Start the game
play_blackjack()
