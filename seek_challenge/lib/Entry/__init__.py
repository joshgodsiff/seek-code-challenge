from dataclasses import dataclass
from datetime import datetime, timedelta, date

@dataclass(order=True, frozen=True, kw_only=True)
class Entry:
  num: int
  time: datetime

  def contiguous(self, other, delta: timedelta) -> bool:
    return self.time + delta == other.time

  def __str__(self) -> str:
    return f"{self.time.isoformat()} {self.num}"

@dataclass(kw_only=True)
class DayEntry:
  num: int
  time: date

  def __str__(self) -> str:
    return f"{self.time.isoformat()} {self.num}"