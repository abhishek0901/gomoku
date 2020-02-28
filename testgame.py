import GAME
import policy_value_net as pvn
import MCTS
import Board
from copy import deepcopy

n=9
p0=pvn.PolicyValueNet(n,n)
p1=pvn.PolicyValueNet(n,n)
'''
b=Board.Board(5,5,3)
tree=MCTS.mcts(b,p0)
tree.get_stronger_pi(sim_num=100)
'''
g=GAME.Game(p0,p1,n,5)
t1 = g.state.current_board_player() == 0
g.play_move()
t2 = g.state.current_board_player() == 1
g.print_state()
g.play_move()
t3 = g.state.current_board_player() == 0
g.print_state()

if t1 and t2 and t3:
	print("Test Passed")
else:
	print("Test Failed")

g.play_game(30)
g.print_state()
