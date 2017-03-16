#!/usr/bin/env python
import math
import pandas as pd
import argparse
import sys
import jtutils
from jtutils.jtfunctions import to_years, threewise

def readCL():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("--outfile",type=argparse.FileType("r"),default=sys.stdout)
    args = parser.parse_args()
    return args.infile, args.outfile

def elo_ev(p1_elo, p2_elo):
    return (1.0 / (1.0 + math.pow(10, ((p2_elo - p1_elo) / 400.))));

def elo_update(p1_elo, p2_elo, p1_result):
    kfactor = 50
    p1_expected = elo_ev(p1_elo, p2_elo)
    p1_new = (p1_elo + kfactor * (p1_result - p1_expected));
    return p1_new

def load_tourney_start_dates():
    INFILE = "NCAA_Dates.csv"

    #eg: ['1985-03-14', '1986-03-13', '1987-03-12', '1988-03-17'...]
    start_dates = pd.read_csv("NCAA_Dates.csv")["first_Formatted"].values

    #eg: {1985:1985.24, 1986:1986.33, ...}
    year2cutoff = dict((int(dt.split("-")[0]), to_years(dt)) for dt in start_dates)
    return year2cutoff

def date_to_tourney_year(dt, year2cutoff):
    #given a date (string) of a game
    #compute the tournament year that we can use that game's data for
    #ie: if the game happens after the start of this year's
    #NCAA tournament then we can't use that data until the next year's tourney
    year_frac = to_years(dt)
    year_integer = math.floor(year_frac)
    cutoff = year2cutoff[year_integer] #the starting time of the NCAA tournament that year, expressed as a fraction
    if year_frac >= cutoff:
        return year_integer + 1
    else:
        return year_integer

def elo_dfs(infile):
    df = pd.read_csv(infile)
    df = df[df.apply(lambda r: r["Result"].split()[0] == "W", axis = 1)]
    elo_dict = {}
    starting_elo = 1500

    year2cutoff = load_tourney_start_dates()

    for las, cur, nex in threewise(df.iterrows()):
        current_game_year = date_to_tourney_year(cur[1]["Date"], year2cutoff)
        if nex:
            next_game_year = date_to_tourney_year(nex[1]["Date"], year2cutoff)
        else:
            next_game_year = ""


        _, row = cur
        p1 = row["Schl"].strip()
        p2 = row["Opp"].strip()

        # p1 = row["Winner"].strip()
        # p2 = row["Loser"].strip()
        p1_elo = elo_dict.get(p1,starting_elo)
        p2_elo = elo_dict.get(p2,starting_elo)
        elo_dict[p1] = elo_update(p1_elo, p2_elo, 1)
        elo_dict[p2] = elo_update(p2_elo, p1_elo, 0)
        #added list wrapping to elo_dict.items(). .items is a list in python2 but a VIEW in python3
        if next_game_year != current_game_year:
            elo_df = pd.DataFrame(list(elo_dict.items()),columns=["TEAM","ELO"])
            elo_df["YEAR"] = current_game_year
            sys.stderr.write(cur[1]["Date"] + '\n')
            if nex:
                sys.stderr.write(nex[1]["Date"] + '\n')
            sys.stderr.write(str(current_game_year) + "\n")
            yield elo_df

if __name__ == "__main__":
    infile, outfile = readCL()
    all_elo_dfs = list(elo_dfs(infile))
    out_df = pd.concat(all_elo_dfs)
    out_df.to_csv(outfile, index=False)
