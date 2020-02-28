#!/usr/env/bin python3
import Board
import MCTS
import os
from copy import deepcopy
import random

#if __name__=="__main__":
def NN(x):
    return ([random.random() for i in range(25)],random.random())
'''
folder_name="/home/david/Documents/myalphago"
if os.getcwd()!=folder_name
    os.chdir(folder_name)
'''
print("initializing a board b...")
b=Board.Board(5,5,3)
b.print_board()
print("making a move")
b.move(12)
b.print_board()
print("after move, current player is ",b.current_board_player(),", should be 1")
print("making another move")
b.move(11)
b.print_board()
print("after move, current player is ",b.current_board_player(),", should be 0")
b.move(7)
b.move(6)
print("after making few moves, the board has reached")
b.print_board()
print("Will the game end if player plays at (1,2)? goalcheck gives ",b.move(2))

print("=============================================")
print("check copy functionality. resetting Board")
b.reset_board()
b.move(12)
b.move(11)
b.print_board()
c=deepcopy(b)
print("make c a copy of b, and move at (3,4)")
c.move(13)
print("print c, then print b")
c.print_board()
b.print_board()
print("==============================================")
print("check mcts_node functionality. Define a node using b")
n=MCTS.mcts_node(None,None,b)
print("node status:")
n.print_node()
print("print board object in node: ",n.board)
print("try explicitly expanding node")
n.expand(NN)
print("get root:")
n.print_node()
print("get successors:")
n.print_successors()


def NN(x):
    return ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],1.0)
print("==============================================")
print("test tree functionality. Initialize a trivial board ")
b=Board.Board(4,4,3)
t=MCTS.mcts(b,NN)
print("perform 1 simulation")
t.simulation()
print("check results")
print("Current state of the root:")
t.root.print_node()
print("Current state of the successors:")
t.root.print_successors()
print("check get_stronger_pi. Initialize b again")
b=Board.Board(4,4,3)
t=MCTS.mcts(b,NN)
print("check initial state")
t.root.print_node()
print("simulation 1")
t.simulation()
print("check root after simulation")
t.root.print_node()
print("simulation 2")
t.simulation()
print("check root after simulation 2")
t.root.print_node()
print("location of root: ",t.root)
print("check successor of root after simulation")
for i in t.root.successors:
    if not i.need_expansion:
        i.print_node()


import Board
import MCTS

b=Board.Board(4,4,3)
def NN(x):
    return ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],1.0)


t=MCTS.mcts(b,NN)
t.get_stronger_pi(sim_num=2)

import random
import Board
import MCTS
import policy_value_net as pvn
import math
NN = pvn.PolicyValueNet(3,3)
print("test terminal cases")
print("test winning on last move")
G=Board.Board(3,3,3)
G.move(6)
G.move(4)
G.move(2)
G.move(5)
G.move(3)
G.move(0)
G.move(8)
G.move(1)
G.move(7)
G.print_board()
print("is winner player 0?")
print(G.winner==0)
print("does terminal node at last move have value -1?")
t=MCTS.mcts(G,NN)
t.simulation()
print(t.root.v==-1)
print("does one state before terminal have positive value?")
G=Board.Board(3,3,3)
G.move(6)
G.move(4)
G.move(2)
G.move(5)
G.move(3)
G.move(0)
G.move(8)
G.move(1)
t=MCTS.mcts(G,NN)
t.root.print_node()
t.simulation()
t.simulation()
t.root.print_node()
t.root.print_successors()
print("does simulations at near ending find optimal move?")
G=Board.Board(3,3,3)
G.move(6)
G.move(4)
G.move(2)
G.move(5)
G.move(3)
G.move(0)
t=MCTS.mcts(G,NN)
t.root.print_node()
for _ in range(20):
    t.simulation()

t.root.print_node()
print([(-child.Q + child.p*math.sqrt(t.root.N)/(1+child.N),move) for move,child in t.root.childs.items()])

G=Board.Board(3,3,3)
G.move(6)
G.move(4)
G.move(2)
G.move(5)
G.move(3)
G.move(0)
G.move(8)
G.move(7)
G.move(1)
t=MCTS.mcts(G,NN)

print([(-child.Q + child.p*math.sqrt(t.root.N)/(1+child.N),move) for move,child in t.root.childs.items()])
t.simulation()
print([(-child.Q + child.p*math.sqrt(t.root.N)/(1+child.N),move) for move,child in t.root.childs.items()])
t.root.print_node()
t.simulation()
t.root.print_node()
t.root.print_successors()
t.simulation()
t.root.print_node()
t.root.print_successors()
