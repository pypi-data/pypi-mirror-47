#!python3
#distutils: language = c++
import itertools as _itertools


__all__ = (
    "random", "uniform", "randbelow", "randint", "choice", "sample",
    "randrange", "shuffle", "normalvariate", "lognormvariate",
    "expovariate", "vonmisesvariate", "gammavariate", "triangular",
    "gauss", "betavariate", "paretovariate", "weibullvariate",
    "choices", "cumulative_weighted_choice", "distribution_timer", "timer",
    "knuth", "fisher_yates", "set_seed", "quick_test"
)


cdef extern from "Pyewacket.hpp":
    void      _set_seed            "Pyewacket::storm.set_seed"(unsigned long long)
    double    _random              "Pyewacket::generate_canonical"()
    long long _randbelow           "Pyewacket::random_below"(long long)
    long long _randint             "Pyewacket::random_int"(long long, long long)
    long long _randrange           "Pyewacket::random_range"(long long, long long, long long)
    double    _uniform             "Pyewacket::random_float"(double, double)
    double    _expovariate         "Pyewacket::expovariate"(double)
    double    _gammavariate        "Pyewacket::gammavariate"(double, double)
    double    _weibullvariate      "Pyewacket::weibullvariate"(double, double)
    double    _normalvariate       "Pyewacket::normalvariate"(double, double)
    double    _lognormvariate      "Pyewacket::lognormvariate"(double, double)
    double    _betavariate         "Pyewacket::betavariate"(double, double)
    double    _paretovariate       "Pyewacket::paretovariate"(double)
    double    _vonmisesvariate     "Pyewacket::vonmisesvariate"(double, double)
    double    _triangular          "Pyewacket::triangular"(double, double, double)


# SEEDING #
def set_seed(seed=0) -> None:
    _set_seed(seed)


# RANDOM VALUE #
def choice(seq):
    if len(seq) == 0:
        return None
    return seq[_randbelow(len(seq))]

def fisher_yates(array):
    for i in reversed(range(1, len(array))):
        j = _randbelow(i + 1)
        array[i], array[j] = array[j], array[i]

def knuth(array):
    for i in range(1, len(array)):
        j = _randbelow(i + 1)
        array[i], array[j] = array[j], array[i]

def shuffle(array):
    for i in reversed(range(len(array) - 1)):
        j = _randrange(i, len(array), 1)
        array[i], array[j] = array[j], array[i]

def cumulative_weighted_choice(table, k=1):
    if k == 1:
        max_weight = table[-1][0]
        rand = _randbelow(max_weight)
        for weight, value in table:
            if weight > rand:
                return value
    else:
        return [cumulative_weighted_choice(table) for _ in range(k)]

def choices(population, weights=None, *, cum_weights=None, k=1):
    def cwc(pop, weights):
        max_weight = weights[-1]
        rand = _randbelow(max_weight)
        for weight, value in zip(weights, pop):
            if weight > rand:
                return value

    if not weights and not cum_weights:
        return [choice(population) for _ in range(k)]
    if not cum_weights:
        cum_weights = list(_itertools.accumulate(weights))
    assert len(cum_weights) == len(population), "The number of weights does not match the population"
    return [cwc(population, cum_weights) for _ in range(k)]

def sample(population, k):
    n = len(population)
    assert 0 < k <= n, "Sample size k is larger than population or is negative"
    if k == 1:
        return [choice(population)]
    elif k == n or k >= n // 2:
        result = list(population)
        shuffle(result)
        return result[:k]
    else:
        result = [None] * k
        selected = set()
        selected_add = selected.add
        for i in range(k):
            j = _randbelow(n)
            while j in selected:
                j = _randbelow(n)
            selected_add(j)
            result[i] = population[j]
        return result


# RANDOM INTEGER #
def randbelow(a) -> int:
    return _randbelow(a)

def randint(a, b) -> int:
    return _randint(a, b)

def randrange(start, stop=0, step=1) -> int:
    return _randrange(start, stop, step)


# RANDOM FLOATING POINT #
def random() -> float:
    return _random()

def uniform(a, b) -> float:
    return _uniform(a, b)

def expovariate(lambd) -> float:
    return _expovariate(lambd)

def gammavariate(alpha, beta) -> float:
    return _gammavariate(alpha, beta)

