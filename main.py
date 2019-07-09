import time

def number(n):
    """
    a generator
    :param n: the upper bound not inclusive
    :return: an iterator of consecutive integers.
    """
    i = 3
    while i<n:
        yield i
        i += 1


def isPrime(ls_primes, n):
    """
    Checks if the given number is prime or not
    :param n: input positive integer
    :param ls_primes: list of all primes numbers found
    :return: boolean True if n is prime
    """
    prime = True
    mid_point = int(n/2)
    stop_index = 0
    for i,p in enumerate(ls_primes):
        if p >= mid_point:
            stop_index = i
            break

    for prime in ls_primes[0:stop_index]:
        if n%prime == 0:
            return False
    return True


if __name__ == "__main__":
    i = number(100000)
    ls_primes = [2]

    start = time.time()

    while True:
        try:
            next_i = next(i)
        except StopIteration as e:
            print(e)
            break

        if isPrime(ls_primes, next_i):
            ls_primes.append(next_i)
    end = time.time()
    duration = end - start
    print("Total Time taken: {0:.4g} seconds".format(duration))