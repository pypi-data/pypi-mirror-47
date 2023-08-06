#!python3
#distutils: language = c++

import time as _time
import math as _math
import statistics as _statistics


__all__ = (
    "TruffleShuffle", "QuantumMonty", "CumulativeWeightedChoice", "RelativeWeightedChoice", "FlexCat",
    "random_below", "random_index", "random_int", "random_range", "d", "dice", "ability_dice",
    "percent_true", "plus_or_minus", "plus_or_minus_linear", "plus_or_minus_gauss",
    "shuffle", "knuth", "fisher_yates", "random_value",
    "cumulative_weighted_choice", "canonical", "random_float",
    "front_gauss", "middle_gauss", "back_gauss", "quantum_gauss", "front_poisson",
    "middle_poisson", "back_poisson", "quantum_poisson", "front_linear",
    "middle_linear", "back_linear", "quantum_linear", "quantum_monty",
    "distribution_timer", "distribution", "timer", "fuzzy_clamp", "smart_clamp", "flatten", "test_warm_up",
    "min_int", "max_int", "min_float", "max_float", "min_above", "min_below",
    "random_rotate",
)


cdef extern from "Fortuna.hpp":
    int           _percent_true           "Fortuna::percent_true"(double)
    int           _ability_dice           "Fortuna::ability_dice"(int)
    long long     _min_int                "Fortuna::min_int"()
    long long     _max_int                "Fortuna::max_int"()
    long long     _smart_clamp            "Fortuna::smart_clamp"(long long, long long, long long)
    long long     _fuzzy_clamp            "Fortuna::fuzzy_clamp"(long long, long long)
    long long     _random_range           "Fortuna::random_range"(long long, long long, long long)
    long long     _random_below           "Fortuna::random_below"(long long)
    long long     _random_index           "Fortuna::random_index"(long long)
    long long     _random_int             "Fortuna::random_int"(long long, long long)
    long long     _d                      "Fortuna::d"(long long)
    long long     _dice                   "Fortuna::dice"(long long, long long)
    long long     _plus_or_minus          "Fortuna::plus_or_minus"(long long)
    long long     _plus_or_minus_linear   "Fortuna::plus_or_minus_linear"(long long)
    long long     _plus_or_minus_gauss    "Fortuna::plus_or_minus_gauss"(long long)
    long long     _front_gauss            "Fortuna::front_gauss"(long long)
    long long     _middle_gauss           "Fortuna::middle_gauss"(long long)
    long long     _back_gauss             "Fortuna::back_gauss"(long long)
    long long     _quantum_gauss          "Fortuna::quantum_gauss"(long long)
    long long     _front_poisson          "Fortuna::front_poisson"(long long)
    long long     _middle_poisson         "Fortuna::middle_poisson"(long long)
    long long     _back_poisson           "Fortuna::back_poisson"(long long)
    long long     _quantum_poisson        "Fortuna::quantum_poisson"(long long)
    long long     _front_linear           "Fortuna::front_linear"(long long)
    long long     _middle_linear          "Fortuna::middle_linear"(long long)
    long long     _back_linear            "Fortuna::back_linear"(long long)
    long long     _quantum_linear         "Fortuna::quantum_linear"(long long)
    long long     _quantum_monty          "Fortuna::quantum_monty"(long long)
    long double   _min_float              "Fortuna::min_float"()
    long double   _max_float              "Fortuna::max_float"()
    long double   _min_below              "Fortuna::min_below"()
    long double   _min_above              "Fortuna::min_above"()
    long double   _canonical              "Fortuna::generate_canonical"()
    long double   _random_float           "Fortuna::random_float"(long double, long double)
    long double   _triangular             "Fortuna::triangular"(long double, long double, long double)


def min_int():
    return _min_int()

def max_int():
    return _max_int()

def min_float():
    return _min_float()

def max_float():
    return _max_float()

def min_above():
    return _min_above()

def min_below():
    return _min_below()


# Random Integer #
def random_below(number):
    return _random_below(number)

def random_index(limit):
    return _random_index(limit)

def random_int(left_limit, right_limit):
    return _random_int(left_limit, right_limit)

def random_range(start, stop=0, step=1):
    return _random_range(start, stop, step)

def d(sides=20):
    return _d(sides)

def dice(rolls=1, sides=20):
    return _dice(rolls, sides)

def ability_dice(rolls=4):
    return _ability_dice(rolls)

def plus_or_minus(number=1):
    return _plus_or_minus(number)

