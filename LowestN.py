from collections import deque, Counter
from Entry import Entry
from copy import deepcopy
from datetime import timedelta

class BoolCounter:
  def __init__(self) -> None:
    self.counter = Counter({True: 0, False: 0})

  def push(self, b: bool) -> None:
    updateC = {True: 0, False: 0}
    updateC[b] += 1
    self.counter.update(updateC)

  def pop(self, b: bool) -> None:
    updateC = {True: 0, False: 0}
    updateC[b] += 1
    self.counter.subtract(updateC)

  def __getitem__(self, i):
    return self.counter[i]

class LowestN:
  def __init__(self, n: int, delta: timedelta) -> None:
    self.q: deque[Entry] = deque([], n)
    self.sum = 0
    self.delta = delta
    self.contiguousCounter = BoolCounter()

  def pop(self) -> Entry:
    p = deque.popleft(self.q)
    self.sum = self.sum - p.num

    if len(self.q) >= 1:
      b = p.contiguous(self.q[0], self.delta)
      self.contiguousCounter.pop(b)

    return p

  def push(self, e: Entry) -> None:
    if len(self.q) == self.q.maxlen:
      self.pop()

    r = deque.append(self.q, e)
    self.sum += e.num

    l = len(self.q)
    if l >= 2:
      b = self.q[l-2].contiguous(self.q[l-1], self.delta)
      self.contiguousCounter.push(b)

  def isFull(self):
    return len(self.q) == self.q.maxlen

  def isContiguous(self) -> bool:
    return (
      self.isFull() and
      self.contiguousCounter[True] > 0 and 
      self.contiguousCounter[False] == 0
    )

def lowestNContiguous(mostRecent: LowestN, lowest3: LowestN) -> deque[Entry]:
  if mostRecent.isContiguous() and lowest3.isContiguous():
      if mostRecent.sum < lowest3.sum:
        return deepcopy(mostRecent)
      else:
        return lowest3
  elif mostRecent.isContiguous():
      return deepcopy(mostRecent)
  else:
    return lowest3