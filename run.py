import Board as brd
bd = brd.Board(5,5,3)
bd.init_board()
#bd.print_board()
t1 = bd.current_board_player() == 0
t2 = bd.valid_board_moves() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
t3 = bd.move_location(0) == [0,0]
t4 = bd.move_location(11) == [2,1]
t5 = bd.move(12)
t6 = bd.current_board_player() == 1
t7 = bd.move(11)
t8 = bd.move(10)
t9 = bd.move(9)
t10 = bd.move(23)
t11 = bd.move(24)
t12 = bd.move(16)
t13 = bd.move(17)
game,player = bd.move(8)
t14 = game == True
t15 = player == 0
#bd.print_board()
if t1 and t2 and t3 and t4 and t5 and t6 and t7 and t8 and t9 and t10 and t11 and t12 and t13 and t14 and t15:
	print("Unit Test Passed")
else:
	print("Unit Test Failed")