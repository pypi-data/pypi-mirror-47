# Pyewacket
### Fast, fault-tolerant, drop-in replacement for the Python3 random module

Built on top of the RNG Storm Engine for stability and performance. While Storm is a high quality random engine, Pyewacket is not appropriate for cryptography of any kind. Pyewacket is meant for games, data science, A.I. and experimental programming, not security.


**Recommended Installation:** `$ pip install Pyewacket`


## Random Integers
- `Pyewacket.randbelow(n: int) -> int`
    - While randrange(a, b, c) can be handy, it's more complex than needed most of the time. Mathematically, randbelow(n) is equivalent to randrange(n) and they have nearly the same performance characteristics in Pyewacket, 10x - 12x faster than the random module's internal randbelow().
    - @param n :: Pyewacket expands the acceptable input domain to include non-positive values of n.
    - @return :: random integer in range (n, 0] or [0, n) depending on the sign of n.
    - Analytic Continuation about zero is used to achieve full input domain coverage for any function that normally can only take positive, non-zero values as input.
    - Symmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n) if n < 0 else 0` (this is how it works now).
    - The lambda is not the actual implementation, but it represents the idea of AC pretty well. AC will invert the meaning of a function for negative input. Thus turning _randbelow_ into _randabove_ for all negative values of n.

_It is possible that an asymmetric AC would be a better match to how negative numbers work as reverse list indexes in python._

Asymmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n)-1 if n < 0 else None` (this is how it could work).

_This would allow_ `some_list[randbelow(-n)]` _to range over the last n items in a list of size n or larger. The interesting part is that you wouldn't need to know the exact size of the list. Let me know if you think this is a good idea._

```python
from Pyewacket import randbelow


""" Standard """
randbelow(10)       # -> [0, 10)

""" Extras """
randbelow(0)        # -> [0, 0) => 0
randbelow(-10)      # -> (-10, 0]
```

- `Pyewacket.randint(a: int, b: int) -> int`
    - @param a, b :: both are required,
    - @return :: random integer in range [a, b] or [b, a]
    - Inclusive on both sides
    - Removed the asymmetric requirement of a < b
    - When a == b returns a

```python
from Pyewacket import randint


""" Standard """
randint(1, 10)      # -> [1, 10]

""" Extras """
randint(10, 1)      # -> [1, 10]
randint(10, 10)     # -> [10, 10] => 10
```

- `Pyewacket.randrange(start: int, stop: int = 0, step: int = 1) -> int`
    - Fault tolerant and about 20x faster than random.randrange()
    - @param start :: required
    - @param stop :: optional, default=0
    - @parma step :: optional, default=1
    - @return :: random integer in range (stop, start] or [start, stop) by |step|
    - Removed the requirements of start < stop, and step > 0
    - Always returns start for start == stop or step == 0

```python
from Pyewacket import randrange


""" Standard """
randrange(10)           # -> [0, 10) by whole numbers
randrange(1, 10)        # -> [1, 10) by whole numbers
randrange(1, 10, 2)     # -> [1, 10) by 2, odd numbers

""" Extras """
randrange(-10)          # -> [-10, 0) by 1
randrange(10, 1)        # -> [1, 10) by 1
randrange(10, 0, 2)     # -> [0, 10) by 2, even numbers
randrange(10, 10, 0)    # -> [10, 10) => 10
```

## Random Floating Point
- `Pyewacket.random() -> float`
    - random float in range [0.0, 1.0] or [0.0, 1.0) depending on rounding.
    - This is the only function that doesn't show a performance increase, as expected.
    - Roughly the same speed as random.random()
- `Pyewacket.uniform(a: float, b: float) -> float`
    - random float in [a, b] or [a, b) depending on rounding
    - 4x faster
- `Pyewacket.expovariate(lambd: float) -> float`
    - 5x faster
- `Pyewacket.gammavariate(alpha, beta) -> float`
    - 10x faster
- `Pyewacket.weibullvariate(alpha, beta) -> float`
    - 4x faster
- `Pyewacket.betavariate(alpha, beta) -> float`
    - 16x faster
- `Pyewacket.paretovariate(alpha) -> float`
    - 4x faster
- `Pyewacket.gauss(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.normalvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.lognormvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.vonmisesvariate(mu: float, kappa: float) -> float`
    - 4x faster
- `Pyewacket.triangular(low: float, high: float, mode: float = None)`
    - 10x faster

