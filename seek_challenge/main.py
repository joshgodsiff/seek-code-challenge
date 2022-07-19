from dateutil import parser
from datetime import timedelta

from lib.Entry import Entry, DayEntry
from lib.Folds.DailyTotal import DailyTotal
from lib.Folds.FoldMany import FoldMany
from lib.Folds.LowestN import LowestN
from lib.Folds.TopN import TopN
from lib.Folds.Total import Total

def processFile():
  halfHour = timedelta(minutes=30)

  total = "total"
  dailyTotal = "dailyTotal"
  top3 = "top3"
  lowest3 = "lowest3"

  folds = FoldMany({
    total: Total(),
    dailyTotal: DailyTotal(),
    top3: TopN(3),
    lowest3: LowestN(3, halfHour)
  })

  with open("test-file.txt") as file:
    for line in file:
      (timeStr, _, num) = line.partition(" ")
      time = parser.parse(timeStr)
      entry = Entry(num=int(num), time=time)
      folds.fold(entry)

  results = folds.result()
    
  print("Total:", results[total])

  print("Daily totals:")
  for k, v in results[dailyTotal].items():
    e = DayEntry(num=v, time=k)
    print("  ", e)
  
  print("Top 3 half hours:")
  for e in results[top3]:
    print("  ", e)

  print("Least seen in a 1.5 hour period:", sum([e.num for e in results[lowest3].q]))
  for e in list(results[lowest3].q):
      print("  ", e)

if __name__ == "__main__":
  processFile()