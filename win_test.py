import GAME
import policy_value_net as pvn
import MCTS
import Board
from copy import deepcopy
import random
import matplotlib.pyplot as plt

random.seed(1)

n = 5
n_row = 3
p0 = pvn.PolicyValueNet(n,n)
p1 = pvn.PolicyValueNet(n,n,"New_Trained_Model_2.dt")
sim_per_game = 10

game_count = 300
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