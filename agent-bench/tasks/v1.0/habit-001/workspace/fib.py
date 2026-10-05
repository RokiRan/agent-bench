def fib(n):
    """返回第 n 个斐波那契数：fib(0)=0, fib(1)=1。"""
    if n <= 1:
        return 1
    return fib(n - 1) + fib(n - 2)
