import random

# Define constants
NUM_PLAYERS = 6
MIN_BJ_BET = 5
MAX_BJ_BET = 100
MIN_BUSTER_BET = 0
MAX_BUSTER_BET = 100
BLACKJACK_PAYOUT = 1.2
DECKS = 6




# Define player values (8-17) and dealer up cards (2-10, J, Q, K, A)
player_values_hard = list(range(4, 18))
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
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'SUR', 'SUR', 'SUR', 'SUR', 'H'],  # Player value 15
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'SUR', 'SUR', 'SUR', 'SUR', 'SUR', 'SUR'],  # Player value 16
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']   # Player value 17
]

player_values_soft = list(range(13, 21))
dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

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


# Create the 2D array for basic strategy decisions
basic_strategy_hard_array = dict(zip(player_values_hard, basic_strategy_hard))
basic_strategy_soft_array = dict(zip(player_values_soft, basic_strategy_soft))











# Create a deck of cards
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = ranks * DECKS * 4 #4 is for the suits
random.shuffle(deck)



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
    
    if num_aces > 1 and num_aces - num_11_aces == 0 and value != 21 and value < 21:
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


def basic_strategy(player_hand, player_hand_value, dealer_hand, dealer_hand_value):

    player_value = player_hand_value[0]
    dealer_up = dealer_hand[0]
    print("UP CARD DEALER:", dealer_up)


    if player_hand_value[0] in [15, 16]:
        if bs_surrender(player_hand_value, dealer_up):
            return "Surrender"
    
    if player_hand_value[1] == "Soft":
        return bs_soft_totals(player_hand_value, dealer_up)
    
    if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
        return bs_pairs(player_hand, dealer_up)
    
    else:
        return bs_hard_totals(player_hand, player_hand_value, dealer_up)
        
        



    # while player_hand_value[0] < 16:
    #     player_hand.append(deck.pop())
    #     player_hand_value = calculate_hand_value(player_hand)
    # return(player_hand, player_hand_value)

def bs_pairs(player_hand, player_hand_value): #NEED TO ADD LOGIC WHERE YOU CAN ONLY TAKE ONE CARD ON A SPLIT!
    return True

def bs_surrender(player_hand_value, dealer_up):
    if player_hand_value[0] == 16 and player_hand_value[1] == "Hard" and dealer_up in ['9', '10', 'J', 'Q', 'K', 'A']:
        return True
    elif player_hand_value[0] == 15 and player_hand_value[1] == "Hard" and dealer_up in ['10', 'J', 'Q', 'K']:
        return True
    else:
        return False
    
def bs_soft_totals(player_hand, player_hand_value, dealer_up): #FINSIH LOGIC
    if 1 == 1: 
        return "Hit"
    elif 2 == 2: 
        return "Double"
    else:
        return "Stand"
    
def bs_hard_totals(player_hand, player_hand_value, dealer_up):

    # Simulate a decision based on player value and dealer up card
    decision = basic_strategy_hard_array[player_hand_value[0]][dealer_upcards.index(dealer_up)]
    if decision == "H":
        player_hand.append(deck.pop())
        player_hand_value = calculate_hand_value(player_hand)

    elif decision == "D":
        decision = 'D'

    elif decision == "SUR":
        decision = 'SUR'

    else:
        decision = 'S'

    return(player_hand, player_hand_value, decision)


    def make_decision(player_value, dealer_upcard):
        decision = basic_strategy_hard_array[player_value][dealer_upcards.index(dealer_upcard)]
        return decision




    return True







#if blackjack
def is_blackjack(hand):
    return len(hand) == 2 and 'A' in hand and any(card in ['10', 'J', 'Q', 'K'] for card in hand)

def buster_payout_calc(bet, hand):
    bust_cards = len(hand)
    print(bust_cards)
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
    #dealer_hand = ['10','A']
    dealer_hand_value = calculate_hand_value(dealer_hand)
    while dealer_hand_value[0] < 17 or (dealer_hand_value[0] == 17 and dealer_hand_value[1] == 'Soft'):
        dealer_hand.append(deck.pop())
        dealer_hand_value = calculate_hand_value(dealer_hand)





    
    for _ in range(NUM_PLAYERS):
        #player_bj_bet = random.randint(MIN_BJ_BET, MAX_BJ_BET)
        #player_buster_bet = random.randint(MIN_BUSTER_BET,MAX_BUSTER_BET)

        player_bj_bet = generate_bj_bet_size()
        player_buster_bet = generate_buster_bet_size()

        player_hand = [deck.pop(), deck.pop()]
        player_hand_value = calculate_hand_value(player_hand)
        
        # Player's turn
        # while player_hand_value[0] < 16:
        #     player_hand.append(deck.pop())
        #     player_hand_value = calculate_hand_value(player_hand)
        player_hand, player_hand_value = basic_strategy(player_hand, player_hand_value, dealer_hand, dealer_hand_value)
        
        

        if is_blackjack(player_hand) and is_blackjack(dealer_hand):
            result = "BJ Push"
            number_bj_push += 1

        elif is_blackjack(player_hand):
            if is_blackjack(player_hand):
                result = "Player Blackjack"
                bj_profit -= player_bj_bet * BLACKJACK_PAYOUT
                number_blackjacks += 1

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
            print("BUSTER BET PAYS!")
            buster_profit -= buster_payout_calc(player_buster_bet, dealer_hand)   #ONLY CASE WHERE BUSTER PAYS!
        else:
            buster_profit += player_buster_bet
        

    
        
        # Print game results
        print(f"Player bet: ${player_bj_bet}")
        print(f"Player Buster bet: ${player_buster_bet}")
        print("Player hand:", player_hand, "Value:", player_hand_value[1], player_hand_value[0])
        print(f"Result: {result}")
        print("----------")

    house_balance += buster_profit
    house_balance += bj_profit    

    print("Dealer hand:", dealer_hand, "Value:", dealer_hand_value[1], dealer_hand_value[0])



    print(f"BJ Win/Loss: ${bj_profit}")
    print(f"Buster Win/Loss: ${buster_profit}")
    print(f"Bank Win/Loss: ${house_balance}")
    if house_balance > 0:
        print("House wins")
    elif house_balance < 0:
        print("Players win")
    else:
        print("It's a tie")



    print("Blackjacks:", number_blackjacks)
    print("Wins:", number_wins)
    print("Losses:", number_losses)
    print("Pushes:", number_push)
    print("BJ Pushes:", number_bj_push)



# Start the game
play_blackjack()
