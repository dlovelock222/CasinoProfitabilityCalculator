print("testing")

import random

# Define constants
NUM_PLAYERS = 2
MIN_BET = 5
MAX_BET = 100
BLACKJACK_PAYOUT = 1.2
DECKS = 6

# Create a deck of cards
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits] * DECKS
random.shuffle(deck)







# Function to calculate the value of a hand PLAYER
def calculate_hand_value(hand):
    value = 0
    num_aces = 0
    
    for card in hand:
        if card['rank'] in ['J', 'Q', 'K']:
            value += 10
        elif card['rank'] == 'A':
            num_aces += 1
            value += 11
        else:
            value += int(card['rank'])
    
    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1
    
    return value



# Main game loop
def play_blackjack():
    house_balance = 0
    
    
    # # Dealer's hand
    # dealer_hand = [deck.pop(), deck.pop()]
    # dealer_hand_value = calculate_hand_value(dealer_hand)
    # while dealer_hand_value < 17 or (dealer_hand_value == 17 and 'A' in [card['rank'] for card in dealer_hand]):
    #     dealer_hand.append(deck.pop())
    #     dealer_hand_value = calculate_hand_value(dealer_hand)
    
    
    for _ in range(NUM_PLAYERS):
        player_bet = random.randint(MIN_BET, MAX_BET)
        player_hand = [deck.pop(), deck.pop()]
        player_hand_value = calculate_hand_value(player_hand)
        
        # Player's turn
        while player_hand_value < 16:
            player_hand.append(deck.pop())
            player_hand_value = calculate_hand_value(player_hand)
        

        # Dealer's hand
        dealer_hand = [deck.pop(), deck.pop()]
        # TEST BLACKJACK dealer_hand = [{'rank': '10', 'suit': 'clubs'}, {'rank': 'A', 'suit': 'diamonds'}]
        dealer_hand_value = calculate_hand_value(dealer_hand)
        while dealer_hand_value < 17 or (dealer_hand_value == 17 and 'A' in [card['rank'] for card in dealer_hand]):
            dealer_hand.append(deck.pop())
            dealer_hand_value = calculate_hand_value(dealer_hand)


        # Determine the winner and calculate payouts

        if len(player_hand) == 2 and 'A' in [card['rank'] for card in player_hand] and any(rank in ['10', 'J', 'Q', 'K'] for rank in [card['rank'] for card in player_hand]):
            if len(dealer_hand) == 2 and 'A' in [card['rank'] for card in dealer_hand] and any(rank in ['10', 'J', 'Q', 'K'] for rank in [card['rank'] for card in dealer_hand]):
                result = "BJ Push"
            else:
                result = "Player Blackjack"
                house_balance -= player_bet * BLACKJACK_PAYOUT
        
        elif player_hand_value > 21:
            result = "Player busts"
            house_balance += player_bet
        elif dealer_hand_value > 21:
            result = "Dealer busts"
            house_balance -= player_bet
        elif player_hand_value > dealer_hand_value:
            result = "Player wins"
            house_balance -= player_bet
        elif player_hand_value < dealer_hand_value:
            result = "Dealer wins"
            house_balance += player_bet
        else:
            result = "Push"
        
        # Print game results
        print(f"Player bet: ${player_bet}")
        print(f"Player hand: {player_hand} (Value: {player_hand_value})")
        print(f"Result: {result}")
        print("----------")

        

    dealer_hand_str = ', '.join([f"{card['rank']}{card['suit'][0]}" for card in dealer_hand])
    print(f"Dealer hand: {dealer_hand_str} (Value: {dealer_hand_value})")



    print(f"House balance: ${house_balance}")
    if house_balance > 0:
        print("House wins")
    elif house_balance < 0:
        print("Players win")
    else:
        print("It's a tie")

# Start the game
play_blackjack()
