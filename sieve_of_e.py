"""
sieve of e....list out all numbers from 2 to n.

cross off numbers by making multiple passes over the array.

dont store numbers, instead store only the boolean isPrime

which by default is set to True for all numbers.

since the array starts with integer 2, number at any index is i+2 where

i is the index
"""
import sys,time
import numpy as np

class Primes:
    def __init__(self,n):
        """
        initializes a numpy boolean array of size n
        :param n: integer upto which we want to find prime numbers
        """

        #to make sure our array isn't too big for memory allocation
        if n <= sys.maxsize:
            try:
                # we used numpy array instead of python list because
                # python stores boolean as integer rather than single bit
                self.ls_primes = np.ones((n),dtype = bool)
                print("Array of booleans created")
            except Exception as e:
                print(e)
        self.n = n
        self.curr_prime = 2

    def epoch(self,multiplier):
        """
        always call getNextPrime() after epoch()
        :param multiplier: is always the curr_prime
        :return: None
        """
        multiple = multiplier*2
        while multiple <= self.n:
            self.ls_primes[multiple - 2] = False
            multiple += multiplier

        #print("All multiples of {0} crossed off".format(multiplier))

    def getNextPrime(self):
        """
        will check for next true value in ls_primes after curr_prime
        updates instance variable curr_prime after each epoch.
        :return: None
        """
        index = self.curr_prime - 1
        while True:
            if self.ls_primes[index]:
                break
            else:
                index += 1
        self.curr_prime = index + 2
        return self.curr_prime

    def getMaxPrime(self):
        """
        after all epochs, find largest prime by looking
        for True value from end of numpy array working backwards.
        :return: largest prime found below self.n
        """
        last_index = self.n - 2
        while True:
            if self.ls_primes[last_index]:
                return last_index + 2
            else:
                last_index += -1


if __name__ == "__main__":
    n = int(input("Enter the upper bound: "))

    start = time.time()
    p = Primes(n)
    while p.curr_prime <= n:
        p.epoch(p.curr_prime)
        p.getNextPrime()
    print(p.getMaxPrime())
    end = time.time()

    print("Total time taken: {0:.4g}".format(end-start))
