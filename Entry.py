from datetime import datetime, timedelta

class Entry:
  def __init__(self, time: datetime, num: int) -> None:
    self.time = time
    self.num = num

  def contiguous(self, other, delta: timedelta):
    return self.time + delta == other.time

  def __eq__(self, other) -> bool:
    return self.num == other.num and self.time == other.time
	
  def __ne__(self, other) -> bool:
    return self.num != other.num and self.time != other.time
	
  def __lt__(self, other) -> bool:
    return self.num < other.num and self.time < other.time
	
  def __le__(self, other) -> bool:
    return self.num <= other.num and self.time <= other.time
	
  def __gt__(self, other) -> bool:
    return self.num > other.num and self.time > other.time
	
  def __ge__(self, other) -> bool:
    return self.num >= other.num and self.time < other.time

  def __str__(self) -> str:
    return f"{self.time.isoformat()} {self.num}"
