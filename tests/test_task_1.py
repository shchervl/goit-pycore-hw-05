import logging
import pytest
from tasks.task_1 import caching_fibonacci


def test_base_case_zero():
    fib = caching_fibonacci()
    assert fib(0) == 0


def test_base_case_one():
    fib = caching_fibonacci()
    assert fib(1) == 1


def test_negative_returns_zero():
    fib = caching_fibonacci()
    assert fib(-1) == 0
    assert fib(-10) == 0


def test_known_fibonacci_values_served_from_cache(caplog):
    fib = caching_fibonacci()

    # Warm the cache up to fib(20)
    with caplog.at_level(logging.DEBUG, logger="tasks.task_1"):
        fib(20)
        caplog.clear()  # discard warm-up log records

        # All smaller known values must now come from cache, not recomputed
        expected = {2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 10: 55, 20: 6765}
        for n, val in expected.items():
            caplog.clear()
            result = fib(n)
            assert result == val, f"fib({n}) should be {val}"
            assert any("cache hit" in r.message for r in caplog.records), (
                f"fib({n}) should have been served from cache"
            )


def test_independent_instances_have_separate_caches():
    fib1 = caching_fibonacci()
    fib2 = caching_fibonacci()

    # Extract the cache dict from each closure cell
    cache1 = fib1.__closure__[0].cell_contents
    cache2 = fib2.__closure__[0].cell_contents

    # They must be different objects in memory
    assert cache1 is not cache2

    # Populate fib1's cache
    fib1(10)
    assert 10 in cache1      # fib1 cached the result
    assert 10 not in cache2  # fib2's cache is unaffected


def test_cache_hit_logged(caplog):
    fib = caching_fibonacci()

    with caplog.at_level(logging.DEBUG, logger="tasks.task_1"):
        fib(5)               # populate cache
        caplog.clear()       # discard warm-up log records
        fib(5)               # should log a cache hit
        assert any("cache hit" in r.message for r in caplog.records)


def test_larger_value_uses_cache_for_known_entries(caplog):
    fib = caching_fibonacci()

    with caplog.at_level(logging.DEBUG, logger="tasks.task_1"):
        fib(20)        # warm cache with fib(1)..fib(20)
        caplog.clear()

        result = fib(30)
        assert result == 832040

        messages = [r.message for r in caplog.records]
        computed  = [m for m in messages if "computed" in m]
        cache_hits = [m for m in messages if "cache hit" in m]

        # fib(21)..fib(30) must be freshly computed — exactly 10 new entries
        assert len(computed) == 10
        # previously cached values (≤20) must be reused, not recomputed
        assert len(cache_hits) > 0
