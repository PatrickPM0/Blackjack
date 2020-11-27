"""Blackjack game with GUI"""

import random



suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}


# boolean to control while loop to control the flow of the game
playing = True


# card class where each card object has a suit and rank
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# deck class to hold 52 cards and can be shuffled
# instantiate all 52 unique cards and add them to deck

class Deck:
    # each deck is created with 52 cards
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    # use the Card Class's __str__() to get a useable string. This isn't used in production code. Used for troubleshooting.
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp+="\n" + card.__str__()
        return deck_comp

    # shuffle deck, don't even worry about complicated shuffle functions, just use random.shuffle
    def shuffle(self):
        random.shuffle(self.deck)

    # remove one card from the TOP of the deck
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# hand class that holds cards that have been dealt from the deck
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self,total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total+=self.bet

    def lost_bet(self):
        self.total-=self.bet

# function to take bets
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet?"))
        except ValueError:
            print("The bet must be an integer.")
        else:
            if chips.bet > chips.total:
                print(f"Sorry! You only have {chips.total} chips.")
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    while True:
        x = input("Would you like to Hit or Stand?")
        if x[0].lower() == "h":
            hit(deck,hand)
        elif x[0].lower() == "s":
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Sorry, invalid input. Type 'hit' or 'h' to hit. Type 'stand' or 's' to stand.")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()

def push():
    print("Dealer and Player tie! It's a push.")

while True:
    # Print an opening statement
    print("Let's play some blackjack!")

    # create a deck and shuffle it
    deck = Deck()
    deck.shuffle()

    # create player and deal two cards
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # create dealer and deal two cards
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()  # default=100 chips

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_chips)
            break


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)

        else:
            push()

    # Inform Player of their chips total
    print("\nPlayer's winnings stand at",player_chips.total)

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break
