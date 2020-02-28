import math
import numpy as np

class Board(object):

	'''
	Game Board

	Example for 5 X 5 it will be

	| - - - - - |
	| * * * * * |
	| * * * * * |
	| * * * * * |
	| * * * * * |
	| * * * * * |
	| - - - - - |

	--------------------------

	| - - - - - - - -|
	| 00 01 02 03 04 |
	| 05 06 07 08 09 |
	| 10 11 12 13 14 |
	| 15 16 17 18 19 |
	| 20 21 22 23 24 |
	| - - - - - - - -|

	NOTE:-
	1. The board will always be with respect to 0th player
	2. The
	'''

	def __init__(self,width,height,n_in_row):
		#Initialize parameters of board
		self.width = width
		self.height = height
		self.n_in_row = n_in_row
		self.players = [0,1]
		self.winner = -1
		self.is_terminated = False
		self.init_board()
	def init_board(self,start_player=0):
		#initialize or reset board states
		if self.width < self.n_in_row or self.height < self.n_in_row:
			return False
		self.current_player = self.players[start_player]
		self.valid_moves = list(range(self.width * self.height))
		self.board = np.zeros((len(self.players),self.width,self.height))
		self.is_end = False
		self.winner = None
		return True
	def move_location(self,move):
		# Input - Move
		# Return - Co ordinates in a (i,j) plane
		h = move // self.width
		w = move % self.width
		return [h,w]
	def location_move(self,location):
		# Input - (i,j)
		# Return - Move
		if len(location) != 2:
			return -1
		return location[0] * self.width + location[1]
	def current_state(self):
		# Input - NA
		# Return - A numpy array 3D - state
		# state[0] - Board with respect to current player
		# state[1] - Board with respect to opponent player

		return [self.board[self.current_player],self.board[(self.current_player+1)%2]]

	def move(self,move):
		# Input - move
		# Return - True if done False otherwise
		if self.is_end:
			print("Game already ended")
			return (True,self.winner)
		if move in self.valid_moves:
			location = self.move_location(move)
			self.board[self.current_player][location[0]][location[1]] = 1
			self.valid_moves.remove(move)
			self.is_end = self.is_game_end(self.board[self.current_player],location)
			if self.is_end:
				self.winner=self.current_player
				return (self.is_end,self.current_player)

			self.current_player = (self.current_player+1)%2
			return (False,-1)
		else:
			return (False,-1)

	def setTerminal(self):
		self.winner = self.current_player
		self.is_terminated = True

	def game_terminated(self):
		return self.is_terminated

	def get_winner(self):
		if game_terminated():
			return self.winner
		return -1

	def is_game_end(self,current_board,location):
		# Input - NA
		# Returns True if game has ended False otherwise
		i = location[0]
		j = location[1]
		n_in_row = self.n_in_row

		#Horizontal
		cnt=1
		for k in range(1,n_in_row):
			if i+k < self.width and current_board[i+k][j] == 1:
				cnt += 1
			else:
				break

		for k in range(1,n_in_row):
			if i-k >= 0 and current_board[i-k][j] == 1:
				cnt += 1
			else:
				break

		if cnt >= self.n_in_row:
			self.setTerminal()
			return True

		#Vertical
		cnt = 1
		for k in range(1,n_in_row):
			if j+k < self.height and current_board[i][j+k] == 1:
				cnt += 1
			else:
				break

		for k in range(1,n_in_row):
			if j-k >= 0 and current_board[i][j-k] == 1:
				cnt += 1
			else:
				break

		if cnt >= self.n_in_row:
			self.setTerminal()
			return True

		#Diagonal 1
		cnt = 1
		for k in range(1,n_in_row):
			if i+k < self.width and j+k < self.height and current_board[i+k][j+k] == 1:
				cnt += 1
			else:
				break
		for k in range(1,n_in_row):
			if i-k >= 0 and j-k >= 0 and current_board[i-k][j-k] == 1:
				cnt += 1
			else:
				break
		if cnt >= self.n_in_row:
			self.setTerminal()
			return True

		#Diagonal 2
		cnt = 1
		for k in range(1,n_in_row):
			if i-k >= 0 and j+k < self.height and current_board[i-k][j+k] == 1:
				cnt += 1
			else:
				break
		for k in range(1,n_in_row):
			if i+k < self.width and j-k >= 0 and current_board[i+k][j-k] == 1:
				cnt += 1
			else:
				break
		if cnt >= self.n_in_row:
			self.setTerminal()
			return True

		if len(self.valid_board_moves()) == 0:
			self.current_player = 0.5
			self.setTerminal()
			return True

		return False
	def current_board_player(self):
		# Input - NA
		# Return - Index of current player
		return self.current_player
	def valid_board_moves(self):
		# Input - NA
		# Returns - List of valid moves
		return self.valid_moves
	def reset_board(self):
		# Input - NA
		# Return True, False otherwise
		self.init_board()
	def print_board(self):
			current_board = self.board
			print("============================================")
			for j in range(self.height):
				print()
				for i in range(self.width):
					print(int(current_board[0][j][i] + 2 * current_board[1][j][i]),end =" ")
			print("\n============================================")