## Random Sequence Values
- `Pyewacket.choice(seq: List) -> Value`
    - An order of magnitude faster than random.choice().
    - @param seq :: any zero indexed object like a list or tuple.
    - @return :: random value from the list, can be any object type that can be put into a list.
- `Pyewacket.choices(population, weights=None, *, cum_weights=None, k=1)`
    - @param population :: data values
    - @param weights :: relative weights
    - @param cum_weights :: cumulative weights
    - @param k :: number of samples to be collected
    - Only seeing a 2x performance gain.
- `Pyewacket.cumulative_weighted_choice(table, k=1)`
    - 10x faster than choices, but radically different API and a bit less flexible.
    - Supports Cumulative Weights only. Convert relative weights to cumulative if needed: `cum_weights = tuple(itertools.accumulate(rel_weights))`
    - @param table :: two dimensional list or tuple of weighted value pairs. `[(1, "a"), (10, "b"), (100, "c")...]`
        - The table can be constructed as `tuple(zip(cum_weights, population))` weights always come first.
    - @param k :: number of samples to be collected. Returns a list of size k if k > 1, otherwise returns a single value - not a list of one.
- `Pyewacket.shuffle(array: list) -> None`
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 20 times faster than random.shuffle().
    - Implements Knuth B Shuffle Algorithm. Knuth B is twice as fast as Knuth A or Fisher-Yates for every test case. This is likely due to the combination of walking backward and rotating backward into the back side of the list. With this combination it can never modify the data it still needs to walk through. Fresh snow all the way home, aka very low probability for cache misses.
- `Pyewacket.knuth(array: list) -> None`, shuffle alternate.
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 10 times faster than random.shuffle().
    - Original Knuth Shuffle Algorithm.
    - Walks forward and rotates backward, but to the front side of the list.
- `Pyewacket.fisher_yates(array: list) -> None`, shuffle alternate.
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 10 times faster than random.shuffle().
    - Fisher-Yates Shuffle Algorithm. Used in random.shuffle().
    - Walks backward and rotates forward, into oncoming traffic.
- `Pyewacket.sample(population: List, k: int) -> list`
    - @param population :: list or tuple.
    - @param k :: number of unique samples to get.
    - @return :: size k list of unique random samples.
    - Performance gains range (5x to 20x) depending on len(population) and the ratio of k to len(population). Higher performance gains are seen when k ~= pop size.

## Seeding
- `set_seed(seed: int=0) -> None`
    - Hardware seeding is enabled by default. This is used to turn on/off software seeding and set or reset the engine seed. This affects all random functions in the module.
    - @param seed :: any non-zero positive integer less than 2**63 enables software seeding.
    - Calling `set_seed()` or `set_seed(0)` will turn off software seeding and re-enable hardware seeding.
    - While you can toggle software seeding on and off and re-seed the engine at will without error, this function is **not intended or optimized to be used in a loop**. General rule: seed once, or better yet, not at all. Typically, software seeding is for research and development, hardware seeding is used for modeling.

## Testing Suite
- `distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - For the statistical analysis of a non-deterministic numeric output function.
    - @param func :: function, method or lambda to analyze. `func(*args, **kwargs)`
    - @optional_kw num_cycles=10000 :: Total number of samples to use for analysis.
    - @optional_kw post_processor=None :: Used to scale a large set of data into a smaller set of groupings for better visualization of the data, esp. useful for distributions of floats. For many functions in quick_test(), math.floor() is used, for others round() is more appropriate. For more complex post processing - lambdas work nicely. Post processing only affects the distribution, the statistics and performance results are unaffected.
- `quick_test() -> None`
    - Runs a battery of tests for each random distribution function in the module.


## Development Log
##### Pyewacket 1.2.1
- Test Update

##### Pyewacket 1.2.0
- Storm Update

##### Pyewacket 1.1.2
- Low level clean up

##### Pyewacket 1.1.1
- Docs Update

##### Pyewacket 1.1.0
- Storm Engine Update

##### Pyewacket 1.0.3
- minor typos

##### Pyewacket 1.0.2
- added choices alternative `cumulative_weighted_choice`

##### Pyewacket 1.0.1
- minor typos

##### Pyewacket 1.0.0
- Storm 2 Rebuild.

##### Pyewacket 0.1.22
- Small bug fix.

##### Pyewacket 0.1.21
- Public Release

##### Pyewacket 0.0.2b1
- Added software seeding.

##### Pyewacket v0.0.1b8
- Fixed a small bug in the tests.

##### Pyewacket v0.0.1b7
- Engine Fine Tuning
- Fixed some typos.

##### Pyewacket v0.0.1b6
- Rearranged tests to be more consistent and match the documentation.

##### Pyewacket v0.0.1b5
- Documentation Upgrade
- Minor Performance Tweaks

##### Pyewacket v0.0.1b4
- Public Beta

##### Pyewacket v0.0.1b3
- quick_test()
- Extended Functionality
    - sample()
    - expovariate()
    - gammavariate()
    - weibullvariate()
    - betavariate()
    - paretovariate()
    - gauss()
    - normalvariate()
    - lognormvariate()
    - vonmisesvariate()
    - triangular()

##### Pyewacket v0.0.1b2
- Basic Functionality
    - random()
    - uniform()
    - randbelow()
    - randint()
    - randrange()
    - choice()
    - choices()
    - shuffle()

##### Pyewacket v0.0.1b1
- Initial Design & Planning


## Pywacket Distribution and Performance Test Suite
```
Pyewacket Distribution & Performance Test Suite

