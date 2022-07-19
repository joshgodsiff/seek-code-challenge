from dataclasses import dataclass, field
from datetime import date
from typing import Dict

from lib.Entry import Entry

@dataclass
class DailyTotal:
  totals: Dict[date, int] = field(default_factory=dict)

  def fold(self, next: Entry):
    date = next.time.date()
    current = self.totals.get(date, 0)
    self.totals[date] = current + next.num

  def result(self):
    return self.totals
