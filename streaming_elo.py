#!/usr/bin/env python
import math
import pandas as pd
import argparse
import date
import sys
from jtutils import to_years, threewise

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


def elo_dfs(infile):
    df = pd.read_csv(infile)
    df = df[df.apply(lambda r: r["Result"].split()[0] == "W", axis = 1)]
    elo_dict = {}
    starting_elo = 1500
    for las, cur, nex in threewise(df.iterrows()):
        cur_yr = str(int(round(to_years(cur[1]["Date"]))))
        if nex:
            nex_yr = str(int(round(to_years(nex[1]["Date"]))))
        else:
            nex_yr = ""

        _, row = cur
        p1 = row["Schl"].strip()
        p2 = row["Opp"].strip()

        # p1 = row["Winner"].strip()
        # p2 = row["Loser"].strip()
        p1_elo = elo_dict.get(p1,starting_elo)
        p2_elo = elo_dict.get(p2,starting_elo)
        elo_dict[p1] = elo_update(p1_elo, p2_elo, 1)
        elo_dict[p2] = elo_update(p2_elo, p1_elo, 0)
        if nex_yr != cur_yr:
            elo_df = pd.DataFrame(elo_dict.items(),columns=["name","elo"])
            elo_df["year"] = cur_yr
            sys.stderr.write(cur_yr + "\n")
            yield elo_df

if __name__ == "__main__":
    infile, outfile = readCL()
    all_elo_dfs = list(elo_dfs(infile))
    out_df = pd.concat(all_elo_dfs)
    out_df.to_csv(outfile, index=False)
