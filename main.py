"""
Using python multiprocessing and little common sense,
this algorithm can list out all prime numbers before n.

Run time complexity is yet to be determined. will be updated
in later commits.
"""

import time
from multiprocessing import Process, Pipe, Manager
import os


def distributor(ls_feed_pipe_open,low,high):
    """
    Takes input ends of all feed pipes and feeds odd numbers starting
    from low until high both inclusive. in a round robin fashion.

    process ends by feeding -1 to all pipes. -1 is a sentinel value.

    :param ls_feed_pipe_open: list of all open ends of feed pipes
    :param low: lower bound integer inclusive
    :param high: upper bound integer inclusive
    :return: none.
    """
    def getNumber(low,high):
        i = low
        if i%2 == 0:        #if i is even, then start from i+1 odd.
            i += 1
        while i<=high:
            yield i
            i+=2            #no need to check for even numbers, so skip it here at begining
        yield -1            #when generator yields -1, it reached high, so terminate

    next_pipe = 0
    number = getNumber(low,high)
    while True:
        msg = next(number)
        if msg == -1:       #to check when generator reached high.
            break
        else:
            #feed pipes in a round robin fashion,
            #so that over time each generatePrime process experiences same load.
            ls_feed_pipe_open[next_pipe].send(msg)
            next_pipe += 1
            if next_pipe == len(ls_feed_pipe_open):
                next_pipe = 0
    for p in ls_feed_pipe_open:
        p.send(-1)              #-1 is sentinel value for all generatePrime processs
    return 0


def generatePrime(ls_primes, feed_pipe,return_dict):
    """
    will take numbers sequentially from feed_pipe,
    verify if it is prime.
    any primes found will be returned as a dict to main process.
    dict contains only one key value pair. val is always a list.
    :param ls_primes: list of primes, read only.
    :param feed_pipe: output end of one feed pipe.
    :param return_dict: manager dictionary to get primes computed by each process
    :return: None.
    """
    local_primes = []
    while True:
        n = feed_pipe.recv()
        if n == -1:             # sentinel given by distributor.
            break
        else:
            is_prime = True

            ##check for divisibility
            ## no need to check for 2 since all are odd numbers
            for prime in ls_primes[1:]:
                if n%prime == 0:
                    is_prime = False
                    break

            ##if the number is prime, append to global list
            if is_prime:
                local_primes.append(n)
    if len(local_primes) >0:
        return_dict[os.getpid()] = local_primes
        return return_dict
    return 0



if __name__ == "__main__":

    start = time.time()

    # change nprocs value to generate more generatePrime processes.
    nprocs = 8

    ls_primes = [2,3,5,7,11,13,17]
    last_checked = ls_primes[-1]
    for _ in range(2):
        low = max(ls_primes[-1]+1,last_checked)
        # to check if n is prime. you only need to check if its divisible by all primes less than floor(sqrt(n))
        # so, when our greatest known prime is n, we can check all numbers from n to n^2 for primality.
        high = ls_primes[-1]**2
        last_checked = high
        print("Checking numbers from {0} to {1}".format(low,high))

        input_ends = []
        output_ends = []
        for _ in range(nprocs):
            inp,out = Pipe()
            input_ends.append(inp)
            output_ends.append(out)

        # only 1 distributor process.
        d1 = Process(target=distributor,args=(input_ends,low,high))

        #manager dict for getting primes from all generatePrime processes.
        man = Manager()
        return_dict = man.dict()
        ls_prime_pros = []
        for i in range(nprocs):
            ls_prime_pros.append(Process(target=generatePrime, args=(ls_primes,output_ends[i],return_dict)))

        d1.start()
        for p in ls_prime_pros:
            p.start()

        d1.join()
        for p in ls_prime_pros:
            p.join()

        # collect primes from all generatePrime Processes,
        # sort and append to ls_primes.
        new_primes = []
        for _,val in return_dict.items():
            for i in val:
                new_primes.append(i)
        new_primes = sorted(new_primes)
        # appending new primes found to ls_primes.
        ls_primes = ls_primes+new_primes
    end = time.time()
    duration = end - start
    print("Total Time taken: {0:.4g} seconds".format(duration))
    print(ls_primes)

