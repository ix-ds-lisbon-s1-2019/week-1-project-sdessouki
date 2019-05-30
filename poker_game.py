
import random
import collections

    
class Card(object):
    VALUES= [2,3,4,5,6,7,8,9,10,11,12,13,14]
    SUITS = [" clubs", " spades", " hearts", " diamonds"]

    def __init__(self, value, suit):
        self.value= value
        self.suit = suit

    def __repr__(self):
        return self.suit + ' ' + str(self.value)
        
    def __str__(self):
        if self.value == 14:
            value = 'A'
        elif self.value ==13:
            value = 'K'
        elif self.value ==12:
            value = 'Q'
        elif self.value ==11:
            value = 'J'
        else:
            value = self.value
        return str(value) + self.suit
    
    def __equal__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            for val in Card.VALUES:
                self.deck.append(Card(val, suit))
                
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) == 0:
            return None
        else:
            return self.deck.pop(random.choice(self.deck).value)

class Poker(object):
    def __init__(self, players):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = players
        self.dealt=[ ]
        self.hand_type= ' '
        self.breaker = [ ]

        for i in range(int(self.players)):
            hand=[ ]
            for j in range(5):
                hand.append(self.deck.deal())
            self.dealt.append(hand)

    def sortHand(self):
        for i in range(self.players):
            sort_Hand = sorted(self.dealt, reverse = False)
            hand = ''
            count =0
            for card in sort_Hand:
                count += 1
                if count !=5:
                    hand = hand + str(card) + ', '
                else:
                    hand = hand + str(card) + ' '
            print ('Player ' + str(i + 1) + "\'s hand: " + hand)


    def isRoyalFlush(self, hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_suit= sort_Hand[0].suit
        current_val= 14
        for card in sort_Hand:
            if card.suit != current_suit or card.value != (current_val):
                flag = False
                break
            else:
                current_val-=1
        if flag:
            print("Royal Flush")
            self.breaker = [10, 0] #if breaker = 0 then tie.
        else:
            self.isStraightFlush(sort_Hand)

    def isStraightFlush(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_suit= sort_Hand[0].suit
        current_val= sort_Hand[0].value
        for card in sort_Hand:
            if card.suit != current_suit or card.value != (current_val):
                flag = False
                break
            else:
                current_val+=1
        if flag:
            print("Straight Flush")
            self.breaker = [9,current_val]
        else:
            self.isFourofaKind(sort_Hand)

    def isFourofaKind(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        c = collections.Counter(sort_Hand).most_common(2)
        if c[0][1] ==4:
            print("Four of a Kind")
            self.breaker = [8, c[0][0]]
        else:
            self.isFullHouse(sort_Hand)
            
    def isFullHouse(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        c = collections.Counter(sort_Hand).most_common(2)
        if c[0][1] ==3 and c[0][1] == 2:
            print("Full House")
            self.breaker = [7, c[0][0]]
        else:
            self.isThreeofaKind(sort_Hand)

    def isFlush(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_suit= sort_Hand[0].suit
        for card in sort_Hand:
            if card.suit != current_suit:
                flag = False
                break
        if flag:
            print("Flush")
            self.breaker = [6,max(sort_Hand)] #decided to break at the highest card, if tie, then its a tie 
        else:
            self.isStraight(sort_Hand)

    def isStraight(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_val= sort_Hand[0].value
        for card in sort_Hand:
            if card.value != current_val:
                flag = False
                break
            else:
                current_val+=1
        if flag:
            print("Straight")
            self.breaker = [5, max(sort_Hand)]
        else:
            self.isThreeofaKind(sort_Hand)
            
    def isThreeofaKind(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        c = collections.Counter(sort_Hand).most_common(2)
        if c[0][1] == 3:
            print("Three of a Kind")
            self.breaker = [4, c[0][0]]
        else:
            self.isTwoPairs(sort_Hand)
            
    def isTwoPairs(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        c = collections.Counter(sort_Hand).most_common(2)
        pair_values = [ ] 
        if c[0][1] ==2 and c[1][1] ==2:
            print("Two Pairs")
            pair_values.append(c[0][0])
            pair_values.append(c[1][0])
            self.breaker = [3, max(pair_values)]
        else:
            self.isOnePair(sort_Hand)
    def isOnePair(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        c = collections.Counter(sort_Hand).most_common(2)
        if c[0][1] ==2:
            print("One Pair")
            self.breaker = [2,c[0][0]]
        else:
            self.isHigh(sort_Hand)
            
    def isHigh(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        self.hand_type="High"
        self.breaker = [1, max(sort_Hand)]

    def break_tie(self): 
        print("same hand type")
        count = 0
        breakers =[]
        for hand in self.dealt:
            breakers.append(self.breaker[1])
            cur_max = 0
            winners = [ ]
            if self.breaker[1].value > cur_max:
                cur_max = self.breaker[1]
        for hand in self.dealt:
            if self.breaker[1] == cur_max:
                winners.append(count)
        if len(winners)==1:
            print("Player " + winners[0] + " wins")
        else:
            print("Tie between")
            for i in winners:
                print("player " + str(winners[i]) + " ")

    def findWinner(self):
        hand_types = [ ]
        break_hands = [ ]
        for hand in self.dealt:
            hand_types.append(self.breaker[0]) #append the rank of each hand
        count = 0
        cur_max = 0
        winners = []
        winner_found= False 
        for rank in hand_types:
            if rank >= cur_max:
                cur_max= rank
        for rank in hand_types:
            count += 1
            if rank == cur_max:
                winners.append(count)
                if cur_max==10:
                    print("the game is tied")
                    winnner_found= True
        if winner_found==False:           
            if len(winners)==1:
                print("Player " + winners[0] + " wins")
            else:
                self.break_tie()

def getNumPlayers():
    try:
        players=int(input("Number of players: "))
    except: 
        print("Guess you don't want to play")
        quit()
    while players <=0 or players >10:
        print("invalid number of players")
        players=int(input("Please re-state the number of players: "))
    return players
        

    


#players=int(input("Number of players: "))
players = getNumPlayers()
print('\n')
game = Poker(players)
game.sortHand()

print('\n')
for i in range(players):
    curHand=game.dealt[i]
    game.isRoyalFlush(curHand)

game.findWinner()
        
    

    
        
