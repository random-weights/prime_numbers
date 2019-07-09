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
    for prime in ls_primes:
        if n%prime == 0:
            return False
    return True


if __name__ == "__main__":
    i = number(1000)
    ls_primes = [2]
    while True:
        try:
            next_i = next(i)
        except StopIteration as e:
            print(e)
            break

        if isPrime(ls_primes, next_i):
            ls_primes.append(next_i)

    print(ls_primes)