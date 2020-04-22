import matplotlib.pyplot as plt

first_player = []
second_player = []
draw = []
f = open("/Users/abhi/Documents/neu/Fun_Projects/Gomoku/gomoku_gitlab/alphagomoku/first_player.csv",'r')
lns = f.readlines()
for ln in lns:
    ln = ln.strip()
    a, b, c = ln.split(',')
    first_player.append(int(a))
    second_player.append(int(b))
    draw.append(int(c))

#plt.plot( first_player, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
#plt.plot( second_player, marker='', color='olive', linewidth=2)
#plt.plot( draw, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
mva = []
cn = 0
for i in range(len(first_player)):
    cn = cn * (i/(i+1)) + first_player[i]/(i+1)
    mva.append(cn)

#plt.plot(mva)
plt.plot(first_player,label='First Player')
plt.plot(second_player,label='Second Player')
plt.plot(draw,label='Draws')
plt.legend()
plt.show()