Software Seed Test Passed
Hardware Seed Test Passed

Output Analysis: Random._randbelow(10)
Typical Timing: 657 ± 15 ns
Raw Samples: 4, 8, 8, 3, 7
Statistics of 1000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.462
 Std Deviation: 2.9365250176320954
Distribution of 10000 Samples:
 0: 9.86%
 1: 9.82%
 2: 10.44%
 3: 9.99%
 4: 9.95%
 5: 9.77%
 6: 10.23%
 7: 9.92%
 8: 10.14%
 9: 9.88%

Output Analysis: randbelow(10)
Typical Timing: 63 ± 4 ns
Raw Samples: 8, 7, 0, 0, 4
Statistics of 1000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.485
 Std Deviation: 2.9199830994889853
Distribution of 10000 Samples:
 0: 10.29%
 1: 10.07%
 2: 9.74%
 3: 9.71%
 4: 10.46%
 5: 10.09%
 6: 9.81%
 7: 10.14%
 8: 9.8%
 9: 9.89%

Output Analysis: Random.randint(1, 10)
Typical Timing: 1157 ± 12 ns
Raw Samples: 1, 9, 1, 2, 6
Statistics of 1000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.468
 Std Deviation: 2.8451838378338703
Distribution of 10000 Samples:
 1: 10.24%
 2: 9.97%
 3: 10.06%
 4: 9.91%
 5: 9.35%
 6: 9.93%
 7: 10.55%
 8: 9.87%
 9: 9.83%
 10: 10.29%

Output Analysis: randint(1, 10)
Typical Timing: 63 ± 7 ns
Raw Samples: 7, 9, 6, 1, 10
Statistics of 1000 Samples:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.534
 Std Deviation: 2.9300903449261475
Distribution of 10000 Samples:
 1: 10.45%
 2: 9.95%
 3: 9.93%
 4: 10.14%
 5: 10.23%
 6: 10.01%
 7: 9.19%
 8: 10.01%
 9: 9.97%
 10: 10.12%

Output Analysis: Random.randrange(0, 10, 2)
Typical Timing: 1313 ± 13 ns
Raw Samples: 2, 0, 0, 8, 4
Statistics of 1000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.048
 Std Deviation: 2.823768699746789
Distribution of 10000 Samples:
 0: 19.93%
 2: 20.18%
 4: 19.91%
 6: 20.48%
 8: 19.5%

Output Analysis: randrange(0, 10, 2)
Typical Timing: 63 ± 7 ns
Raw Samples: 6, 0, 6, 0, 2
Statistics of 1000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 3.958
 Std Deviation: 2.8344788357421673
Distribution of 10000 Samples:
 0: 20.0%
 2: 19.87%
 4: 19.7%
 6: 20.14%
 8: 20.29%

Output Analysis: Random.random()
Typical Timing: 32 ± 8 ns
Raw Samples: 0.9820321473707115, 0.5543823569855546, 0.4495390505417324, 0.03916859833080899, 0.2835945767211503
Statistics of 1000 Samples:
 Minimum: 0.00011040498336067905
 Median: (0.5250286968420679, 0.5260931110085462)
 Maximum: 0.9984837213600186
 Mean: 0.5122062277754271
 Std Deviation: 0.28814583319382875
Post-processor Distribution of 10000 Samples using round method:
 0: 49.66%
 1: 50.34%

