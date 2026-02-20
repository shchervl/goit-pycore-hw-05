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


def test_known_fibonacci_values_served_from_cache():
    fib = caching_fibonacci()

    # Warm the cache up to fib(20)
    fib(20)
    hits_after_warmup = fib.cache_hits

    # All smaller known values must now come from cache, not recomputed
    expected = {2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 10: 55, 20: 6765}
    for n, val in expected.items():
        hits_before = fib.cache_hits
        misses_before = fib.cache_misses
        result = fib(n)
        assert result == val, f"fib({n}) should be {val}"
        assert (
            fib.cache_hits == hits_before + 1
        ), f"fib({n}) should have been a cache hit"
        assert (
            fib.cache_misses == misses_before
        ), f"fib({n}) should not have triggered a new computation"


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
    assert 10 in cache1  # fib1 cached the result
    assert 10 not in cache2  # fib2's cache is unaffected


def test_cache_hit_increments_counter():
    fib = caching_fibonacci()
    fib(5)  # populate cache (internal recursion may also hit cache)
    hits_before = fib.cache_hits  # snapshot after warm-up
    fib(5)  # top-level call must be exactly one more cache hit
    assert fib.cache_hits == hits_before + 1


def test_larger_value_uses_cache_for_known_entries():
    fib = caching_fibonacci()
    fib(20)  # warm cache with fib(1)..fib(20)
    misses_after_warmup = fib.cache_misses

    result = fib(30)
    assert result == 832040

    # fib(21)..fib(30) must be freshly computed — exactly 10 new misses
    assert fib.cache_misses == misses_after_warmup + 10
    # previously cached values (≤20) must be reused, not recomputed
    assert fib.cache_hits > 0
