def fib(n):
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b


print(list(fib(10)))
