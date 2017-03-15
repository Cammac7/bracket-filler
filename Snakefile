"allGames.csv" <-
  for f in alltheGames/*csv; do less $f | pawk -g '",School," not in l and len(r) > 1'; done | pawk -g 'i==0 or "PTS" not in l' | psort -c Date --str > $OUTPUT0

"best_elo_by_year.csv" <- "allGames.csv"
  ./streaming_elo.py $INPUT0  | psort -c elo > $OUTPUT0