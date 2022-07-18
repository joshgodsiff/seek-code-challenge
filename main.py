from dateutil import parser
import heapq
from datetime import timedelta

from Entry import Entry, DayEntry
from LowestN import LowestN, lowestNContiguous

halfHour = timedelta(minutes=30)

def processFile():
  total = 0
  dailyTotals = {}
  top3 = []
  mostRecent3 = LowestN(3, halfHour)
  lowest3 = LowestN(3, halfHour)

  with open("test-file.txt") as file:
    for line in file:
      (timeStr, _, num) = line.partition(" ")
      time = parser.parse(timeStr)
      entry = Entry(num=int(num), time=time)
      total = rollingTotal(total, entry)
      dailyTotals = rollingDailyTotal(dailyTotals, entry)
      top3 = topN(3, top3, entry)
      mostRecent3.push(entry)
      lowest3 = lowestNContiguous(mostRecent3, lowest3)
    
  print("Total:", total)

  print("Daily totals:")
  for k, v in dailyTotals.items():
    e = DayEntry(num=v, time=k)
    print("  ", e)
  
  print("Top 3 half hours:")
  for e in top3:
    print("  ", e)

  print("Least seen in a 1.5 hour period:", sum([e.num for e in lowest3.q]))
  for e in list(lowest3.q):
      print("  ", e)

def rollingTotal(prev: int, current: Entry) -> int:
  return prev + current.num

def rollingDailyTotal(m: dict, e: Entry) -> dict:
  date = e.time.date()
  current = m.get(date, 0)
  m[date] = current + e.num

  return m

def topN(n: int, heap: list[Entry], current: Entry) -> list[Entry]:
  if len(heap) < n:
    heapq.heappush(heap, current)
  else:
    try:
      smallest = heapq.heappop(heap)
      heapq.heappush(heap, max(smallest, current))
    except IndexError:
      # This should never happen unless n < 1, but I prefer to check known exceptions just in case.
      heapq.heappush(heap,current)

  return heap


if __name__ == "__main__":
  # print("Hello")
  processFile()
  # print("World")