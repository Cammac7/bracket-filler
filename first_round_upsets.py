import pandas
import sys
import argparse
import numpy
import matplotlib
import matplotlib.pyplot as plt

def readCL():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("--outfile",type=argparse.FileType("r"),default=sys.stdout)
    args = parser.parse_args()
    return args.infile, args.outfile
def upset(j):
    if j['ROUND'] == 'First Round' and j['SEED']>j['OPP_SEED'] and j['SCORE']>j['OPP_SCORE']:
        return 1
    elif j['ROUND'] == 'First Round' and j['SEED']<j['OPP_SEED'] and j['SCORE']<j['OPP_SCORE']:
        return 1
    else:
        return 0



if __name__ == "__main__":
    infile, outfile = readCL()
    df = pandas.read_csv(infile)
    df['UPSET'] = df.apply(upset,axis=1)
    yearlyUpsets = df.groupby('YEAR')['UPSET'].sum()
    print(yearlyUpsets.describe())
    yearlyUpsets.plot()
    plt.show()
    print(yearlyUpsets)
