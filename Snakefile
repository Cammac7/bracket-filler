"allGames.csv" <-
  for f in alltheGames/*csv; do less $f | pawk -g '",School," not in l and len(r) > 1'; done | pawk -g 'i==0 or "PTS" not in l' | psort -c Date --str > $OUTPUT0

"best_elo_by_year.csv" <- "allGames.csv"
  ./streaming_elo.py $INPUT0  | psort -c elo > $OUTPUT0

"test_elo_file.csv" <- "allGames.csv"
  less $INPUT0 | pcsv -p 'r["yr"] = r["Date"].split("-")[0]' -c yr,Schl | (read -r h; echo $h; cat - | sort | uniq) | pawk -b 'print "year,team,elo"' -g 'i>0' -p 'write_line(r + [rand()])' > $OUTPUT0