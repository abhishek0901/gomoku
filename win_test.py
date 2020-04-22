import GAME
import policy_value_net as pvn
import MCTS
import Board
from copy import deepcopy
import random
import matplotlib.pyplot as plt
import math

random.seed(1)

n = 4
n_row = 5
p0 = pvn.PolicyValueNet(n,n)
p1 = pvn.PolicyValueNet(n,n,"New_Trained_Model_1.dt")
sim_per_game = 10


game_count = 1000
plyer = [0,0,0]
for j in range(game_count):
	g  = GAME.Game(p0,p1,n,n_row)
	winner = g.play_game_with_winner(sim_per_game)
	print(winner)
	if winner != 0.5:
		plyer[winner] += 1
	else:
		plyer[2] += 1

print("0th player Win - ",plyer[0])
print("1st player Win - ",plyer[1])
print("Draw - ",plyer[2])

'''game_count=400
player=[0,0,0]
for j in range(game_count):
	if random.random()>0.5:
		g  = GAME.Game(p0,p1,n,n_row)
		winner = g.play_game_with_winner(sim_per_game)
		if winner != 0.5:
			plyer[winner] += 1
		else:
			plyer[2] += 1
	else:
		g  = GAME.Game(p1,p0,n,n_row)
		winner = g.play_game_with_winner(sim_per_game)
		if winner != 0.5:
			plyer[1-winner] += 1
		else:
			plyer[2] += 1

	#start checking at 16 games to remove effect of black white
	if j>=15:
		if player[0]/(j+1)>0.5+math.sqrt(1/(j+1)):
			print("p0 is better")
			break
		elif player[1]/(j+1)>0.5+math.sqrt(1/(j+1)):
			print("p1 is better")
			break
print("0th player Win - ",player[0])
print("1st player Win - ",player[1])
print("Draw - ",player[2])'''
