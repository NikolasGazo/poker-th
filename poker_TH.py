# -*- coding: utf-8 -*-
"""
Created on Sun May 30 21:31:54 2021

@author: nikol
"""

import numpy as np
import random
from collections import Counter
import pandas as pd





## make card deck
suits = ['C','D','H','S']
ranks = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']

## heirarchy order, two versions... Ace high or low?
order = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
order2 = ['K','Q','J','10','9','8','7','6','5','4','3','2','A']

def make_new_deck():
	''' return a new deck of 52 cards '''
	cardDeck = []
	for s in suits:
		for r in ranks:
			cardDeck.append(''.join([s,r]))

	return cardDeck


## make a class for a player...
class Player():
	def __init__(self):
		self.card1 = ''
		self.card2 = ''
		
	def return_cards(self):
		return [self.card1, self.card2]

## make a class for the dealer
class Dealer():
	def __init__(self):
		self.card1 = ''
		self.card2 = ''
		self.card3 = ''
		self.card4 = ''
		self.card5 = ''
		
	def return_cards(self):
		dealerHand = []
		if self.card1 != '':
			dealerHand.append(self.card1)
		if self.card2 != '':
			dealerHand.append(self.card2)
		if self.card3 != '':
			dealerHand.append(self.card3)
		if self.card4 != '':
			dealerHand.append(self.card4)
		if self.card5 != '':
			dealerHand.append(self.card5)

		return dealerHand


'''

sequence of events.. dealer starts face up card for themselves...

then passes to every entrant one face up card...or face deown?

.. then dealer flops another to themselves and then everyone else face down...


need to define "ifRoyalFlush" and "ifStraightFlush", etc functions...


use the 2 cards each entrant has and the 5 cards the dealer has put forward and make a best 5-card hand


https://www.cardplayer.com/rules-of-poker/hand-rankings

'''





def addCardToPlayer(p, newCard, deck):
	if p.card1 == '':
		p.card1 = newCard
		deck.remove(newCard)
	elif p.card1 != '' and p.card2 == '':
		p.card2 = newCard
		deck.remove(newCard)
	else:
		return None
	
def addCardToDealer(p, newCard, deck):
	if p.card1 == '':
		p.card1 = newCard
		deck.remove(newCard)
	elif p.card2 == '':
		p.card2 = newCard
		deck.remove(newCard)
	elif p.card3 == '':
		p.card3 = newCard
		deck.remove(newCard)
	elif p.card4 == '':
		p.card4 = newCard
		deck.remove(newCard)
	elif p.card5 == '':
		p.card5 = newCard
		deck.remove(newCard)
	else:
		return None
	

## give card to each player...
def give_player_card(p, deck):
	if isinstance(p,list):
		for player in p:
			newCard = random.choice(deck)
			addCardToPlayer(player, newCard, deck)
# 			deck.remove(newCard)
# 			newCard = random.choice(deck) ## if two at a time...
# 			addCardToPlayer(player, newCard)
# 			deck.remove(newCard)
			
	if not isinstance(p,list):
		newCard = random.choice(deck)
		addCardToPlayer(p, newCard, deck)
# 		deck.remove(newCard)
# 		newCard = random.choice(deck) ## if two at a time...
# 		addCardToPlayer(player, newCard)
# 		deck.remove(newCard)

## give card to each player...
def give_dealer_card(p, deck):
	if isinstance(p,list):
		for player in p:
			newCard = random.choice(deck)
			addCardToDealer(player, newCard, deck)
# 			deck.remove(newCard)
# 			newCard = random.choice(deck) ## if two at a time...
# 			addCardToPlayer(player, newCard)
# 			deck.remove(newCard)
			
	if not isinstance(p,list):
		newCard = random.choice(deck)
		addCardToDealer(p, newCard, deck)
# 		deck.remove(newCard)
# 		newCard = random.choice(deck) ## if two at a time...
# 		addCardToPlayer(player, newCard)
# 		deck.remove(newCard)




def get_hand(p,d):
	if isinstance(p, list) and isinstance(d, list):
		return p + d
	elif isinstance(p, list) and not isinstance(d,list):
		return p + d.return_cards()
	elif isinstance(d, list) and not isinstance(p,list):
		return d + p.return_cards()
	else:
		return p.return_cards() + d.return_cards()

def get_rank(card):
	""" return rank of the card, ie 2-10,J,Q,K,A"""
	if isinstance(card, str):
		return card[1:]
	else:
		newList = []
		for c in card:
			newList.append(c[1:])
		return newList

