# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 17:46:24 2021

@author: nikol
"""


import dash

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import dash_table

from datetime import date, timedelta, datetime

import pandas as pd
import numpy as np
import os

from poker_TH import *

# mainFolder = os.getcwd()
# print(mainFolder)

# cardDeck = make_new_deck()
# dealer = Dealer()
# allPlayers = []


app = dash.Dash(
    __name__,
    title="Poker - TH",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no",
        }
    ],
	external_stylesheets=[dbc.themes.BOOTSTRAP],
	# requests_pathname_prefix='/poker/' ## need for webpage..
)
app._favicon= "favicon.ico" ## make assets folder and put favicon in it..



def return_PNG(card='back'):
	filename=f'PNG/{card}.png'
	theCard = html.Div(
				className='row',
				children=[
				html.Div(
					className='col',
					children=[
					# html.Img(
					dbc.CardImg(
						className='img-responsive',
						src=app.get_asset_url(filename))
					])
				]
			)

	return theCard

def return_possible_hands(p, dealer):
	possibleHands = []
	if isRoyalFlush(p,dealer):
		possibleHands.extend(['1. Royal Flush!',html.Br()])
	if isStraightFlush(p,dealer):
		possibleHands.extend(['2. Straight flush',html.Br()])
	if isFourOfAKind(p,dealer):
		possibleHands.extend(['3. Four of a kind!',html.Br()])
	if isFullHouse(p,dealer):
		possibleHands.extend(['4. Full House',html.Br()])
	if isFlush(p, dealer):
		possibleHands.extend(['5. Flush',html.Br()])
	if isStraight(p,dealer):
		possibleHands.extend(['6. Straight',html.Br()])
	if isThreeOfAKind(p, dealer):
		possibleHands.extend(['7. Three of a Kind',html.Br()])
	if isTwoPair(p, dealer):
		possibleHands.extend(['8. Two Pair',html.Br()])
	if isPair(p, dealer):
		possibleHands.extend(['9. Pair',html.Br()])
	possibleHands.extend([f'10. High Card for {isHighCard(p, dealer)}',html.Br()])

	return possibleHands



def make_all_player_cards(numOfPlayers, viewAll='No', flopClicked=False):
	print('make_all_player_cards')
	children = []
	# print(allPlayers)
	for p in range(1,numOfPlayers+1):
		if p == 1:
			Text = "Player 1 (Me)"
			card1 = allPlayers[p-1].card1
			card2 = allPlayers[p-1].card2
		else:
			if viewAll == 'Yes':
				card1 = allPlayers[p-1].card1
				card2 = allPlayers[p-1].card2
			else:
				card1 = 'back'
				card2 = 'back'				
			Text = f"Player {p}"

		if flopClicked == False:
			prob = ["Your current probability -"," best hand"]
			possprob = "Possible probability -  best hand with remaining undealt cards"
		if flopClicked == True:
			prob = return_possible_hands(allPlayers[p-1],dealer)
			possprob = "TBD"	

		children += [
			html.Label(Text),
			html.Div(
				className='container justify-content-center',
				children=[

					html.Div(
						id=f'player-{p}',
						className='row',
						children=[
							# html.Label(Text),
							html.Div(
								id=f'player-{p}-c1',
								className='col',
								children=[return_PNG(card1)]),
							html.Div(
								id=f'player-{p}-c2',
								className='col',
								children=[return_PNG(card2)]),
							html.Div(
								id=f'player-{p}-prob',
								className='col',
								children=[
									html.P(prob, style={'fontSize':'2vh'})
								]
							),
							html.Div(
								id=f'player-{p}-poss-prob',
								className='col',
								children=[
									html.P(possprob, style={'fontSize':'2vh'})
								]
							),
						],
					),
				]
			),
			html.Hr()
		]
	return children

def initialize_player_dealer(numPlayers):
	global cardDeck
	global allPlayers 
	global dealer
	print("initializing new round...")

	cardDeck = make_new_deck()
	allPlayers = []
	dealer = Dealer()
	dealer.card1=''
	dealer.card2=''
	dealer.card3=''
	dealer.card4=''
	dealer.card5=''
		
	for p in range(0,numPlayers):
		allPlayers.append(Player())

	give_player_card(allPlayers, cardDeck)
	give_player_card(allPlayers, cardDeck)	

	
###############################################################################
###############################################################################
app.layout = html.Div(
		children=[
			html.H2([html.A('Poker - Beta', style={'text-decoration':'none','color':'black'})],style={ 'textAlign':'center'}),
			# html.H2("Poker - Beta", style={"textAlign":'center','margin-top':'10px','padding-top':'0px'}),
			html.Div(
				className='d-flex justify-content-center',
				children=[
					html.Div(
						id="num-of-players",
						className='p-2',								
						children=[
							html.Label("Number of Players", style={'fontSize':'2vh'}),
							dcc.Dropdown(
								id="player-count",
								options=[{'label': i, 'value': i} for i in np.arange(2,11)],
								# value=2,
								multi=False,
								clearable=False
							),
						],
					),
					html.Div(
						id='see-cards',
						className='p-2',
						children=[
							html.Label("See all cards?", style={'fontSize':'2vh'}),
							dcc.RadioItems(
								id='see-cards-choice',
								options=[
									{'label':'Yes','value':'Yes'},
									{'label':'No','value':'No'}
									],
								value='No',
								inputStyle={'margin':'8px'}
							),
						]
					),
					html.Div(
						id='start-button',
						className='p-2',
						children=[
							dbc.Button("Start / Reshuffle", 
										id='start-button-2',
										disabled=True,
										color="primary",
										size="md lg",
										block=True,
										className="mr-2"),					
							dbc.Tooltip(
								"After setting number of players, click to shuffle the deck and start!",
								target='start-button-2',
								placement='top'
							)	
						],
					),
				], 
			),
			html.Hr(),
			html.Div(
				children=[
					html.Label("Dealer's Hand", className='p-2'),
					html.Div(
						id='dealer-hand',
						className='container justify-content-center',
						children=[
							html.Div(
								className='row',
								children=[
									# dbc.Container([
										# dbc.CardGroup([
											html.Div(
												id='dealer-1',
												className='col d-flex align-items-stretch',
												children=[return_PNG('back')]),
											
											html.Div(
												id='dealer-2',
												className="col d-flex align-items-stretch",
												children=[return_PNG('back')]),
											
											html.Div(
												id='dealer-3',
												className="col d-flex align-items-stretch",
												children=[return_PNG('back')]),
											
											html.Div(
												id='dealer-4',
												className="col d-flex align-items-stretch",
												children=[return_PNG('back')]),
											
											html.Div(
												id='dealer-5',
												className="col d-flex align-items-stretch",
												children=[return_PNG('back')]),
										# ]),
									# ]),
								],
							),
						],
					),
				],
			),
			html.Hr(),
			html.Label("Actions",className='p-1'),			
			html.Div(
				id='buttons',
				children=[
					html.Div(
						className='row p-1 justify-content-center',
						children=[
							dbc.Button( "Flop",
										id='flop-button',
										disabled=True,
										color="primary",
										size='lg',
										className="col-3 mr-1 btn btn-primary btn-lg"
							),
							dbc.Button( "Turn",
										id='turn-button',
										disabled=True,
										color="secondary",
										size='lg',
										className="col-3 mr-1 btn btn-primary btn-lg"
							),
							dbc.Button( "River",
										id="river-button",
										disabled=True,
										color="success",
										size='lg',
										className="col-3 mr-1 btn btn-primary btn-lg"
							),
						],
					),
				],
			),
			html.Hr(),
			html.Div([
				html.Div(id='player-cards', className='container')		
			]),
		],
	)



############################################################################################
############################################################################################


@app.callback(
	Output('start-button-2','disabled'),
	Input('player-count','value'))
def enable_start_button(val):
	print(f"number of players: {val}")
	if val == None:
		return True
	else:
		if isinstance(val,int):
			return False
		else:
			return True


@app.callback(
	Output('flop-button','disabled'),
	Output('turn-button','disabled'),
	Output('river-button','disabled'),
	Output('dealer-1','children'),
	Output('dealer-2','children'),
	Output('dealer-3','children'),
	Output('dealer-4','children'),
	Output('dealer-5','children'),
	Output('player-cards','children'),
	Input('start-button-2','n_clicks'),
	Input('player-count','value'),	
	Input('see-cards-choice','value'),
	Input('flop-button','n_clicks'),
	Input('turn-button','n_clicks'),
	Input('river-button','n_clicks'),
	Input('dealer-1','children'),
	Input('dealer-2','children'),
	Input('dealer-3','children'),
	Input('dealer-4','children'),
	Input('dealer-5','children'))
def enable_dealer_buttons(start, numOfPlayers, view_cards, flop, turn, river, d1_child, d2_child, d3_child, d4_child, d5_child):
	ctx = dash.callback_context


	flop_disabled = True
	turn_disabled = True
	river_disabled = True
	dealer_1_child = return_PNG('back')
	dealer_2_child = return_PNG('back')
	dealer_3_child = return_PNG('back')
	dealer_4_child = return_PNG('back')
	dealer_5_child = return_PNG('back')

	players_cards_child = []

	for vals in ctx.triggered:
		if vals['prop_id'] == 'start-button-2.n_clicks':
			initialize_player_dealer(numOfPlayers)
			make_all_player_cards(numOfPlayers, view_cards)
			flop_disabled, turn_disabled, river_disabled = False, False, False
			players_cards_child = make_all_player_cards(numOfPlayers, view_cards, flopClicked=False)
			try:
				flop.n_clicks, turn.n_clicks, river.n_clicks = 0, 0, 0
			except AttributeError:
				pass

		if vals['prop_id'] == 'flop-button.n_clicks':
			if dealer.card3 == '':
				give_dealer_card(dealer, cardDeck)
				give_dealer_card(dealer, cardDeck)
				give_dealer_card(dealer, cardDeck)
				dealer_1_child, dealer_2_child, dealer_3_child =  \
				return_PNG(dealer.card1), return_PNG(dealer.card2), return_PNG(dealer.card3)
			elif dealer.card3 != '':
				dealer_1_child, dealer_2_child, dealer_3_child =  \
				return_PNG(dealer.card1), return_PNG(dealer.card2), return_PNG(dealer.card3)
			flop_disabled, turn_disabled, river_disabled = False, False, False
			players_cards_child = make_all_player_cards(numOfPlayers, view_cards, flopClicked=True)

		if vals['prop_id'] == 'turn-button.n_clicks':
			dealer_1_child, dealer_2_child, dealer_3_child =  \
				return_PNG(dealer.card1), return_PNG(dealer.card2), return_PNG(dealer.card3)
			if dealer.card4 == '':
				give_dealer_card(dealer, cardDeck)
				dealer_4_child = return_PNG(dealer.card4)
			elif dealer.card4 != '':
				dealer_4_child = return_PNG(dealer.card4)
			players_cards_child = make_all_player_cards(numOfPlayers, view_cards, flopClicked=True)
			flop_disabled, turn_disabled, river_disabled = False, False, False

		if vals['prop_id'] == 'river-button.n_clicks':
			if dealer.card5 == '':
				give_dealer_card(dealer, cardDeck)
				dealer_5_child = return_PNG(dealer.card5)
			elif dealer.card5 != '':
				dealer_5_child = return_PNG(dealer.card5)
			players_cards_child = make_all_player_cards(numOfPlayers, view_cards, flopClicked=True)
			dealer_1_child, dealer_2_child, dealer_3_child, dealer_4_child =  \
				return_PNG(dealer.card1), return_PNG(dealer.card2), return_PNG(dealer.card3), return_PNG(dealer.card4)
			flop_disabled, turn_disabled, river_disabled = False, False, False

		if vals['prop_id'] == 'see-cards-choice.value':
			flop_disabled, turn_disabled, river_disabled = False, False, False
			dealer_1_child, dealer_2_child, dealer_3_child, dealer_4_child, dealer_5_child = \
			d1_child, d2_child, d3_child, d4_child, d5_child
			if flop != None:
				players_cards_child = make_all_player_cards(numOfPlayers, view_cards, flopClicked=True)
			else:
				players_cards_child = make_all_player_cards(numOfPlayers, view_cards, flopClicked=False)

		else:
			pass
			# start_round = False
			# return True, True, True



	return flop_disabled, turn_disabled, river_disabled,\
			dealer_1_child, dealer_2_child, dealer_3_child, dealer_4_child, dealer_5_child,\
			players_cards_child






## for the website
# server = app.server


## for running locally and testing
app.run_server(debug=True,host=('192.168.0.104'),port=8050,use_reloader=True)