def plus_or_minus_linear(number=1):
    return _plus_or_minus_linear(number)

def plus_or_minus_gauss(number=1):
    return _plus_or_minus_gauss(number)


# Random Bool #
def percent_true(truth_factor=50.0) -> bool:
    return _percent_true(truth_factor) == 1


# Random Floats #
def canonical() -> float:
    return _canonical()

def random_float(left_limit=0.0, right_limit=1.0) -> float:
    return _random_float(left_limit, right_limit)


# Utilities #
def smart_clamp(target, lo, hi):
    return _smart_clamp(target, lo, hi)

def fuzzy_clamp(target, upper_bound):
    return _fuzzy_clamp(target, upper_bound)

def flatten(itm, flat=True):
    if flat is False or not callable(itm):
        return itm
    else:
        try:
            return flatten(itm())
        except TypeError:
            return itm


# Shuffle #
def shuffle(list array):
    size = len(array) - 1
    for i in reversed(range(size)):
        j = _random_int(i, size)
        array[i], array[j] = array[j], array[i]

def fisher_yates(list array):
    size = len(array)
    for i in reversed(range(1, size)):
        j = _random_below(i + 1)
        array[i], array[j] = array[j], array[i]

def knuth(list array):
    size = len(array)
    for i in range(1, size):
        j = _random_below(i + 1)
        array[i], array[j] = array[j], array[i]

def random_rotate(data: list, zero_cool: staticmethod = _random_index):
    r = zero_cool(len(data))
    return data[r:] + data[:r]


# ZeroCool Methods #
def front_gauss(size):
    return _front_gauss(size)

def middle_gauss(size):
    return _middle_gauss(size)

def back_gauss(size):
    return _back_gauss(size)

def quantum_gauss(size):
    return _quantum_gauss(size)

def front_poisson(size):
    return _front_poisson(size)

def middle_poisson(size):
    return _middle_poisson(size)

def back_poisson(size):
    return _back_poisson(size)

def quantum_poisson(size):
    return _quantum_poisson(size)

def front_linear(size):
    return _front_linear(size)

def middle_linear(size):
    return _middle_linear(size)

def back_linear(size):
    return _back_linear(size)

def quantum_linear(size):
    return _quantum_linear(size)

def quantum_monty(size):
    return _quantum_monty(size)


# Fortuna Generator Functions #
def random_value(data, flat=True):
    return flatten(data[_random_index(len(data))], flat=flat)

def cumulative_weighted_choice(weighted_table, flat=True):
    max_weight = weighted_table[-1][0]
    rand = _random_below(max_weight)
    for weight, value in weighted_table:
        if weight > rand:
            return flatten(value, flat=flat)


# Fortuna Generator Classes #
class TruffleShuffle:
    __slots__ = ("flat", "data")

    def __init__(self, sequence_data, flat=True):
        self.flat = flat
        self.data = list(sequence_data)
        assert len(self.data) > 0, "Input Error, Empty Container"
        shuffle(self.data)

    def __call__(self):
        result = self.data.pop()
        self.data.insert(_front_poisson(len(self.data) - 1), result)
        return flatten(result, flat=self.flat)

    def __str__(self):
        output = (
            "TruffleShuffle(sequence_data",
            f", flat={self.flat}" if not self.flat else "",
            ")",
        )
        return "".join(output)


