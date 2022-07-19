from collections import deque, Counter
from dataclasses import dataclass, field
from lib.Entry import Entry
from copy import deepcopy
from datetime import timedelta

class BoolCounter:
  def __init__(self) -> None:
    self.counter: Counter = Counter({True: 0, False: 0})

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

class LowestNCore:
  def __init__(self, n: int, delta: timedelta) -> None:
    self.n: int = n
    # This does not, and is not designed to work for n=1 or n=0
    # It could easily be special-cased for n=1, but that case is degenerate
    # And probably better handled elsewhere.
    assert n >= 2
    self.delta: timedelta = delta
    self.q: deque[Entry] = deque([], n)
    self.sum: int = 0
    self.contiguousCounter: BoolCounter = BoolCounter()

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

class LowestN:
  def __init__(self, n: int, delta: timedelta) -> None:
    self.mostRecent: LowestNCore = LowestNCore(n, delta)
    self.lowestN: LowestNCore = LowestNCore(n, delta)

  def fold(self, next: Entry):
    self.mostRecent.push(next)
    self.lowestN = self.lowestNContiguous()

  def result(self):
    return self.lowestN

  def lowestNContiguous(self) -> deque[Entry]:
    if self.mostRecent.isContiguous() and self.lowestN.isContiguous():
        if self.mostRecent.sum < self.lowestN.sum:
          return deepcopy(self.mostRecent)
        else:
          return self.lowestN
    elif self.mostRecent.isContiguous():
        return deepcopy(self.mostRecent)
    else:
      return self.lowestN