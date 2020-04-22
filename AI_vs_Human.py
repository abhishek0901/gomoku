# This class is for AI vs Human Game
import GAME
import policy_value_net as pvn
import random
import matplotlib.pyplot as plt
import numpy as np


class AIVsHuman:
    def __init__(self,n,n_row,trained_model = 'New_Trained_Model_1.dt',sim_per_game=10):
        self.n = n
        self.n_row = n_row
        self.p0 = pvn.PolicyValueNet(n, n, trained_model)
        self.sim_per_game = sim_per_game
        self.g = GAME.Game(self.p0, self.p0, n, n_row)
    def play_game(self):
        game_end = False
        while not game_end:
            print("Current Player : AI")
            self.g.state.print_board()
            game_end,winner = self.g.play_move(self.sim_per_game,1.0)
            print("Current Player : YOU")
            self.g.state.print_board()
            if not game_end:
                mv = int(input("Your Turn Enter Move : "))
                while mv not in self.g.state.valid_board_moves():
                    mv = int(input("Invalid move try again : "))
                game_end,winner = self.g.state.move(mv)
        print("Winner is : ",winner)

ai_vs_human = AIVsHuman(5,4,'New_Trained_Model_200.dt',400)
ai_vs_human.play_game()