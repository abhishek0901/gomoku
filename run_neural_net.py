import Board as brd
import policy_value_net as pvn
bd = brd.Board(5,5,3)
bd.init_board()

pvn = pvn.PolicyValueNet(5,5)
next_move,value = pvn.get_move(bd.current_state())

print(next_move,value)

bd1 = brd.Board(5,5,3)
bd1.init_board()
bd2 = brd.Board(5,5,3)
bd2.init_board()
bd2.move(2)
bd3 = brd.Board(5,5,3)
bd3.init_board()
bd3.move(4)
bd3.move(5)
bd4 = brd.Board(5,5,3)
bd4.init_board()
bd4.move(1)
bd4.move(3)
bd4.move(9)
bd5 = brd.Board(5,5,3)
bd5.init_board()
bd4.move(1)
bd4.move(8)
bd4.move(6)
bd4.move(2)

pi1 = [0,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pi2 = [0,0,0,0,0.8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pi3 = [0,0,0,0.99,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pi4 = [0,0,0,0,0.88,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pi5 = [0,0,0,0,0,0.9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

v1 = 0.02
v2 = 0.01
v3 = 0.09
v4 = 0.08
v5 = 0.09

prob,val = pvn.get_move(bd1.current_state())
print(prob,val)

prob,val = pvn.get_move(bd2.current_state())
print(prob,val)

prob,val = pvn.get_move(bd3.current_state())
print(prob,val)

prob,val = pvn.get_move(bd4.current_state())
print(prob,val)

prob,val = pvn.get_move(bd5.current_state())
print(prob,val)

pvn.train_step([bd1.current_state(),bd2.current_state(),bd3.current_state(),bd4.current_state(),bd5.current_state()],[pi1,pi2,pi3,pi4,pi5],[v1,v2,v3,v4,v5],0.01,100)


pvn.save_model("test_weightts.md5")
print("Test Passed")