Output Analysis: random()
Typical Timing: 32 ± 8 ns
Raw Samples: 0.5068364050694357, 0.8538140397397256, 0.6421661805817236, 0.6171263692635488, 0.11820214979765328
Statistics of 1000 Samples:
 Minimum: 0.000805828911190407
 Median: (0.5328927698808247, 0.5337509801514929)
 Maximum: 0.999901888827233
 Mean: 0.5205139821027316
 Std Deviation: 0.29231358532851914
Post-processor Distribution of 10000 Samples using round method:
 0: 49.48%
 1: 50.52%

Output Analysis: Random.uniform(0.0, 10.0)
Typical Timing: 219 ± 8 ns
Raw Samples: 0.8628518634742288, 6.138689269826711, 4.2584912774727846, 3.4555155510276068, 1.5201168240798757
Statistics of 1000 Samples:
 Minimum: 0.00985666350619474
 Median: (5.03106733828775, 5.0444746780234535)
 Maximum: 9.998225472567396
 Mean: 4.962245553818666
 Std Deviation: 2.8235248876019807
Post-processor Distribution of 10000 Samples using floor method:
 0: 10.23%
 1: 10.02%
 2: 9.97%
 3: 10.1%
 4: 9.22%
 5: 10.24%
 6: 9.8%
 7: 10.03%
 8: 10.28%
 9: 10.11%

Output Analysis: uniform(0.0, 10.0)
Typical Timing: 32 ± 8 ns
Raw Samples: 3.1666368135154688, 4.644234723679322, 2.937324769758903, 0.17223247782913376, 9.041133900474676
Statistics of 1000 Samples:
 Minimum: 0.029792594987942577
 Median: (4.997053922258964, 5.028486274278575)
 Maximum: 9.99634114426451
 Mean: 5.029584531147504
 Std Deviation: 2.9341900797868488
Post-processor Distribution of 10000 Samples using floor method:
 0: 9.91%
 1: 10.08%
 2: 10.06%
 3: 9.94%
 4: 10.32%
 5: 10.34%
 6: 9.63%
 7: 9.99%
 8: 9.93%
 9: 9.8%

Output Analysis: Random.expovariate(1.0)
Typical Timing: 313 ± 7 ns
Raw Samples: 0.056557528407497275, 0.36324620534017926, 0.7345357775691527, 0.19198192089737248, 1.4370570366820605
Statistics of 1000 Samples:
 Minimum: 0.0002521313914756107
 Median: (0.6563220879101878, 0.6596713008063708)
 Maximum: 7.866883814422792
 Mean: 0.9651441490829515
 Std Deviation: 0.9738140430950728
Post-processor Distribution of 10000 Samples using floor method:
 0: 62.68%
 1: 23.4%
 2: 8.84%
 3: 3.4%
 4: 1.04%
 5: 0.41%
 6: 0.13%
 7: 0.07%
 8: 0.01%
 10: 0.01%
 12: 0.01%

Output Analysis: expovariate(1.0)
Typical Timing: 63 ± 3 ns
Raw Samples: 1.3506872243020749, 1.6734190825975932, 0.8373569024485672, 2.545197360152299, 0.21894956831480283
Statistics of 1000 Samples:
 Minimum: 0.00011745104782263943
 Median: (0.6609174533357693, 0.6657767670621884)
 Maximum: 7.667452425011901
 Mean: 0.9731907945653412
 Std Deviation: 0.996350775421818
Post-processor Distribution of 10000 Samples using floor method:
 0: 63.14%
 1: 23.26%
 2: 8.72%
 3: 2.99%
 4: 1.24%
 5: 0.46%
 6: 0.11%
 7: 0.07%
 8: 0.01%

Output Analysis: Random.gammavariate(2.0, 1.0)
Typical Timing: 1188 ± 29 ns
Raw Samples: 2.340587817897044, 1.6248583882353496, 2.247560083213798, 0.2851670912542922, 0.21413918958632738
Statistics of 1000 Samples:
 Minimum: 0.03417685268895996
 Median: (1.703006291269952, 1.7079731776621938)
 Maximum: 10.360666079726817
 Mean: 2.010165518053083
 Std Deviation: 1.3975686426923988
Post-processor Distribution of 10000 Samples using round method:
 0: 8.95%
 1: 34.8%
 2: 27.09%
 3: 15.41%
 4: 7.6%
 5: 3.39%
 6: 1.62%
 7: 0.58%
 8: 0.31%
 9: 0.2%
 10: 0.05%

