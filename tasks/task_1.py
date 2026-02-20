def caching_fibonacci():
    """Create a memoized Fibonacci function using a closure.

    The cache dictionary is created once and shared across all calls to the
    returned inner function, so previously computed values are never
    recalculated.

    Returns:
        fibonacci (Callable[[int], int]): A function that accepts a non-negative
            integer ``n`` and returns the n-th Fibonacci number.
            The returned function exposes two counters as attributes mainly for testing purposes:
            - ``cache_hits``   — number of times a result was served from cache
            - ``cache_misses`` — number of times a result was freshly computed
    """
    cache = {}

    def fibonacci(n: int) -> int:
        """Return the n-th Fibonacci number, using a shared cache.

        The sequence is defined as:
            F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1.

        Negative values of ``n`` are treated as 0.

        Args:
            n (int): Index in the Fibonacci sequence (0-based).

        Returns:
            int: The n-th Fibonacci number.
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            fibonacci.cache_hits += 1
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        fibonacci.cache_misses += 1
        return cache[n]

    fibonacci.cache_hits = 0
    fibonacci.cache_misses = 0
    return fibonacci
