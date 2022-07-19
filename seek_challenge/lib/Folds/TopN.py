from dataclasses import dataclass, field

import heapq
from lib.Entry import Entry

@dataclass
class TopN:
  n: int
  heap: list[Entry] = field(default_factory=list)

  def fold(self, next: Entry):
    if len(self.heap) < self.n:
      heapq.heappush(self.heap, next)
    else:
      try:
        smallest = heapq.heappop(self.heap)
        heapq.heappush(self.heap, max(smallest, next))
      except IndexError:
        # This should never happen unless n < 1, but I prefer to check known exceptions just in case.
        heapq.heappush(self.heap, next)

  def result(self):
    return self.heap