def get_suit(card):
	""" return the suit of the card """
	if isinstance(card, list):
		temp = []
		for c in card:
			temp.append(c[0])
	else:
		temp = card[0]
		
	return temp

###########################################################
### Find hands....
## need to evaulute the hands of each player with the dealers cards & then compare against actual hands...
## all the hands... there are 10
#  1. Royal Flush
def isRoyalFlush(p,d):
	""" A, K, Q, J, 10, all the same suit. """
	hand = get_hand(p,d)
	heartsRF = ['HA', 'HK', 'HQ', 'HJ', 'H10']
	clubsRF = ['CA', 'CK', 'CQ', 'CJ', 'C10']
	spadesRF = ['SA', 'SK', 'SQ', 'SJ', 'S10']
	diamondsRF = ['DA', 'DK', 'DQ', 'DJ', 'D10']

	counter = []

	for c in hand:
		if c in heartsRF: 
			counter.append('H')
		elif c in clubsRF:
			counter.append('C')
		elif c in spadesRF: 
			counter.append('S')
		elif c in diamondsRF:
			counter.append('D')
		else:
			counter.append('N')
	
	if counter.count('H') >= 5:
		return True
	elif counter.count('C') >= 5:
		return True
	elif counter.count('S') >= 5:
		return True
	elif counter.count('D') >= 5:
		return True
	else:
		return False



## 6. Straight
def isStraight(p,d):
	"""Five cards in a sequence, but not of the same suit"""
	if isinstance(p,list) and isinstance(d,list):
		hand = p + d
	else:
		hand = get_hand(p,d)
#	print(hand)
	indexPos = []
	indexPos2 = []
	for c in get_rank(hand):
		indexPos.append(order.index(c))
		indexPos2.append(order2.index(c))

	version1 = sorted(indexPos)
	version2 = sorted(indexPos2)
# 	print(version1)
# 	print(version2)
	straight = False
	s = -5 + len(hand)
	for pos in np.arange(0,s+1):
		if np.diff(version1[pos:pos+5]).min() == 1 and np.diff(version1[pos:pos+5]).mean() == 1:
			straight = True
	for pos in np.arange(0,s+1):
		if np.diff(version2[pos:pos+5]).min() == 1 and np.diff(version2[pos:pos+5]).mean() == 1:
			straight = True

	return straight



## 2. Straight Flush
def isStraightFlush(p,d):
	"""  Five cards in a sequence, all in the same suit  """
	if isinstance(p,list) and isinstance(d,list):
		hand = p + d
		p1 = get_suit(p)
		d1 = get_suit(d)
	else:
		hand = get_hand(p,d)
		p1 = get_suit(p.return_cards())
		d1 = get_suit(d.return_cards())
		
	suit_counter = [get_suit(c) for c in hand]
	if suit_counter.count('C') > 4:
# 		print('C flush')
		StraightFlush = isStraight([c for c in hand if 'C' in p1],[c for c in hand if 'C' in d1])
		if StraightFlush:
			return True
		else:
			return False
		
	elif suit_counter.count('D') > 4:
# 		print('D flush')
		StraightFlush = isStraight([c for c in hand if 'D' in p1],[c for c in hand if 'D' in d1])
		if StraightFlush:
			return True
		else:
			return False
	elif suit_counter.count('H') > 4:
# 		print('H flush')
		StraightFlush = isStraight([c for c in hand if 'H' in p1],[c for c in hand if 'H' in d1])
		if StraightFlush:
			return True
		else:
			return False
		
	elif suit_counter.count('S') > 4:
# 		print('S flush')
		StraightFlush = isStraight([c for c in hand if 'S' in p1],[c for c in hand if 'S' in d1])
		if StraightFlush:
			return True
		else:
			return False
	else:
		return False
	
	

## 3. Four of a kind
def isFourOfAKind(p,d):
	""" find 4 cards with same rank  """ 
	hand = get_hand(p,d)
	
	rank_counter = [get_rank(c) for c in hand]

	if pd.Series(rank_counter).value_counts().max() >= 4:
# 		print("four of a kind!")
		return True
	else:
		return False



## 4. Full House
def isFullHouse(p,d):
	""" find 3 cards with same rank, and find 2 cards with same rank """
	hand = get_hand(p,d)
	
	rank_counter = [get_rank(c) for c in hand]

	rank_counted = pd.Series(rank_counter).value_counts().tolist()
	if 3 in rank_counted and 2 in rank_counted:
