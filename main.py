import time
from multiprocessing import Process, Pipe, Manager
import os

def getNumber(main_pipe_input,low,high):
    print("Feeding batch of numbers from {0} to {1}".format(low,high))
    i = low
    while i<=high:
        main_pipe_input.send(i)
        i += 1
    main_pipe_input.send(-1)
    return 0


def distributor(main_pipe_output,ls_feed_pipe_input):
    next_pipe = 0
    while True:
        msg = main_pipe_output.recv()
        if msg == -1:
            break
        else:
            ls_feed_pipe_input[next_pipe].send(msg)
            next_pipe += 1
            if next_pipe == len(ls_feed_pipe_input):
                next_pipe = 0
    for p in ls_feed_pipe_input:
        p.send(-1)
    return 0


def generatePrime(ls_primes, feed_pipe_output,return_dict):
    pcount = 0
    local_primes = []
    while True:
        n = feed_pipe_output.recv()
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
    ls_primes = [2,3,5,7,11,13,17]
    for _ in range(3):
        low = ls_primes[-1] + 1
        high = ls_primes[-1]**2

        mpipei,mpipeo = Pipe()

        i1 = Process(target = getNumber,args=(mpipei,low,high))

        input_ends = []
        output_ends = []
        for _ in range(8):
            inp,out = Pipe()
            input_ends.append(inp)
            output_ends.append(out)
        d1 = Process(target=distributor,args=(mpipeo,input_ends))

        man = Manager()
        return_dict = man.dict()
        ls_prime_pros = []
        for i in range(8):
            ls_prime_pros.append(Process(target=generatePrime, args=(ls_primes,output_ends[i],return_dict)))

        i1.start()
        d1.start()
        for p in ls_prime_pros:
            p.start()

        i1.join()
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
    print(ls_primes[-1])