Output Analysis: gammavariate(2.0, 1.0)
Typical Timing: 125 ± 5 ns
Raw Samples: 1.0669690251572312, 1.6013000145817387, 2.8322004548468573, 2.4387473798555734, 1.0884681555076179
Statistics of 1000 Samples:
 Minimum: 0.0260623927298701
 Median: (1.6200534566409555, 1.6209087848596224)
 Maximum: 11.090311256924222
 Mean: 1.9817376294116529
 Std Deviation: 1.4394365996068412
Post-processor Distribution of 10000 Samples using round method:
 0: 9.21%
 1: 34.65%
 2: 27.5%
 3: 14.85%
 4: 7.42%
 5: 3.66%
 6: 1.54%
 7: 0.67%
 8: 0.25%
 9: 0.2%
 10: 0.04%
 11: 0.01%

Output Analysis: Random.weibullvariate(1.0, 1.0)
Typical Timing: 407 ± 7 ns
Raw Samples: 0.20145430908376338, 1.085309559578678, 0.04790207819236292, 1.0316396199485198, 0.999426324458673
Statistics of 1000 Samples:
 Minimum: 0.001676611622361662
 Median: (0.6975073774184228, 0.6985159726059269)
 Maximum: 8.245510774103344
 Mean: 1.017227739236608
 Std Deviation: 0.9869458651727325
Post-processor Distribution of 10000 Samples using floor method:
 0: 63.26%
 1: 23.06%
 2: 8.56%
 3: 3.17%
 4: 1.28%
 5: 0.38%
 6: 0.19%
 7: 0.07%
 8: 0.01%
 9: 0.02%

Output Analysis: weibullvariate(1.0, 1.0)
Typical Timing: 94 ± 6 ns
Raw Samples: 0.24678137142900597, 0.7697339948550035, 0.35443325983110147, 0.6942494367943725, 0.022371215667053385
Statistics of 1000 Samples:
 Minimum: 0.0021719940607884685
 Median: (0.6605026437718177, 0.6634776829521866)
 Maximum: 6.902006238554751
 Mean: 0.9830918255635315
 Std Deviation: 0.9877516989855255
Post-processor Distribution of 10000 Samples using floor method:
 0: 63.45%
 1: 23.54%
 2: 8.09%
 3: 3.12%
 4: 1.17%
 5: 0.43%
 6: 0.14%
 7: 0.01%
 8: 0.03%
 9: 0.01%
 12: 0.01%

Output Analysis: Random.betavariate(3.0, 3.0)
Typical Timing: 2563 ± 43 ns
Raw Samples: 0.09444426257644345, 0.3455836050211544, 0.4355230053627496, 0.2412592575909043, 0.6193976898817825
Statistics of 1000 Samples:
 Minimum: 0.041433903589522876
 Median: (0.4941869832024153, 0.4953364196025999)
 Maximum: 0.952654590153644
 Mean: 0.4988999659471316
 Std Deviation: 0.18671770279262984
Post-processor Distribution of 10000 Samples using round method:
 0: 49.87%
 1: 50.13%

Output Analysis: betavariate(3.0, 3.0)
Typical Timing: 188 ± 8 ns
Raw Samples: 0.5297653849363014, 0.35408674245560373, 0.3392321800171851, 0.5691981398485935, 0.69959612846755
Statistics of 1000 Samples:
 Minimum: 0.010113530056475398
 Median: (0.5028113612075514, 0.503893023117671)
 Maximum: 0.9585235973663784
 Mean: 0.4977400114634504
 Std Deviation: 0.19480850043786213
Post-processor Distribution of 10000 Samples using round method:
 0: 50.6%
 1: 49.4%

Output Analysis: Random.paretovariate(4.0)
Typical Timing: 282 ± 8 ns
Raw Samples: 1.0262712497455777, 1.089842337423379, 1.0495594917981133, 1.5215189789556915, 1.11805667773468
Statistics of 1000 Samples:
 Minimum: 1.0001741539482463
 Median: (1.2078073433758192, 1.2078620127477961)
 Maximum: 4.651671290633672
 Mean: 1.3578880570794276
 Std Deviation: 0.4681722908998761
Post-processor Distribution of 10000 Samples using floor method:
 1: 93.97%
 2: 4.58%
 3: 0.91%
 4: 0.25%
 5: 0.09%
 6: 0.1%
 7: 0.05%
 8: 0.01%
 9: 0.03%
 13: 0.01%

