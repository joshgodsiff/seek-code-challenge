# Running

You'll need to do `pipenv install` (or your preferred equivalent).

To run the main program, run `python3 seek_challenge/main.py test-file.txt`.

To run tests, run `python3 seek_challenge/test.py` - no output means tests passed.

# Explanation

I tried to do this in such a way that the solution uses constant space (i.e. space usage is not proportional to the size of the input). In my experience, having to handle the case where you don't know the size of the input file (and the input file could be large enough it doesn't fit in memory) is typically the hardest version of these sorts of problems.

This doesn't _quite_ get there - aggregating the daily totals means we do accumulate some memory that's proportional to the input, but in practice you can usually work around that either with a local DB like RocksDB, or in a worst-case by shunting intermediate results off-machine to somewhere with unbounded storage like S3.

# Alternatives
It occurred to me about half way through building this that possibly a better way to solve this problem - and certainly a better way to solve it if you don't care about space usage - is to load the data set into something like SQLite and just run queries against the DB. All the questions the assignment asks for answers to are ones that SQL engines are very good at answering.

It's also very possible that there are some good Python libraries out there that are well suited to these problems - Pandas or Spark or something. But I haven't written Python seriously since like... 2017, and never for this style of data processing, so I'm not really familiar with them.