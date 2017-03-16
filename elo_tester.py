import sys
import numpy
import pandas

eloFile = "test_elo_file.csv"
tourneyfile = "NCAA_Tourney_Data.csv"
teamNames = "teamnamematchset.csv"

elo_names = ['year', 'team' ,'elo']
tourney_names = ['YEAR','ROUND','SEED','TEAM','SCORE','OPP_SEED','OPPONENT','OPP_SCORE','RESULT']
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

tourneyDataset['TEAM'] = tourneyDataset['TEAM'].map(nameswitch)
tourneyDataset['OPPONENT'] = tourneyDataset['OPPONENT'].map(nameswitch)

#eloDataset['score'] = 0

#print(eloDataset.head(20))

newset = tourneyDataset.merge(eloDataset,on=['TEAM','YEAR'])
eloDataset.columns = ['YEAR','OPPONENT','OPP_ELO']
newerset = newset.merge(eloDataset,on=['OPPONENT','YEAR'])

def calcscore(j):
    if j['ELO'] > j['OPP_ELO'] and j['RESULT']=='WIN':
        return 1
    elif j['ELO']<j['OPP_ELO'] and j['RESULT']=='LOSS':
        return 1
    else:
        return -1

   
newerset['ELOSCORE'] = newerset.apply(calcscore,axis=1)

newerset.to_csv('testexport.csv')
print(newset.head(20))
