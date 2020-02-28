import math
from copy import deepcopy
import random

class mcts_node:
    def __init__(self,board,p=0.0):

        self.G=board                        #current state
        self.N=0.0
        self.Q=0.0
        self.W=0.0
        self.is_leaf = True
        self.v=0.0
        self.p=p
        self.childs = {}

    def expand(self,NN):
        if self.G.game_terminated():
            self.v = 0 if self.G.winner==None or self.G.winner==0.5 or self.G.winner==-1 else -1
        else:
            result=NN.get_move(self.G.current_state())
            pi,self.v=result[0][0],result[1][0]

            for i in self.G.valid_moves:
                tmp=deepcopy(self.G)
                tmp.move(i)
                self.childs[i]=mcts_node(tmp,p=pi[i])

    def sample(self,c=1.0):
        #return child with highest utility
        utilities = [(-child.Q + c*child.p*math.sqrt(self.N)/(1+child.N),move) for move,child in self.childs.items()]
        return self.childs[max(utilities)[1]]

    def print_node(self):
        print("========================================")
        print("current_node:")
        self.G.print_board()
        print("Statistics: W=%f, Q=%f, N=%f, v=%f, p=%f" % (self.W,self.Q,self.N,self.v,self.p))
        print("is leaf? ",self.is_leaf,"Terminal : ",self.G.game_terminated())
        print("========================================")

    def print_successors(self):
        #print the first two successors
        for i in self.childs:
            self.childs[i].print_node()

class mcts:
    '''
    An important realization: because mcts is a self play algorithm, there should only be 1 neural network involved.
    Because all the rollouts should be done using the same NN, the NN should be defined while initializing
    other numbers like sim_num and temperature can be adjusted

    MCTS is called when a player needs to make a move, so the root node is never terminal
    '''
    def __init__(self,board,NN):
        self.root=mcts_node(board)
        self.NN=NN

    def update_edge(self,node,v):
        node.W += v
        node.N += 1
        node.Q = node.W/node.N

    def simulation(self):
        return self.simulation_at_node(self.root)

    def simulation_at_node(self,node):
        #node.print_node()
        if node.is_leaf:
            node.expand(self.NN)
            if not node.G.game_terminated():
                node.is_leaf = False
            v=node.v
        else:
            v = self.simulation_at_node(node.sample())
        self.update_edge(node,v)
        return -v

    def get_stronger_pi(self,sim_num=400,temperature=2.0):
        for i in range(sim_num):
            self.simulation()

        PI = [0 for i in range(self.root.G.width*self.root.G.height)]

        if self.root.G.game_terminated():
            return PI
        else:
            for i in self.root.childs:
                PI[i]=self.root.childs[i].N**temperature
            s=sum(PI)
            for i in range(len(PI)):
                PI[i]=PI[i]/s
            return PI
