# Responsible for Training Gomoku and Playing with another player
import GAME
import policy_value_net as pvn
import MCTS
import Board
from copy import deepcopy
import random
import matplotlib.pyplot as plt
import numpy as np

class GameMaster:
	def __init__(self,n,n_row,sim_per_game=10):
		self.n = n
		self.n_row = n_row
		self.p0 = pvn.PolicyValueNet(n,n)
		self.p1 = pvn.PolicyValueNet(n,n)
		self.g  = GAME.Game(self.p0,self.p0,n,n_row)
		self.sim_per_game = sim_per_game

	def convert_data(self,data):
		train_set_board = []
		train_set_prob = []
		train_set_val = []
		for triples in data:
			train_set_board.append(triples[0])
			train_set_prob.append(triples[1])
			train_set_val.append(triples[2])
		return (train_set_board,train_set_prob,train_set_val)

	def play_game(self,num_of_games=100):
		self.data = []
		for game in range(num_of_games):
			self.g = GAME.Game(self.p0,self.p0,self.n,self.n_row)
			current_series = self.g.play_game(self.sim_per_game)
			for triples in current_series:
				self.data.append(triples)

		random.shuffle(self.data)
		train_set_board,train_set_prob,train_set_val = 	self.convert_data(self.data)

		#Neural Net Training
		print("Neural Net training")
		k=32
		cnt = 0
		total_loss = []
		total_loss_temp = []

		total_val_loss = []
		total_val_loss_temp = []
		total_ploicy_loss = []
		total_ploicy_loss_temp = []


		for iter in range(16): #Epochs
			total_loss_temp = []
			total_val_loss_temp = []
			total_ploicy_loss_temp = []
			for j in range(int(len(self.data)/k)):
				(loss,val_loss,pol_loss) = self.p0.train_step(train_set_board[j*k:k*(j+1)],train_set_prob[j*k:k*(j+1)],train_set_val[j*k:k*(j+1)],0.01,1)
				cnt = k*(j+1)
				total_loss_temp.append(loss)
				total_val_loss_temp.append(val_loss)
				total_ploicy_loss_temp.append(pol_loss)
			total_loss.append(np.mean(total_loss_temp))
			total_val_loss.append(np.mean(total_val_loss_temp))
			total_ploicy_loss.append(np.mean(total_ploicy_loss_temp))
		#if cnt < len(self.data):
		#	loss = self.p0.train_step(train_set_board[cnt:],train_set_prob[cnt:],train_set_val[cnt:],0.1,10)
		#	total_loss.append(loss)

		print("After training")

		return total_loss,total_val_loss,total_ploicy_loss

	def play_play_game_with_nn(self,num_of_games=100,iter_count=20):
		LOSS = []
		for cnt in range(iter_count):
			print("After Iteration %d "%cnt)
			loss,val_loss,pol_loss = self.play_game(num_of_games)
			plt.plot(loss,'r')
			plt.plot(val_loss,'b')
			plt.plot(pol_loss,'g')
			plt.ylabel("Loss Function for Iteration %d"%cnt)
			plt.legend(["Total Loss","Value Loss","Policy Loss"])
			plt.show()
			name = "New_Trained_Model_" + str(cnt+1) + ".dt"
			self.p0.save_model(name)
			LOSS.extend(loss)
		plt.plot(LOSS)
		plt.ylabel("Loss Function for After Training Completion")
		plt.show()

	def play_game_over_trained_network(self):
		print("Trained Network")
		self.g = GAME.Game(self.p0,self.p1,self.n,self.n_row)
		self.g.play_game(self.sim_per_game)
		self.p0.save_model("Final.dt")
		return




g1 = GameMaster(5,3,400)
g1.play_play_game_with_nn(20,100)
g1.play_game_over_trained_network()