import MCTS
import Board
import policy_value_net as pvn
import random
from copy import deepcopy

class Game:
    #A game has two players(2 neural nets) and a board
    def __init__(self,p0,p1,l,n):
        self.NN0=p0
        self.NN1=p1
        self.data=[]
        self.state=Board.Board(l,l,n)

    def get_move_from_prob_distribution(self,probabilityDistribution):
        r = random.random()
        cumulativeProbability = 0
        for a in range(len(probabilityDistribution)-1):
            cumulativeProbability += probabilityDistribution[a][0]
            if r <= cumulativeProbability:
                return probabilityDistribution[a][1]
        return probabilityDistribution[len(probabilityDistribution)-1][1]

    def play_move(self,sim_num=100,t=1.0):
        if self.state.current_player==0:
            tree=MCTS.mcts(deepcopy(self.state),self.NN0)
        else:
            tree=MCTS.mcts(deepcopy(self.state),self.NN1)

        prob=tree.get_stronger_pi(sim_num=sim_num,temperature=t)
        #print(prob)

        # 5 .2, 10 .5 =, 11 .3
        #print("probability from mcts: ",prob)
        move=random.choices(range(len(prob)),weights=prob)[0]
        #move = self.get_move_from_prob_distribution(prob)
        print("Current Player : ",self.state.current_board_player())
        print("Move : ",move)
        #print("Is Valid Move : ",move in self.state.valid_board_moves())

        self.data.append([deepcopy(self.state.current_state()),prob,''])
        val =  self.state.move(move)
        #print("Is Terminated : ",self.state.game_terminated())
        return val


    def play_game(self,sim_num=100):
        #play the initial move manually
        game_end,winner=self.play_move(sim_num=sim_num,t=1.0)
        self.state.print_board()
        #cntr = 2
        while not game_end:
            #print("Game Cntr : ",cntr)
            game_end,winner=self.play_move(sim_num=sim_num,t=1.0)
            self.state.print_board()
            #cntr += 1
            #TODO: adjust temperature

        self.data[0][2]=-2*winner+1
        for i in range(1,len(self.data)):
            self.data[i][2]=-self.data[i-1][2]

        return self.data

    def play_game_with_winner(self,sim_num=100):
        #play the initial move manually
        # when in the play with winner mode, both players should use strongest moves. Use higher temperature.
        game_end,winner=self.play_move(sim_num=sim_num,t=4.0)
        self.state.print_board()
        #cntr = 2
        while not game_end:
            #print("Game Cntr : ",cntr)
            game_end,winner=self.play_move(sim_num=sim_num,t=4.0)
            self.state.print_board()
            #cntr += 1
            #TODO: adjust temperature

        self.data[0][2]=-2*winner+1
        for i in range(1,len(self.data)):
            self.data[i][2]=-self.data[i-1][2]

        return winner



    def print_state(self):
        self.state.print_board()
