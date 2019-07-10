import time
from multiprocessing import Process, Queue, Manager
import os

def number(integer_q,n):
    """
    a generator
    :param n: the upper bound not inclusive
    :return: an iterator of consecutive integers.
    """
    print("number Process Started")
    i = 3
    while i<n:
        integer_q.put(i)
        i += 1
    print("number process Ended")
    return 0


man = Manager()
shared_ls_primes = man.list()

def generatePrime(integer_q):
    """
    Checks if the given number is prime or not
    :param n: input positive integer
    :param ls_primes: list of all primes numbers found
    :return: boolean True if n is prime
    """
    print("Prime Process started")
    pcount = 0
    while True:
        try:
            n = integer_q.get_nowait()
            pcount += 1
        except Exception as e:
            print("queue is empty")
            break

        # determine the stop index after which no division is necessary
        global shared_ls_primes

        is_prime = True

        ##check for divisibility untill stop index
        for prime in shared_ls_primes:
            if n%prime == 0:
                is_prime = False
                break

        ##if the number is prime, append to global list
        if is_prime:
            shared_ls_primes.append(n)
    print("Prime process ended, looked at {0} numbers".format(pcount))
    return 0


if __name__ == "__main__":
    shared_ls_primes.append(2)

    start = time.time()

    integer_q = Queue()
    i1 = Process(target=number,args=(integer_q,10000))
    p1 = Process(target=generatePrime, args=(integer_q,))
    p2 = Process(target=generatePrime, args=(integer_q,))

    i1.start()
    time.sleep(2)
    p1.start()
    p2.start()

    i1.join()
    p1.join()
    p2.join()

    end = time.time()
    duration = end - start
    print("Total Time taken: {0:.4g} seconds".format(duration))
    print(shared_ls_primes)