Output Analysis: paretovariate(4.0)
Typical Timing: 94 ± 1 ns
Raw Samples: 1.2435992615042166, 1.0814359960342859, 1.2849278890273375, 1.0289791358714846, 1.8397208727588947
Statistics of 1000 Samples:
 Minimum: 1.0000529431723724
 Median: (1.1922140446699776, 1.1932692120905846)
 Maximum: 4.296850843928264
 Mean: 1.3381115935937329
 Std Deviation: 0.43427321313779116
Post-processor Distribution of 10000 Samples using floor method:
 1: 94.05%
 2: 4.77%
 3: 0.82%
 4: 0.19%
 5: 0.1%
 6: 0.05%
 8: 0.02%

Output Analysis: Random.gauss(1.0, 1.0)
Typical Timing: 563 ± 7 ns
Raw Samples: 2.6545794488819485, 1.0671125108880315, 1.4688505725349397, 0.2563823800256526, -0.9708937967690416
Statistics of 1000 Samples:
 Minimum: -2.1551495844228925
 Median: (0.985167796961334, 0.9852519948397755)
 Maximum: 4.542596420608218
 Mean: 0.9917048994204836
 Std Deviation: 1.004616994818099
Post-processor Distribution of 10000 Samples using round method:
 -3: 0.02%
 -2: 0.58%
 -1: 6.25%
 0: 25.07%
 1: 38.08%
 2: 23.45%
 3: 6.02%
 4: 0.49%
 5: 0.04%

Output Analysis: gauss(1.0, 1.0)
Typical Timing: 94 ± 1 ns
Raw Samples: 1.258683622306338, -0.35676929765995663, 0.698265461743795, 2.5119831080878354, 0.754703365786846
Statistics of 1000 Samples:
 Minimum: -2.4942597311105428
 Median: (0.9482149064775212, 0.9504286764347505)
 Maximum: 4.32393785258698
 Mean: 0.9673925356676288
 Std Deviation: 1.0242246782285263
Post-processor Distribution of 10000 Samples using round method:
 -3: 0.02%
 -2: 0.72%
 -1: 6.38%
 0: 24.14%
 1: 38.05%
 2: 24.19%
 3: 5.92%
 4: 0.55%
 5: 0.03%

Output Analysis: Random.normalvariate(0.0, 2.8)
Typical Timing: 625 ± 22 ns
Raw Samples: 0.7843496484997124, 0.5331762609609316, -7.797331562464318, -2.293483487064677, -1.9791468354919348
Statistics of 1000 Samples:
 Minimum: -8.487249100145998
 Median: (0.06436777608805976, 0.06713823497817509)
 Maximum: 8.948262914885438
 Mean: -0.005611424942135695
 Std Deviation: 2.751649008048358
Post-processor Distribution of 10000 Samples using round method:
 -9: 0.12%
 -8: 0.28%
 -7: 0.66%
 -6: 1.56%
 -5: 2.99%
 -4: 5.35%
 -3: 7.76%
 -2: 11.42%
 -1: 13.05%
 0: 13.97%
 1: 12.85%
 2: 10.78%
 3: 8.5%
 4: 5.0%
 5: 3.19%
 6: 1.46%
 7: 0.68%
 8: 0.21%
 9: 0.14%
 10: 0.02%
 11: 0.01%

Output Analysis: normalvariate(0.0, 2.8)
Typical Timing: 94 ± 3 ns
Raw Samples: -0.32096828727089616, -2.303323360010777, 2.355923078597011, 2.1964845972033418, 2.928940527172713
Statistics of 1000 Samples:
 Minimum: -8.789294064275794
 Median: (0.12026404506150982, 0.12570387788767645)
 Maximum: 8.716625841513174
 Mean: 0.08307095662128675
 Std Deviation: 2.815274567898717
Post-processor Distribution of 10000 Samples using round method:
 -9: 0.06%
 -8: 0.2%
 -7: 0.55%
 -6: 1.35%
 -5: 3.17%
 -4: 5.19%
 -3: 8.09%
 -2: 11.51%
 -1: 13.43%
 0: 13.9%
 1: 13.19%
 2: 10.72%
 3: 7.83%
 4: 5.38%
 5: 3.13%
 6: 1.43%
 7: 0.49%
 8: 0.27%
 9: 0.1%
 11: 0.01%

Output Analysis: Random.lognormvariate(0.0, 0.5)
Typical Timing: 844 ± 21 ns
Raw Samples: 1.34353223469613, 2.449504801889568, 1.280766538928976, 0.9616035209352419, 1.0421782786101264
Statistics of 1000 Samples:
 Minimum: 0.20091738788412655
 Median: (1.0135430460491468, 1.0146137799243655)
 Maximum: 3.744376687872472
 Mean: 1.1244634658832013
 Std Deviation: 0.5567831697542911
