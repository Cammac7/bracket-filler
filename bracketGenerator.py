import pandas
import matplotlib
import matplotlib.pyplot as plt
class team:
    rank = 0

def pick_Winner():
    tourn_round = int(input('Round: '))
    team1_seed = int(input('Team 1 Seed: '))
    team2_seed = int(input('Team 2 Seed: '))

round1data = {"Seed":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"1win_pct": [100.0,93.8,83.6,79.7,64.1,64.1,60.9,50.0,50.0,39.1,35.9,35.9,25.5,16.4,6.3,0.0]}

round1df = pandas.DataFrame(round1data)
round1odds = round1df.set_index('Seed')

round1odds.plot()
plt.show()

