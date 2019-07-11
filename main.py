import time
from multiprocessing import Process, Queue, Pipe, Manager
import os


def distributor(ls_feed_pipe_open,low,high):
    def getNumber(low,high):
        i = low
        if i%2 == 0:
            i += 1

        while i<=high:
            yield i
            i+=2
        yield -1

    next_pipe = 0
    number = getNumber(low,high)
    while True:
        msg = next(number)
        if msg == -1:
            break
        else:
            ls_feed_pipe_open[next_pipe].send(msg)
            next_pipe += 1
            if next_pipe == len(ls_feed_pipe_open):
                next_pipe = 0
    for p in ls_feed_pipe_open:
        p.send(-1)
    return 0


def generatePrime(ls_primes, feed_pipe,return_dict):
    pcount = 0
    local_primes = []
    while True:
        n = feed_pipe.recv()
        if n == -1:
            break
        else:
            pcount += 1
            is_prime = True

            ##check for divisibility
            for prime in ls_primes:
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

    new_prime_queue = Queue()
    ls_primes = [2,3,5,7,11,13,17]
    last_checked = ls_primes[-1]
    for _ in range(3):
        low = max(ls_primes[-1]+1,last_checked)
        high = ls_primes[-1]**2
        last_checked = high
        print("Checking numbers from {0} to {1}".format(low,high))

        input_ends = []
        output_ends = []
        for _ in range(8):
            inp,out = Pipe()
            input_ends.append(inp)
            output_ends.append(out)
        d1 = Process(target=distributor,args=(input_ends,low,high))

        man = Manager()
        return_dict = man.dict()
        ls_prime_pros = []
        for i in range(8):
            ls_prime_pros.append(Process(target=generatePrime, args=(ls_primes,output_ends[i],return_dict)))

        d1.start()
        for p in ls_prime_pros:
            p.start()

        d1.join()
        for p in ls_prime_pros:
            p.join()


        new_primes = []
        for _,val in return_dict.items():
            for i in val:
                new_primes.append(i)
        new_primes = sorted(new_primes)
        ls_primes = ls_primes+new_primes
    end = time.time()
    duration = end - start
    print("Total Time taken: {0:.4g} seconds".format(duration))
    print(ls_primes)