Post-processor Distribution of 10000 Samples using round method:
 0: 8.32%
 1: 70.6%
 2: 17.6%
 3: 2.93%
 4: 0.43%
 5: 0.1%
 8: 0.02%

Output Analysis: lognormvariate(0.0, 0.5)
Typical Timing: 94 ± 7 ns
Raw Samples: 0.9710796768689338, 0.8135141657537172, 2.2914587984250003, 1.342905248311371, 0.6965274570980418
Statistics of 1000 Samples:
 Minimum: 0.22507612339474936
 Median: (1.0094383560534876, 1.0109243838455884)
 Maximum: 4.701842232093691
 Mean: 1.1546308514508614
 Std Deviation: 0.6331125063957624
Post-processor Distribution of 10000 Samples using round method:
 0: 8.73%
 1: 70.44%
 2: 17.61%
 3: 2.63%
 4: 0.44%
 5: 0.13%
 6: 0.01%
 7: 0.01%

Output Analysis: Random.vonmisesvariate(0, 0)
Typical Timing: 250 ± 8 ns
Raw Samples: 4.458210462595683, 2.088161528680619, 5.037335380651193, 4.937321225106458, 1.5939651679353626
Statistics of 1000 Samples:
 Minimum: 0.00639467711893127
 Median: (3.156588795661799, 3.1735423026321015)
 Maximum: 6.282237772569084
 Mean: 3.184266110375619
 Std Deviation: 1.8230424308897282
Post-processor Distribution of 10000 Samples using floor method:
 0: 15.7%
 1: 16.27%
 2: 15.61%
 3: 15.95%
 4: 16.14%
 5: 15.87%
 6: 4.46%

Output Analysis: vonmisesvariate(0, 0)
Typical Timing: 63 ± 8 ns
Raw Samples: 6.103558111844794, 2.1103126074579492, 1.8313433322729673, 6.193119192280361, 2.7086842427939324
Statistics of 1000 Samples:
 Minimum: 0.003639614709736534
 Median: (3.0790612093487804, 3.0828431030034027)
 Maximum: 6.276407728358619
 Mean: 3.173337758808393
 Std Deviation: 1.8387266539309477
Post-processor Distribution of 10000 Samples using floor method:
 0: 15.52%
 1: 15.72%
 2: 16.24%
 3: 16.26%
 4: 15.69%
 5: 16.27%
 6: 4.3%

Output Analysis: Random.triangular(0.0, 10.0, 0.0)
Typical Timing: 469 ± 8 ns
Raw Samples: 3.358212379140129, 1.1838949078714496, 3.19838479227845, 0.9582389389114763, 5.379690910569051
Statistics of 1000 Samples:
 Minimum: 0.0018785904451625868
 Median: (3.064197036473896, 3.084826630658367)
 Maximum: 9.758348706018223
 Mean: 3.401132210019609
 Std Deviation: 2.33338387336625
Post-processor Distribution of 10000 Samples using floor method:
 0: 19.32%
 1: 17.27%
 2: 14.41%
 3: 12.66%
 4: 11.36%
 5: 9.25%
 6: 7.21%
 7: 4.92%
 8: 2.75%
 9: 0.85%

Output Analysis: triangular(0.0, 10.0, 0.0)
Typical Timing: 32 ± 7 ns
Raw Samples: 4.286491787985068, 3.613554887851116, 3.7998825926863375, 7.464736734808892, 1.7163070249805013
Statistics of 1000 Samples:
 Minimum: 0.0029903081211235527
 Median: (2.878405888786888, 2.8843127934511283)
 Maximum: 9.929058811819282
 Mean: 3.409801316153365
 Std Deviation: 2.4684680148817755
Post-processor Distribution of 10000 Samples using floor method:
 0: 19.71%
 1: 17.35%
 2: 14.86%
 3: 12.1%
 4: 10.94%
 5: 8.99%
 6: 7.17%
 7: 4.7%
 8: 3.06%
 9: 1.12%

Output Analysis: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 750 ± 13 ns
Raw Samples: 5, 4, 3, 2, 3
Statistics of 1000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.591
 Std Deviation: 2.8258989197607023
Distribution of 10000 Samples:
 0: 9.1%
 1: 10.13%
 2: 9.61%
 3: 10.62%
 4: 10.19%
 5: 10.02%
 6: 10.35%
 7: 10.08%
 8: 10.0%
 9: 9.9%

