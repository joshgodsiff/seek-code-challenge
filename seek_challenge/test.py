from copy import copy
from datetime import datetime, timedelta
from lib.Entry import Entry
from hypothesis import given, strategies as st
from lib.Folds.Total import Total
from lib.Folds.TopN import TopN
from lib.Folds.DailyTotal import DailyTotal
from lib.Folds.LowestN import LowestN
from itertools import groupby

max_time = datetime(2100, 12, 31) # Avoids overflow in calculations below.

@given(
  num=st.integers(),
  time1=st.datetimes(max_value=max_time),
  time2=st.datetimes(max_value=max_time)
)
def test_entries_are_contiguous(num, time1, time2):
  smaller = min(time1, time2)
  bigger = max(time1, time2) 

  e1 = Entry(num=num, time=smaller)
  e2 = Entry(num=num, time=bigger)

  delta = bigger - smaller
  
  assert e1.contiguous(e2, delta)
  assert e1.time == e2.time or not e2.contiguous(e1, delta)

@given(
  lst=st.lists(st.integers()),
  time=st.datetimes()
)
def total_fold_gives_sum(lst, time):
  f = Total()

  for num in lst:
    entry = Entry(num=num, time=time)
    f.fold(entry)

  result = f.result()

  assert result == sum(lst)

@given(
  lst=st.lists(st.integers(), min_size=10),
  time=st.datetimes(),
  n=st.integers(min_value=1, max_value=10)
)
def top_n_fold_gives_biggest_n_elements(lst, time, n):
  f = TopN(n)

  for num in lst:
    entry = Entry(num=num, time=time)
    f.fold(entry)

  result = [e.num for e in f.result()]
  result.sort()

  lstCopy = copy(lst)
  lstCopy.sort()

  assert result == lstCopy[-n:]

# We need to limit the range sufficiently that we actually get some overlap in terms
# of days when we run the tests.
dec1st2022 = datetime(2022, 12, 1)
dec31st2022 = datetime(2022, 12, 31)

@given(
  nums=st.lists(st.integers(), min_size=32),
  times=st.lists(st.datetimes(min_value=dec1st2022, max_value=dec31st2022), min_size=32),
)
def daily_total_fold_aggregates_by_day(nums, times):
  f = DailyTotal()
  entries = [Entry(num=n, time=t) for n, t in zip(nums, times)]

  for e in entries:
    f.fold(e)
  
  results = f.result()
  group = lambda e: e.time.date()
  
  sorted = copy(entries)
  sorted.sort(key=group)
  grouped = groupby(sorted, key=group)

  expected = {k: sum([e.num for e in gr]) for k, gr in grouped}

  assert expected == results

@given(
  nums=st.lists(st.integers(min_value=0), min_size=10),
  time=st.datetimes(),
  n=st.integers(min_value=2, max_value=10)
)
def sum_of_lowest_n_fold_should_be_the_sum_of_the_lowest_n_window(nums, time, n):
  delta = timedelta(minutes=30)
  f = LowestN(n=n, delta=delta)
  entries = [Entry(num=m, time=time + (i * delta)) for m, i in zip(nums, range(len(nums)))]

  for e in entries:
    f.fold(e)

  results = f.result()

  lists = [entries[i:] for i in range(n)]
  zipped = list(zip(*lists))
  sums = [ sum([e.num for e in list(tpl)]) for tpl in zipped ]

  sumResults = sum([e.num for e in results.q])

  assert min(sums) == sumResults

if __name__ == "__main__":
  test_entries_are_contiguous()
  total_fold_gives_sum()
  top_n_fold_gives_biggest_n_elements()
  daily_total_fold_aggregates_by_day()
  sum_of_lowest_n_fold_should_be_the_sum_of_the_lowest_n_window()