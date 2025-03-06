"""
In this assignment you should find the intersection points for two functions.
"""
import math
import numpy as np
import time
import random
from collections.abc import Iterable


class Assignment2:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """
        pass

    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> Iterable:
        """
        Find as many intersection points as you can. The assignment will be
        tested on functions that have at least two intersection points, one
        with a positive x and one with a negative x.
        
        This function may not work correctly if there is infinite number of
        intersection points. 


        Parameters
        ----------
        f1 : callable
            the first given function
        f2 : callable
            the second given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        maxerr : float
            An upper bound on the difference between the
            function values at the approximate intersection points.


        Returns
        -------
        X : iterable of approximate intersection Xs such that for each x in X:
            |f1(x)-f2(x)|<=maxerr.

        """

        g = self.make_g(f1, f2)
        intervals = self.get_intervals(a, b, f1, f2)
        intersects = []
        for i in range(1, len(intervals)):
            root = self.newton_raphson(g, intervals[i - 1], intervals[i], maxerr)
            if root:
                intersects.append(root)
        return intersects

    def get_intervals(self, a, b, f1, f2):
        p = int(np.ceil(abs(b-a) * 30)) #todo:33
        return np.linspace(a, b, p, endpoint=True)

    def make_g(self, f1, f2):
        def g(x):
            try:
                return f1(x) - f2(x)
            except:
                return np.inf
        return g

    def bisection(self, g, a, b, maxerr):
        ans = 0.5 * a + 0.5 * b
        while not abs(a - b) < maxerr:
            if np.sign(g(ans)) != np.sign(g(a)):
                b = ans
            else:
                a = ans
            ans = 0.5 * a + 0.5 * b
        return ans

    def der_f(self, f):
        h = 1e-5
        return lambda x: (f(x + h) - f(x - h)) / (2 * h)

    def newton_raphson(self, g, a, b, maxerr):
        max_iter = 10
        x = self.bisection(g, a, b, maxerr)
        i = 0

        while abs(g(x)) >= maxerr:
            if i == max_iter:
                return None
            d_g = self.der_f(g)
            if d_g(x) == 0:
                if abs(g(x)) <= maxerr:
                    return x
                return None
            x = x - g(x) / d_g(x)
            i += 1
        if b >= x >= a:
            return x
        return None


##########################################################################


# import unittest
# from sampleFunctions import *
# from tqdm import tqdm
# from commons import *
# 
# class TestAssignment2(unittest.TestCase):
# 
#     def test_sqr(self):
# 
#         ass2 = Assignment2()
# 
#         f1 = np.poly1d([-1, 0, 1])
#         f2 = np.poly1d([1, 0, -1])
# 
#         X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)
# 
#         for x in X:
#             self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))
# 
#     def test_sqr2(self):
#         start_time = time.perf_counter()
# 
#         ass2 = Assignment2()
# 
#         def f1(x):
#             return (x - 3) ** 2 - x + 1
# 
#         def f2(x):
#             return x + 1
# 
#         X = ass2.intersections(f1, f2, 1, 100, maxerr=0.001)
#         print(X)
#         for x in X:
#             self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         print(f'Elapsed time: {elapsed_time:.3f} seconds')
# 
#     def test_poly(self):
# 
#         ass2 = Assignment2()
# 
#         f1, f2 = randomIntersectingPolynomials(10)
# 
#         X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)
# 
#         for x in X:
#             self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))
# 
#     def test_sqr3(self):
#         start_time = time.perf_counter()
# 
#         ass2 = Assignment2()
# 
#         def f10(x):
#             return math.sin(math.log(x))
# 
#         def f3_nr(x):
#             return math.sin(pow(x, 2))
# 
#         X = ass2.intersections(f10, f3_nr, 1, 10, maxerr=0.001)
#         print(X)
#         for x in X:
#             self.assertGreaterEqual(0.001, abs(f10(x) - f3_nr(x)))
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         print(f'Elapsed time: {elapsed_time:.3f} seconds')
# 
#     def test_sinlog_sinsqrt(self):
#         start_time = time.perf_counter()
#         ass2 = Assignment2()
#         X = sorted(ass2.intersections(f3_nr, f10, 1, 10))
#         print(X)
#         print(len(X))
#         print(f' the expected is :{[1.62899, 2.6973, 3.725809, 3.7914655]}')
#         for x in X: self.assertGreaterEqual(0.001, abs(f3_nr(x) - f10(x)))
#         for x in X:
#             print(abs(f3(x) - f10(x)), x)
#         print(len(X))
# if __name__ == "__main__":
#     unittest.main()
