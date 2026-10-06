import random
import time

from topk import topk_frequent


def test_perf_200k_under_1s():
    random.seed(42)
    stream = [random.randint(0, 5000) for _ in range(200_000)]
    start = time.perf_counter()
    result = topk_frequent(stream, 10)
    elapsed = time.perf_counter() - start
    assert len(result) == 10
    assert elapsed < 1.0, f"耗时 {elapsed:.2f}s 超过 1s 门槛"
