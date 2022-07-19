from dataclasses import dataclass
from typing import Dict

from lib.Entry import Entry

@dataclass
class FoldMany:
  folds: Dict[str, object]

  def fold(self, next: Entry):
    for f in self.folds.values():
      f.fold(next)

  def result(self):
    return {k: v.result() for k, v in self.folds.items()}