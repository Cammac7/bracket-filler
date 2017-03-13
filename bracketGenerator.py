import sys
import scipy
import numpy
import sklearn
import pandas
import matplotlib

#libraries
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

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
scatter_matrix(round1odds)
plt.show()

