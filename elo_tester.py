import sys
import numpy
import pandas

eloFile = "test_elo_file.csv"
tourneyfile = "NCAAtourneydata_all.csv"
teamNames = "teamnamematchset.csv"

elo_names = ['year', 'team' ,'elo']
tourney_names = ['YEAR','ROUND','SEED','TEAM','SCORE','OPP_SEED','OPPONENT','OPP_SCORE','SCORE_DIFF','RESULT']
teamNames_names = ['Games','NCAA']

eloDataset = pandas.read_csv(eloFile)
tourneyDataset = pandas.read_csv(tourneyfile)
namematchDataset = pandas.read_csv(teamNames)

namesHash = dict(zip(namematchDataset['NCAA'], namematchDataset['Games']))

for k, v in namesHash.items():
    print(k, v)

def nameswitch(x):
    return namesHash[x]

#print(tourneyDataset.head(20))

tourneyDataset['TEAM'].map(nameswitch)
tourneyDataset['OPPONENT'].map(nameswitch)

#eloDataset['score'] = 0

#print(eloDataset.head(20))

newset = tourneyDataset.merge(eloDataset,on=['TEAM','YEAR'])

print(newset.head(20))
