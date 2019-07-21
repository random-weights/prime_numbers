"""
sieve of e....list out all numbers from 3 to n.

cross off numbers by making multiple passes over the array.

dont store numbers, instead store only the boolean isPrime
which by default is set to True for all numbers.
since the array starts with integer 3, number at any index is i+3 where
i is the index
"""
import sys
import math

class Primes:
    def __init__(self,n):
        if n <= sys.maxsize:
            try:
                self.ls_primes = [True]*n
                print("Array of booleans created")
            except Exception as e:
                print(e)
        self.n = n
        self.curr_prime = 2

    def epoch(self,multiplier):
        multiple = multiplier*2
        while multiple <= self.n:
            self.ls_primes[multiple - 2] = False
            multiple += multiplier

        print("All multiples of {0} crossed off".format(multiplier))

    def getNextPrime(self):
        index = self.curr_prime - 1
        while True:
            if self.ls_primes[index]:
                break
            else:
                index += 1
        self.curr_prime = index + 2
        return self.curr_prime

    def getMaxPrime(self):
        last_index = self.n - 2
        while True:
            if self.ls_primes[last_index]:
                return last_index + 2
            else:
                last_index += -1

if __name__ == "__main__":
    n = int(input("Enter the upper bound: "))
    p = Primes(n)
    for _ in range(1000):
        p.epoch(p.curr_prime)
        p.getNextPrime()
    print(p.getMaxPrime())
