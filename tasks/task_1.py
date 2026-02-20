import logging

logger = logging.getLogger(__name__)


def caching_fibonacci():
    """Create a memoized Fibonacci function using a closure.

    The cache dictionary is created once and shared across all calls to the
    returned inner function, so previously computed values are never
    recalculated.

    Returns:
        fibonacci (Callable[[int], int]): A function that accepts a non-negative
            integer ``n`` and returns the n-th Fibonacci number.
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
            # Added for testing purpose 
            logger.debug("fib(%d): cache hit → %d", n, cache[n])
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        # Added for testing purpose 
        logger.debug("fib(%d): computed → %d", n, cache[n])
        return cache[n]

    return fibonacci