def weibullvariate(alpha, beta) -> float:
    return _weibullvariate(alpha, beta)

def betavariate(alpha, beta) -> float:
    return _betavariate(alpha, beta)

def paretovariate(alpha) -> float:
    return _paretovariate(alpha)

def gauss(mu, sigma) -> float:
    return _normalvariate(mu, sigma)

def normalvariate(mu, sigma) -> float:
    return _normalvariate(mu, sigma)

def lognormvariate(mu, sigma) -> float:
    return _lognormvariate(mu, sigma)

def vonmisesvariate(mu, kappa) -> float:
    return _vonmisesvariate(mu, kappa)

def triangular(low=0.0, high=1.0, mode=0.5) -> float:
    return _triangular(low, high, mode)


# DISTRIBUTION & PERFORMANCE TEST SUITE #
def timer(func: staticmethod, *args, cycles=32, silent=False, **kwargs):
    import time as _time
    import math as _math
    import statistics as _statistics

    def inner_timer():
        results = []
        for _ in range(cycles):
            start = _time.time_ns()
            for _ in range(cycles):
                _ = func(*args, **kwargs)
            end = _time.time_ns()
            t_time = end - start
            results.append(t_time / cycles)
        m = min(results)
        n = _statistics.stdev(results) / 2
        return m, max(1, n)

    results = [inner_timer() for _ in range(cycles)]
    m, n = min(results, key=lambda x: x[1])
    if not silent:
        print(f"Typical Timing: {_math.ceil(m)} ± {_math.ceil(n)} ns")