class QuantumMonty:
    __slots__ = ("flat", "size", "data", "truffle_shuffle")

    def __init__(self, sequence_data, flat=True):
        self.flat = flat
        self.data = tuple(sequence_data)
        self.size = len(self.data)
        assert self.size > 0, "Input Error, Empty Container"
        self.truffle_shuffle = TruffleShuffle(self.data, flat)

    def __call__(self):
        return self.quantum_monty()

    def dispatch(self, monty):
        return {
            "flat_uniform": self.flat_uniform,
            "truffle_shuffle": self.truffle_shuffle,
            "front_linear": self.front_linear,
            "middle_linear": self.middle_linear,
            "back_linear": self.back_linear,
            "quantum_linear": self.quantum_linear,
            "front_gauss": self.front_gauss,
            "middle_gauss": self.middle_gauss,
            "back_gauss": self.back_gauss,
            "quantum_gauss": self.quantum_gauss,
            "front_poisson": self.front_poisson,
            "middle_poisson": self.middle_poisson,
            "back_poisson": self.back_poisson,
            "quantum_poisson": self.quantum_poisson,
            "quantum_monty": self.quantum_monty,
        }[monty]

    def flat_uniform(self):
        return flatten(self.data[_random_index(self.size)], self.flat)

    def front_linear(self):
        return flatten(self.data[_front_linear(self.size)], self.flat)

    def middle_linear(self):
        return flatten(self.data[_middle_linear(self.size)], self.flat)

    def back_linear(self):
        return flatten(self.data[_back_linear(self.size)], self.flat)

    def quantum_linear(self):
        return flatten(self.data[_quantum_linear(self.size)], self.flat)

    def front_gauss(self):
        return flatten(self.data[_front_gauss(self.size)], self.flat)

    def middle_gauss(self):
        return flatten(self.data[_middle_gauss(self.size)], self.flat)

    def back_gauss(self):
        return flatten(self.data[_back_gauss(self.size)], self.flat)

    def quantum_gauss(self):
        return flatten(self.data[_quantum_gauss(self.size)], self.flat)

    def front_poisson(self):
        return flatten(self.data[_front_poisson(self.size)], self.flat)

    def middle_poisson(self):
        return flatten(self.data[_middle_poisson(self.size)], self.flat)

    def back_poisson(self):
        return flatten(self.data[_back_poisson(self.size)], self.flat)

    def quantum_poisson(self):
        return flatten(self.data[_quantum_poisson(self.size)], self.flat)

    def quantum_monty(self):
        return flatten(self.data[_quantum_monty(self.size)], self.flat)

    def __str__(self):
        output = (
            "QuantumMonty(sequence_data",
            f", flat={self.flat}" if not self.flat else "",
            ")",
        )
        return "".join(output)


class FlexCat:
    __slots__ = ("key_bias", "val_bias", "flat", "random_cat", "random_selection")

    def __init__(self, matrix_data: dict, key_bias="front_linear", val_bias="truffle_shuffle", flat=True):
        self.key_bias = key_bias
        self.val_bias = val_bias
        self.flat = flat
        self.random_cat = QuantumMonty(tuple(matrix_data.keys()), flat=False).dispatch(key_bias)
        self.random_selection = {
            key: QuantumMonty(tuple(seq), flat=flat).dispatch(val_bias) for key, seq in matrix_data.items()
        }

    def __call__(self, cat_key=None):
        monty = self.random_selection
        key = cat_key if cat_key is not None else self.random_cat()
        return monty[key]()

    def __str__(self):
        output = (
            "FlexCat(matrix_data",
            f", key_bias='{self.key_bias}'" if self.key_bias is not "front_linear" else "",
            f", val_bias='{self.val_bias}'" if self.val_bias is not "truffle_shuffle" else "",
            f", flat={self.flat}" if not self.flat else "",
            ")",
        )
        return "".join(output)


class WeightedChoice:
    __slots__ = ("flat", "max_weight", "data")

    def __call__(self):
        rand = _random_below(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return flatten(value, self.flat)


class RelativeWeightedChoice(WeightedChoice):
    __slots__ = ("flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.flat = flat
        optimized_data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __str__(self):
        output = (
            "RelativeWeightedChoice(weighted_table",
            f", flat={self.flat}" if not self.flat else "",
            ")",
        )
        return "".join(output)


class CumulativeWeightedChoice(WeightedChoice):
    __slots__ = ("flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.flat = flat
        data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
        prev_weight = 0
        for w_pair in data:
            w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
        optimized_data = sorted(data, key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __str__(self):
        output = (
            "CumulativeWeightedChoice(weighted_table",
            f", flat={self.flat}" if not self.flat else "",
            ")",
        )
        return "".join(output)


# Test Suite

def timer(func: staticmethod, *args, cycles=32, silent=False, **kwargs):

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


def distribution(func: staticmethod, *args, num_cycles=1000000, post_processor: staticmethod = None, **kwargs):
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    try:
        stat_samples = results[:min(100, num_cycles)]
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
        pro_results = results
        print(f"Distribution of {num_cycles} Samples:")
        unique_results = list(set(results))
    else:
        pro_results = list(map(post_processor, results))
        unique_results = list(set(pro_results))
        print(f"Post-processor Distribution of {num_cycles} Samples using {post_processor.__name__}():")

    results = [
        tuple([itm, f"{pro_results.count(itm) / (num_cycles / 100)}%", pro_results.count(itm)]) for itm in unique_results
    ]
    try:
        results.sort()
    except TypeError:
        results.sort(key=lambda x: x[2])
    for key, val, _ in results:
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


def test_warm_up():
    timer(random_int, min_int(), max_int(), cycles=96, silent=True)
