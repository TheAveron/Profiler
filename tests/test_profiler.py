# tests/test_profiler.py

import unittest

from profiler import (
    profile,
    profile_async,
    profile_with_memory,
    profile_with_memory_graph,
)

import time
import random
import string


class TestProfiler(unittest.TestCase):

    def test_sync_profile(self):
        @profile
        def simple_add(a, b):
            return a + b

        result = simple_add(1, 2)
        self.assertEqual(result, 3)

    def test_async_profile(self):
        import asyncio

        @profile_async
        async def async_add(a, b):
            return a + b

        result = asyncio.run(async_add(1, 2))
        self.assertEqual(result, 3)

    def test_profile_with_memory(self):
        @profile_with_memory
        def simple_add(a, b):
            return a + b

        result = simple_add(3, 4)
        self.assertEqual(result, 7)

    def test_profile_with_memory_graph(self):

        @profile_with_memory_graph
        def complex_memory_function(
            iterations=4,
            base_size=20_000,
            spike_factor=5,
        ):
            """
            Function designed to stress memory allocation patterns:
            - progressive growth
            - temporary spikes
            - garbage creation
            """

            results = []

            for i in range(iterations):
                data = [random.random() for _ in range(base_size * (i + 1))]
                results.append(sum(data[:1000]))

                time.sleep(0.1)
                mapping = {
                    j: "".join(random.choices(string.ascii_letters, k=20))
                    for j in range(base_size // 10)
                }

                time.sleep(0.1)

                spike = [
                    [random.randint(0, 1000) for _ in range(100)]
                    for _ in range((base_size // 100) * spike_factor)
                ]

                time.sleep(0.1)

                del spike
                del mapping

                text = ""
                for _ in range(2000):
                    text += random.choice(string.ascii_lowercase)

                results.append(len(text))

                time.sleep(0.1)

            final = {
                "mean": sum(results) / len(results),
                "max": max(results),
                "count": len(results),
            }

            return final

        print("result:", complex_memory_function())

    def test_profile_with_memory_graph_2(self):
        @profile_with_memory_graph
        def fibo():
            fibonacci_numbers = {0: 0, 1: 1}

            def fibonacci(n):
                if n in fibonacci_numbers:
                    return fibonacci_numbers[n]
                return fibonacci(n - 1) + fibonacci(n - 2)

            for i in range(100_000):
                fibonacci_numbers[i] = fibonacci(i)

            return fibonacci_numbers

        fibo()


if __name__ == "__main__":
    unittest.main()