Output Analysis: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 63 ± 5 ns
Raw Samples: 1, 2, 2, 6, 8
Statistics of 1000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.462
 Std Deviation: 2.8306480827839704
Distribution of 10000 Samples:
 0: 10.43%
 1: 9.56%
 2: 10.11%
 3: 10.34%
 4: 9.94%
 5: 9.59%
 6: 10.2%
 7: 10.37%
 8: 9.62%
 9: 9.84%

Output Analysis: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Typical Timing: 2344 ± 10 ns
Raw Samples: [0], [4], [5], [1], [7]
Statistics of 1000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.189
 Std Deviation: 2.534897375576515
Distribution of 10000 Samples:
 0: 17.95%
 1: 16.78%
 2: 14.18%
 3: 13.13%
 4: 10.76%
 5: 8.79%
 6: 7.21%
 7: 5.34%
 8: 3.9%
 9: 1.96%

Output Analysis: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Typical Timing: 1094 ± 7 ns
Raw Samples: [3], [3], [2], [5], [1]
Statistics of 1000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.014
 Std Deviation: 2.429754659982713
Distribution of 10000 Samples:
 0: 17.84%
 1: 16.11%
 2: 14.91%
 3: 12.98%
 4: 11.32%
 5: 9.31%
 6: 7.13%
 7: 4.95%
 8: 3.69%
 9: 1.76%

Output Analysis: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Typical Timing: 1719 ± 8 ns
Raw Samples: [2], [4], [5], [5], [0]
Statistics of 1000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.987
 Std Deviation: 2.3930226822070777
Distribution of 10000 Samples:
 0: 17.92%
 1: 17.07%
 2: 14.02%
 3: 12.77%
 4: 11.43%
 5: 9.01%
 6: 7.55%
 7: 5.08%
 8: 3.27%
 9: 1.88%

Output Analysis: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Typical Timing: 688 ± 7 ns
Raw Samples: [3], [7], [3], [0], [7]
Statistics of 1000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.204
 Std Deviation: 2.4520188409546115
Distribution of 10000 Samples:
 0: 18.14%
 1: 16.54%
 2: 14.81%
 3: 12.59%
 4: 10.97%
 5: 9.26%
 6: 6.79%
 7: 5.53%
 8: 3.66%
 9: 1.71%

Output Analysis: cumulative_weighted_choice(((10, 0), (19, 1), (27, 2), (34, 3), (40, 4), (45, 5), (49, 6), (52, 7), (54, 8), (55, 9)), k=1)
Typical Timing: 157 ± 7 ns
Raw Samples: 4, 3, 5, 0, 0
Statistics of 1000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.15
 Std Deviation: 2.497947105072431
Distribution of 10000 Samples:
 0: 18.26%
 1: 15.55%
 2: 14.65%
 3: 13.01%
 4: 11.36%
 5: 9.04%
 6: 7.47%
 7: 5.22%
 8: 3.66%
 9: 1.78%

Timer only: _random.shuffle(some_list) of size 10:
Typical Timing: 6782 ± 40 ns

Timer only: shuffle(some_list) of size 10:
Typical Timing: 407 ± 7 ns

Timer only: knuth(some_list) of size 10:
Typical Timing: 875 ± 7 ns

Timer only: fisher_yates(some_list) of size 10:
Typical Timing: 969 ± 3 ns

Output Analysis: Random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Typical Timing: 4000 ± 26 ns
Raw Samples: [0, 2, 8], [7, 5, 8], [7, 2, 5], [5, 0, 1], [1, 3, 9]
Statistics of 1000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.541
 Std Deviation: 2.844012554017195
Distribution of 10000 Samples:
 0: 9.88%
 1: 9.77%
 2: 10.09%
 3: 10.05%
 4: 10.02%
 5: 9.69%
 6: 10.41%
 7: 10.2%
 8: 9.93%
 9: 9.96%

Output Analysis: sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Typical Timing: 750 ± 7 ns
Raw Samples: [4, 6, 0], [6, 5, 2], [4, 9, 0], [6, 1, 0], [1, 6, 7]
Statistics of 1000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.586
 Std Deviation: 2.9125739625092932
Distribution of 10000 Samples:
 0: 10.3%
 1: 10.01%
 2: 9.79%
 3: 9.7%
 4: 9.45%
 5: 10.49%
 6: 10.01%
 7: 10.22%
 8: 9.94%
 9: 10.09%


Total Test Time: 1.845 sec

```
