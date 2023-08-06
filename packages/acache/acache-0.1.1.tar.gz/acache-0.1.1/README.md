# acache

![pipeline status](https://gitlab.com/sj1k/acache/badges/master/pipeline.svg)
![coverage](https://gitlab.com/sj1k/acache/badges/master/coverage.svg)


An extremely versitile and lightweight cache library. Supports custom cache strategies and function runners.

Works with async and without async.


## Installation


It's currently not on pypi yet so you need to clone this repo and then run

```
pip3 install . --user
```

from the root directory (with the setup.py file)


# Using

There are 2 main cache functions. `cache` and `acache`. `acache` is just a wrapper around `cache` with the asyncio runner.

```python
# A simple async LRU cache that holds 10 items.
@acache.cache(10, strat=acache.strategy.LRU, runner=acache.runners.as_asyncio)
# or
@acache.acache(10, strat=acache.strategy.LRU)

# An async timed cache, items time out after 10 seconds.
@acache.cache(10, strat=acache.strategy.Timed, runner=acache.runners.as_asyncio)
# or
@acache.acache(10, strat=acache.strategy.Timed)
```


## Normal cache

```python
import acache
import time

@acache.cache(100)  # Creates a cache which stores 100 items, using default strategies and runners.
def myfunc(thing):
   time.sleep(5)
   return thing

print(myfunc('Thing'))
print(myfunc('Thing'))  # This will not have any delay, using the previous value.  
```

## Async cache

```python
import acache
import time
import asyncio

@acache.acache(100)  # Creates a cache which stores 100 items, using default strategies and runners.
async def myfunc(thing):
   await asyncio.sleep(5)
   return thing

async def main():
   print(await myfunc('Thing'))
   print(await myfunc('Thing'))  # This will not have any delay, using the previous value.  
   return None

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Custom strategies


### Pre-existing decorators

You can make custom strategies based off pre-existing cache decorators.
Here is the simple lru implementation.


```python
def lru(size):                              
    return functools.lru_cache(maxsize=size)
```


### Class based strategies

The class based strategies should inherit from `acache.strategy.Base`
These classes should also inherit from one of the hash strategies.


```python
from acache.strategy import Base, hash

class Basic(hash.MD5, Base):

    def __init__(self, size):
        super().__init__()
        self.cache = OrderedDict()
        self.size = size

    def filter(self):
        if len(self.cache) > self.size:
            diff = len(self.cache) - self.size
            for (i, key) in enumerate([x for x in self.cache.keys()]):
                if i < diff:
                    del self.cache[key]
        return None
```
