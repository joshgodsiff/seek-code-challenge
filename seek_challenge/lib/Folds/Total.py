from dataclasses import dataclass
from tkinter import Entry

from lib.Entry import Entry

@dataclass
class Total:
  total: int = 0

  def fold(self, next: Entry):
    self.total += next.num

  def result(self):
    return self.total
