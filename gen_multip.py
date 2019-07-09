"""
Experiments with generators in multi processing
"""
import time

from multiprocessing import Process


def getInteger(low,high):
    """
    yield consecuitve integer between low and high both inclusive
    :param low: lower bound integer inclusive
    :param high: higher bound integer inclusive
    :return: integer iterator
    """
    i = low
    while i <= high:
        yield i
        i += 1

def printer(pid,i):
    while True:
        try:
            print("{0} from process {1}".format(i.next(),pid))
        except Exception as e:
            print("Process with PID: {0} is terminated".format(pid))
            return 0


if __name__ == "__main__":
    """
    Doesnt work as expected. Looks like each process creates its own copy of iterator
    and each process goes from 10 to 100. Didnt work as expected. 
    """
    i1 = getInteger(10,100)
    p1 = Process(target = printer, args=(1,i1,))
    p2 = Process(target = printer, args = (2,i1,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("All processes ended")