# 		print("FULLHOUSE!")
		return True
	else:
		return False


## 5. Flush
def isFlush(p,d):
	"""  Five cards in the same suit; not in sequence though """
	hand = get_hand(p,d)
	
	suit_counter = [get_suit(c) for c in hand]
	if suit_counter.count('C') > 4:
# 		print('C flush')
		return True
	elif suit_counter.count('D') > 4:
# 		print('D flush')
		return True
	elif suit_counter.count('H') > 4:
# 		print('H flush')
		return True
	elif suit_counter.count('S') > 4:
# 		print('S flush')
		return True
	else:
		return False



## 7. Three of a kind
def isThreeOfAKind(p,d):
	""" if 3 cards with same rank """
	hand = get_hand(p,d)
	
	rank_counter = [get_rank(c) for c in hand]

	rank_counted = pd.Series(rank_counter).value_counts().tolist()
# 	print(rank_counted)
	if max(rank_counted) >= 3:
# 		print("Three of a Kind!")
		return True
	else:
		return False


## 8. Two pair
def isTwoPair(p,d):
	""" checks if hand has 2 distinct pairs. e.g., 2 K's and 2 10's"""
	hand = get_hand(p,d)
	
	rank_counter = [get_rank(c) for c in hand]

	rank_counted = pd.Series(rank_counter).value_counts().tolist()
	
	if sorted(rank_counted)[-1] >=2 and sorted(rank_counted)[-2] >= 2:
		return True
	else:
		return False
	

## 9. Pair
def isPair(p,d, return_rank=False):
	""" checks if hand has 1 distinct paid. e.g., 2 K's """
	hand = get_hand(p,d)
	rank_counter = [get_rank(c) for c in hand]

	rank_counted = pd.Series(rank_counter).value_counts().tolist()
	

	if max(rank_counted) >= 2:
		if return_rank:
			temp = pd.Series(rank_counter).value_counts().sort_index().iloc[0]
			return min(order.index(temp),order2.index(temp))
# 			return pd.Series(rank_counter).value_counts()
		else:
			return True
	else:
		return False


		


## 10. High Card
def isHighCard(p,d):
	""" return the highest card in the hand """
	hand = get_hand(p,d)
	indexPos = []
	for c in get_rank(hand):
		indexPos.append(order.index(c))

	version1 = sorted(indexPos)
	
	maxCard = order[version1[0]]
	
	return maxCard
	


def return_all_hands(allPlayers, dealer):
	print("All hands:")
	for i, p in enumerate(allPlayers):
		print(i, p.return_cards() + dealer.return_cards())
	print("================================================")


##################################
##################################
####
#### Comparison of same hands functions...
def best_pair(ps,d):
	highestPairCard = []
	print(ps)
	for i,p in enumerate(ps):
		pList = isPair(p,d, return_rank=True)
		pairHigh = order.index(pList.index[0])
		highestPairCard.append([i,pairHigh])
		
	print(highestPairCard)
	


def find_winning_hand(p_out,dealer,allPlayerHands,allPlayers):
	""" bring in a dictionary of the players and they're hands then parse which has highest hand; head-to-head"""
	tempList = pd.DataFrame(allPlayerHands,columns=['player','hand'])
	
	bestHands = tempList.loc[tempList['hand']==tempList['hand'].min()]
	
# 	print('best hands..')
	if bestHands.shape[0] == 1:
		pass
# 		print(f"the winner is player {bestHands['player'].values[0]}! with a {bestHands['hand'].min()}")
#  add a return here...
	else:
		bestHand = bestHands['hand'].min()
		players = bestHands['player'].values.tolist()
		if bestHand == 9:
# 			print(f"pair: {players}")
			temp = [allPlayers[i] for i in players]
			best_pair(temp,dealer)
		if bestHand == 8:
			print(f"two pair: {players}")
		if bestHand == 7:
			print(f"Three of a Kind: {players}")
		if bestHand == 6:
			print(f"Straight: {players}")
		if bestHand == 5:
			print(f"Flush: {players}")
		if bestHand == 4:
			print(f"Full House: {players}")
		if bestHand == 3:
			print(f"Four of a kind: {players}")
		if bestHand == 2:
			print(f"Straight Flush: {players}")
		if bestHand == 1:
			print(f"Royal Flush: {players}")
			

## will return player number
	pass









