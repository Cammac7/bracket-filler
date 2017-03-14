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

#class team:
#    rank = 0

#def pick_Winner():
#    tourn_round = int(input('Round: '))
#    team1_seed = int(input('Team 1 Seed: '))
#    team2_seed = int(input('Team 2 Seed: '))

#round1data = {"Seed":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"1win_pct": [100.0,93.8,83.6,79.7,64.1,64.1,60.9,50.0,50.0,39.1,35.9,35.9,25.5,16.4,6.3,0.0]}

path = "NCAAtourneydata_all_noteams.csv"

names = ['YEAR', 'ROUND', 'SEED', 'TEAM', 'SCORE', 'OPP_SEED', 'OPPONENT', 'OPP_SCORE', 'SCORE_DIFF', 'RESULT']
dataset = pandas.read_csv(path, names=names)

print(dataset.shape)

print(dataset.head(20))

print(dataset.describe())

print(dataset.groupby('TEAM').size())


scatter_matrix(dataset)
#Awesome, this shows that there's no correlation between anything. Sweet!
#previous comment is sarcastic
plt.show()

#Split-out validation dataset
array = dataset.values
X = array[:,0:10]
print(X)
Y = array[:,9]
print(Y)
validation_size = 0.20

#vv ok so it seems like this can be any number? just a way to seed the number generator? Double check to confirm that.
seed = 7
scoring = 'accuracy'
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

#ok, so a BUNCH of algorithm models. more as a way to test them all out.
#I've never even heard of half of these. Just pushing all the buttons on pandas
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

#evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    #As of line 76 i'm confused a bit. Onward we press.
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
