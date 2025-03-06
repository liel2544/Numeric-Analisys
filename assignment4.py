"""
In this assignment you should fit a model function of your choice to data 
that you sample from a given function. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you take an iterative approach and know that 
your iterations may take more than 1-2 seconds break out of any optimization 
loops you have ahead of time.

Note: You are NOT allowed to use any numeric optimization libraries and tools 
for solving this assignment. 

"""
import math
import numpy as np
import time
import random


class Assignment4:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before
        solving the assignment for specific functions.
        """

        pass

    def fit(self, f: callable, a: float, b: float, d: int, maxtime: float) -> callable:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape.

        Parameters
        ----------
        f : callable.
            A function which returns an approximate (noisy) Y value given X.
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds.

        Returns
        -------
        a function:float->float that fits f between a and b
        """

        t = time.time()
        y = f(b - 0.000001)
        samp_time = time.time() - t
        rest_time = maxtime - samp_time

        if rest_time == maxtime:
            xx = np.linspace(a, b, 10000)
        else:
            xx = np.linspace(a, b, max(1, int(1.4 * rest_time / (samp_time + 0.01))))

        y = []
        flag = False
        # for x in xx:
        try:
            y.append(f(xx))
        except:
            for x in xx:
                try:
                    y.append(f(x))
                except:
                    f = np.vectorize(f)
                    flag = True
                    y.append(0)
                    continue

        yy = np.ravel(y)
        # yy = np.array(y)


        initial_time = time.time() - t
        rest_time = maxtime - initial_time - 0.4
        i = 1
        temp = []
        while (time.time() - t) <= rest_time:
            try:
                yy += f(xx)
            except:
                for x in xx:
                    try:
                        temp.append(f(x))
                    except:
                        f = np.vectorize(f)
                        temp.append(0)
                yy += np.array(temp)
                temp = []
            i += 1

        yy = yy / i
        yyy = np.diff(yy)
        d_new = 1
        while np.sum(yyy) >= 0.00001:
            yyy = np.diff(yyy)
            d_new += 1
        if abs(np.mean(yy) - yy[0]) <= 0.001:
            return lambda line: yy[0]

        if d_new > 1:
            A = np.vander(xx, d_new)
        else:
            A = np.vander(xx, d + 1)

        a_y = A.transpose().dot(yy)
        a_a = A.transpose().dot(A)
        c = np.linalg.inv(a_a).dot(a_y)
        return np.polynomial.Polynomial(np.flip(c))


##########################################################################


# import unittest
# from sampleFunctions import *
# from tqdm import tqdm
# from commons import *
# 
# 
# class TestAssignment4(unittest.TestCase):
# 
#     def test_return(self):
#         f = DELAYED(1)(NOISY(0.01)(poly(1, 1, 1)))
#         ass4 = Assignment4()
#         T = time.time()
#         shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
#         T = time.time() - T
#         self.assertLessEqual(T, 5)
# 
#     def test_delay(self):
#         f = DELAYED(7)(NOISY(0.01)(poly(1, 1, 1)))
#         ass4 = Assignment4()
#         T = time.time()
#         shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
#         T = time.time() - T
#         self.assertGreaterEqual(T, 5)
# 
#     def test_err(self):
#         f = poly(1, 1, 1)
#         nf = NOISY(1)(f)
#         ass4 = Assignment4()
#         T = time.time()
#         ff = ass4.fit(f=nf, a=0, b=1, d=10, maxtime=5)
#         T = time.time() - T
#         mse = 0
#         for x in np.linspace(0, 1, 1000):
#             self.assertNotEqual(f(x), nf(x))
#             mse += (f(x) - ff(x)) ** 2
#         mse = mse / 1000
# 
#     def test_return2(self):
#         f = NOISY(0.01)(RESTRICT_INVOCATIONS(10)(f6))
#         ass4 = Assignment4()
#         T = time.time()
#         shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
#         T = time.time() - T
#         # self.assertLessEqual(T, 5)
# 
# 
# if __name__ == "__main__":
#     unittest.main()
