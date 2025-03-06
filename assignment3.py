"""
In this assignment you should find the area enclosed between the two given functions.
The rightmost and the leftmost x values for the integration are the rightmost and 
the leftmost intersection points of the two functions. 

The functions for the numeric answers are specified in MOODLE. 


This assignment is more complicated than Assignment1 and Assignment2 because: 
    1. You should work with float32 precision only (in all calculations) and minimize the floating point errors. 
    2. You have the freedom to choose how to calculate the area between the two functions. 
    3. The functions may intersect multiple times. Here is an example: 
        https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx
    4. Some of the functions are hard to integrate accurately. 
       You should explain why in one of the theoretical questions in MOODLE. 

"""
import math

import numpy as np
import time
import random
import assignment2
from assignment2 import *



class Assignment3:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def integrate(self, f: callable, a: float, b: float, n: int) -> np.float32:
        """
                       Integrate the function f in the closed range [a,b] using at most n
                       points. Your main objective is minimizing the integration error.
                       Your secondary objective is minimizing the running time. The assignment
                       will be tested on variety of different functions.

                       Integration error will be measured compared to the actual value of the
                       definite integral.

                       Note: It is forbidden to call f more than n times.

                       Parameters
                       ----------
                       f : callable. it is the given function
                       a : float
                           beginning of the integration range.
                       b : float
                           end of the integration range.
                       n : int
                           maximal number of points to use.

                       Returns
                       -------
                       np.float32
                           The definite integral of f between a and b
                       """

        if n == 1:
            mid = (a + b) / 2
            height = mid - a
            return np.float32(abs(f(mid) * height * 2))
        if n % 2 == 1:
            n += 1
        h = (b - a) / (n - 2)
        x = np.linspace(a, b, n - 1)
        result = [f(i) for i in x]
        y = np.array(result)
        res = y[0] + y[n - 2] + 2 * np.sum(y[2:-1:2]) + 4 * np.sum(y[1:-1:2])
        res *= h / 3
        return abs(np.float32(res))

    def areabetween(self, f1: callable, f2: callable) -> np.float32:
        """
        Finds the area enclosed between two functions. This method finds
        all intersection points between the two functions to work correctly.

        Example: https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx

        Note, there is no such thing as negative area.

        In order to find the enclosed area the given functions must intersect
        in at least two points. If the functions do not intersect or intersect
        in less than two points this function returns NaN.
        This function may not work correctly if there is infinite number of
        intersection points.


        Parameters
        ----------
        f1,f2 : callable. These are the given functions

        Returns
        -------
        np.float32
            The area between function and the X axis

        """
        ass2 = Assignment2()
        intersects = np.sort(list(ass2.intersections(f1, f2, 1, 100)))
        if len(intersects) < 2:
            return np.NaN
        g = lambda x: abs(f1(x) - f2(x))
        S = self.integrate(g, intersects[0], intersects[-1], 1000)
        return S


##########################################################################


# import unittest
# from sampleFunctions import *
# from tqdm import tqdm
# 
# 
# class TestAssignment3(unittest.TestCase):
# 
#     def test_integrate_float32(self):
#         ass3 = Assignment3()
#         f1 = np.poly1d([-1, 0, 1])
#         r = ass3.integrate(f1, -1, 1, 10)
# 
#         self.assertEquals(r.dtype, np.float32)
# 
#     # def test_integrate_hard_case(self):
#     #     ass3 = Assignment3()
#     #     f1 = strong_oscilations()
#     #     r = ass3.integrate(f1, 0.09, 10, 20)
#     #     true_result = -7.78662 * 10 ** 33
#     #     self.assertGreaterEqual(0.001, abs((r - true_result) / true_result))
# 
#     def test_areabetween_sinlnx_strong_oscilations(self):
#         start_time = time.perf_counter()
#         ass3 = Assignment3()
#         f1 = strong_oscilations()
#         f2 = f10
# 
#         res = ass3.areabetween(f1, f2)
#         print(res)
#         true_result = 9.21011
#         self.assertGreaterEqual(0.001, abs(res - true_result))
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         print(f'Elapsed time: {elapsed_time:.3f} seconds')
# 
#     def test_areabetween_sin_ln_e(self):
#         start_time = time.perf_counter()
#         ass3 = Assignment3()
# 
#         def f1(x):
#             return math.sin(math.log(x))
# 
#         def f2(x):
#             return math.exp(-2 * x ** 2)
# 
#         res = ass3.areabetween(f1, f2)
#         print(res)
#         true_result = 12.04809
#         self.assertGreaterEqual(0.001, abs(res - true_result))
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         print(f'Elapsed time: {elapsed_time:.3f} seconds')
# 
#     def test_areabetween_sinlnx_1_ln(self):
#         start_time = time.perf_counter()
#         ass3 = Assignment3()
# 
#         def f1(x):
#             return math.sin(math.log(x))
# 
#         def f2(x):
#             return 1 / math.log(x)
# 
#         res = ass3.areabetween(f1, f2)
#         print(res)
#         true_result = 3.33770
#         self.assertGreaterEqual(0.001, abs(res - true_result))
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         print(f'Elapsed time: {elapsed_time:.3f} seconds')
# 
#     def test_areabetween_poly(self):
#         start_time = time.perf_counter()
# 
#         ass3 = Assignment3()
# 
#         def f1(x):
#             return (x - 3) ** 2 - x + 1
# 
#         def f2(x):
#             return x + 1
# 
#         res = ass3.areabetween(f1, f2)
#         print(res)
#         true_result = 24.69367
#         self.assertGreaterEqual(0.001, abs(res - true_result))
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         print(f'Elapsed time: {elapsed_time:.3f} seconds')
# 
#     def test_area(self):
#         ass = Assignment3()
#         f1 = np.sin
#         f2 = np.cos
#         print(ass.areabetween(f1, f2))
# 
# 
# if __name__ == "__main__":
#     unittest.main()