###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
if __name__=='__main__':

	allHands = []
	highestHand =[]
	for runs in np.arange(0,1):
		singleHand = []
		print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print(f"Run number: {runs}")
		
		cardDeck = make_new_deck()
		
		
		## number of players (omitting dealer, even dealer rotates)
		numPlayers = 6
		
		allPlayers = []
		
		
		for p in range(0,numPlayers):
			allPlayers.append(Player())
		
		dealer = Dealer()
		
		## deal two cards to each player... one at a time?
		give_player_card(allPlayers, cardDeck)
		give_player_card(allPlayers, cardDeck)		
		give_dealer_card(dealer, cardDeck)
		give_dealer_card(dealer, cardDeck)
		
		
		## give dealer 3 of 5 cards and each player has 2 cards
		give_dealer_card(dealer,cardDeck)
		
		## give dealer 4 of 5 cards
		give_dealer_card(dealer, cardDeck)
		
		## give dealer 5 of 5 cards
		give_dealer_card(dealer, cardDeck)
		
		p_out = {}
		allPlayerHands = []
# 		return_all_hands(allPlayers,dealer)
		for i, p in enumerate(allPlayers):
			playerHand = []
	
# 			print(f"Player {str(i)} has:")
			if isRoyalFlush(p,dealer):
# 				print('-> 1. Royal Flush!')
				allHands.append(1)
				singleHand.append(1)
				playerHand.append(1)
				allPlayerHands.append([i,1])
			if isStraightFlush(p,dealer):
# 				print('-> 2. Straight flush')
				allHands.append(2)
				singleHand.append(2)
				playerHand.append(2)
				allPlayerHands.append([i,2])
			if isFourOfAKind(p,dealer):
# 				print("-> 3. Four of a kind!")
				allHands.append(3)
				singleHand.append(3)
				playerHand.append(3)
				allPlayerHands.append([i,3])
			if isFullHouse(p,dealer):
# 				print('-> 4. Full House')
				allHands.append(4)
				singleHand.append(4)
				playerHand.append(4)
				allPlayerHands.append([i,4])
			if isFlush(p, dealer):
# 				print("-> 5. Flush")
				allHands.append(5)
				singleHand.append(5)
				playerHand.append(5)
				allPlayerHands.append([i,5])
			if isStraight(p,dealer):
# 				print('-> 6. Straight')
				allHands.append(6)
				singleHand.append(6)
				playerHand.append(6)
				allPlayerHands.append([i,6])
			if isThreeOfAKind(p, dealer):
# 				print('-> 7. Three of a Kind')
				allHands.append(7)
				singleHand.append(7)
				playerHand.append(7)
				allPlayerHands.append([i,7])
			if isTwoPair(p, dealer):
# 				print('-> 8. Two Pair')
				allHands.append(8)
				singleHand.append(8)
				playerHand.append(8)
				allPlayerHands.append([i,8])
			if isPair(p, dealer):
# 				print('-> 9. Pair')
				allHands.append(9)
				singleHand.append(9)
				playerHand.append(9)
				allPlayerHands.append([i,9])
# 			print(f"10. High Card for {str(i)} is {isHighCard(p, dealer)}")
# 			print('-----------------------------')
			p_out[i] = {'hands' : playerHand, 'high_card' : isHighCard(p, dealer)}
	
	
		try:
			highestHand.append(min(singleHand))
		except ValueError:
			continue
		
		
# 		find_winning_hand(p_out,dealer,allPlayerHands,allPlayers)
	
	
	print("######################################")
	allSeries = pd.Series(index=[1,2,3,4,5,6,7,8,9],dtype=str,
						  data=['Royal Flush','Straight Flush', 'Four of a Kind',
							  'Full House','Flush','Straight','Three of a Kind','Two Pair','Pair'],
						  name='Hand')
	results = pd.Series(allHands,dtype=int).value_counts()
	results.name='results'
	comp = pd.merge(allSeries, results, left_on=allSeries.index, right_on=results.index, how='left')
	comp.fillna(0,inplace=True)
	
	
	print(comp[['key_0','Hand','results']])
	
	### print the highest card per round distribtuuon
	print("winning hand counts")
	temp = pd.Series(highestHand).value_counts().sort_index()
	temp.name='out'
	sim_results = pd.merge(allSeries,temp, left_on=allSeries.index, right_on=temp.index, how='left')
	print(sim_results)
	
	print(pd.Series(highestHand).quantile(q=[0.25,0.5,0.75]))
