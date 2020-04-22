import GAME
import policy_value_net as pvn
import MCTS
import Board
from copy import deepcopy
import random
import matplotlib.pyplot as plt
import os
from os import path
import gc
import time
class StoreStats:
    def __init__(self,dirname,outfile):
        self.dirname = dirname
        self.n = 5
        self.n_row = 4
        self.sim_per_game = 50
        self.game_count = 10
        self.plyer = [0, 0, 0]
        self.output_file = outfile

    def trained_net_as_first_player(self,filename):
        self.p0 = pvn.PolicyValueNet(self.n, self.n, filename)
        self.p1 = pvn.PolicyValueNet(self.n, self.n)

    def trained_net_as_second_player(self,filename):
        self.p0 = pvn.PolicyValueNet(self.n, self.n)
        self.p1 = pvn.PolicyValueNet(self.n, self.n,filename)

    def reset(self):
        self.plyer = [0, 0, 0]
        print("******************************",gc.get_count(),"**************************************")
        gc.collect()
        time.sleep(10)

    def show_stats(self):
        for j in range(self.game_count):
            g = GAME.Game(self.p0, self.p1, self.n, self.n_row)
            winner = g.play_game_with_winner(self.sim_per_game)
            print(winner)
            if winner != 0.5:
                self.plyer[winner] += 1
            else:
                self.plyer[2] += 1

        print("0th player Win - ", self.plyer[0])
        print("1st player Win - ", self.plyer[1])
        print("Draw - ", self.plyer[2])

        f = open(self.output_file,'a+')
        f.write(str(self.plyer[0]) + ',' + str(self.plyer[1]) + ',' + str(self.plyer[2]) + '\n')
        f.close()

    def run_stats(self,nn_player = 0):
        for cnt in range(10 + 168,201):
            filename = 'New_Trained_Model_' + str(cnt) + '.dt'
            self.reset()
            if path.exists(self.dirname + '/' + filename):
                if nn_player == 0:
                    self.trained_net_as_first_player(self.dirname + '/' + filename)
                else:
                    self.trained_net_as_second_player(self.dirname + '/' + filename)

                self.show_stats()

st_stats = StoreStats('/Users/abhi/Documents/neu/Fun_Projects/Gomoku/gomoku_gitlab/alphagomoku/data_files','second_player.csv')
st_stats.run_stats(1)