Design Choices in branch prototype_v1:

Board:
-valid moves is an array of bool
-board is a 3d array in the form CWH
-players are 0 and 1
-The reward is absolute.

MCTS_node:


MCTS_tree:
-the pi vector must be as long as the board, for future training purposes
-

Neural Network:
-inputs board, output policy and value
-the value is always in the channel 0 player's perspective
-the value is between -1 and 1. 1 means the current player is winning
  -1 means the opponent is winning
-the value is relative