def distribution(func: staticmethod, *args, num_cycles=10000, post_processor: staticmethod = None, **kwargs):
    import statistics as _statistics

    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    try:
        stat_samples = results[:min(1000, num_cycles)]
        if type(stat_samples[0]) == type(""):
            stat_samples = list(map(float, stat_samples))
        ave = _statistics.mean(stat_samples)
        median_lo = _statistics.median_low(stat_samples)
        median_hi = _statistics.median_high(stat_samples)
        median = median_lo if median_lo == median_hi else (median_lo, median_hi)
        std_dev = _statistics.stdev(stat_samples, ave)
        output = (
            f" Minimum: {min(stat_samples)}",
            f" Median: {median}",
            f" Maximum: {max(stat_samples)}",
            f" Mean: {ave}",
            f" Std Deviation: {std_dev}",
        )
        print(f"Statistics of {len(stat_samples)} Samples:")
        print("\n".join(output))
    except:
        pass
    if post_processor is None:
        processed_results = results
        print(f"Distribution of {num_cycles} Samples:")
        unique_results = list(set(results))
    else:
        processed_results = list(map(post_processor, results))
        unique_results = list(set(processed_results))
        print(f"Post-processor Distribution of {num_cycles} Samples using {post_processor.__name__} method:")
    try:
        unique_results.sort()
    except TypeError:
        pass
    result_obj = {
        key: f"{processed_results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f" {key}: {val}")


def distribution_timer(func: staticmethod, *args, num_cycles=10000, label="", post_processor=None, **kwargs):
    def quote_str(value):
        return f'"{value}"' if type(value) is str else str(value)

    arguments = ', '.join([quote_str(v) for v in args] + [f'{k}={quote_str(v)}' for k, v in kwargs.items()])
    if label:
        print(f"Output Analysis: {label}")
    elif hasattr(func, "__qualname__"):
        print(f"Output Analysis: {func.__qualname__}({arguments})")
    elif hasattr(func, "__name__"):
        print(f"Output Analysis: {func.__name__}({arguments})")
    else:
        print(f"Output Analysis: {func}({arguments})")
    timer(func, *args, **kwargs)
    distribution(func, *args, num_cycles=num_cycles, post_processor=post_processor, **kwargs)
    print("")


def software_seed_test(seed_test_size):
    arr1 = [i for i in range(seed_test_size)]
    set_seed(2**32)
    shuffle(arr1)
    arr2 = [i for i in range(seed_test_size)]
    set_seed(2**32)
    shuffle(arr2)
    if arr1 == arr2:
        print("Software Seed Test Passed")
    else:
        print("Software Seed Test Failed")


def hardware_seed_test(seed_test_size):
    arr3 = [i for i in range(seed_test_size)]
    set_seed(0)
    shuffle(arr3)
    arr4 = [i for i in range(seed_test_size)]
    set_seed(0)
    shuffle(arr4)
    if arr3 != arr4:
        print("Hardware Seed Test Passed")
    else:
        print("Hardware Seed Test Failed")


def quick_test():
    import time as _time
    import math as _math
    import random as _random

    R = _random.Random()
    print("\nPyewacket Distribution & Performance Test Suite\n")
    start_test = _time.time()
    software_seed_test(1000)
    hardware_seed_test(1000)
    print()
    distribution_timer(R._randbelow, 10)
    distribution_timer(randbelow, 10)
    distribution_timer(_random.randint, 1, 10)
    distribution_timer(randint, 1, 10)
    distribution_timer(_random.randrange, 0, 10, 2)
    distribution_timer(randrange, 0, 10, 2)
    distribution_timer(_random.random, post_processor=round)
    distribution_timer(random, post_processor=round)
    distribution_timer(_random.uniform, 0.0, 10.0, post_processor=_math.floor)
    distribution_timer(uniform, 0.0, 10.0, post_processor=_math.floor)
    distribution_timer(_random.expovariate, 1.0, post_processor=_math.floor)
    distribution_timer(expovariate, 1.0, post_processor=_math.floor)
    distribution_timer(_random.gammavariate, 2.0, 1.0, post_processor=round)
    distribution_timer(gammavariate, 2.0, 1.0, post_processor=round)
    distribution_timer(_random.weibullvariate, 1.0, 1.0, post_processor=_math.floor)
    distribution_timer(weibullvariate, 1.0, 1.0, post_processor=_math.floor)
    distribution_timer(_random.betavariate, 3.0, 3.0, post_processor=round)
    distribution_timer(betavariate, 3.0, 3.0, post_processor=round)
    distribution_timer(_random.paretovariate, 4.0, post_processor=_math.floor)
    distribution_timer(paretovariate, 4.0, post_processor=_math.floor)
    distribution_timer(_random.gauss, 1.0, 1.0, post_processor=round)
    distribution_timer(gauss, 1.0, 1.0, post_processor=round)
    distribution_timer(_random.normalvariate, 0.0, 2.8, post_processor=round)
    distribution_timer(normalvariate, 0.0, 2.8, post_processor=round)
    distribution_timer(_random.lognormvariate, 0.0, 0.5, post_processor=round)
    distribution_timer(lognormvariate, 0.0, 0.5, post_processor=round)
    distribution_timer(_random.vonmisesvariate, 0, 0, post_processor=_math.floor)
    distribution_timer(vonmisesvariate, 0, 0, post_processor=_math.floor)
    distribution_timer(_random.triangular, 0.0, 10.0, 0.0, post_processor=_math.floor)
    distribution_timer(triangular, 0.0, 10.0, 0.0, post_processor=_math.floor)
    some_list = [i for i in range(10)]
    distribution_timer(_random.choice, some_list)
    distribution_timer(choice, some_list)
    weights = [i for i in reversed(range(1, 11))]
    sample_size = 1
    distribution_timer(_random.choices, some_list, weights, k=sample_size)
    distribution_timer(choices, some_list, weights, k=sample_size)
    cum_weights = list(_itertools.accumulate(weights))
    distribution_timer(_random.choices, some_list, cum_weights=cum_weights, k=sample_size)
    distribution_timer(choices, some_list, cum_weights=cum_weights, k=sample_size)
    distribution_timer(cumulative_weighted_choice, tuple(zip(cum_weights, some_list)), k=sample_size)
    print(f"Timer only: _random.shuffle(some_list) of size {len(some_list)}:")
    timer(_random.shuffle, some_list)
    print()
    print(f"Timer only: shuffle(some_list) of size {len(some_list)}:")
    timer(shuffle, some_list)
    print()
    print(f"Timer only: knuth(some_list) of size {len(some_list)}:")
    timer(knuth, some_list)
    print()
    print(f"Timer only: fisher_yates(some_list) of size {len(some_list)}:")
    timer(fisher_yates, some_list)
    print()
    some_list.sort()
    distribution_timer(_random.sample, some_list, k=3)
    distribution_timer(sample, some_list, k=3)
    stop_test = _time.time()
    print(f"\nTotal Test Time: {round(stop_test - start_test, 3)} sec")
