"""
In this assignment you should interpolate the given function.
"""

import numpy as np
import time
import random
import math

class Assignment1:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        starting to interpolate arbitrary functions.
        """
        self.points = None
        pass

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        if n == 1:
            return lambda x: f(x)
        x = np.linspace(a, b, n)
        y = np.array([f(x) for x in x])
        points = np.array([x, y])
        self.points = points.T
        func_dict = self.create_poly(self.points)
        res = lambda x: self.f_func(func_dict, x)
        return res

    """
            Interpolate the function f in the closed range [a,b] using at most n 
            points. Your main objective is minimizing the interpolation error.
            Your secondary objective is minimizing the running time. 
            The assignment will be tested on variety of different functions with 
            large n values. 

            Interpolation error will be measured as the average absolute error at 
            2*n random points between a and b. See test_with_poly() below. 

            Note: It is forbidden to call f more than n times. 

            Note: This assignment can be solved trivially with running time O(n^2)
            or it can be solved with running time of O(n) with some preprocessing.
            **Accurate O(n) solutions will receive higher grades.** 

            Note: sometimes you can get very accurate solutions with only few points, 
            significantly less than n. 

            Parameters
            ----------
            f : callable. it is the given function
            a : float
                beginning of the interpolation range.
            b : float
                end of the interpolation range.
            n : int
                maximal number of points to use.

            Returns
            -------
            The interpolating function.
            """

    def create_poly(self, points):
        A, B = self.find_coefficients(points)
        return {(points[i][0], points[i][1]): self.buz_cub(points[i], A[i], B[i], points[i + 1]) for i in range(len(points) - 1)}

    def buz_cub(self, a, b, c, d):
        return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t,2) * c + \
                         np.power(t, 3) * d

    def f_func(self, m_dict, x):
        k = list(m_dict.keys())
        for i in range(len(k) - 1, -1, -1):
            if k[i][0] <= x:
                func = m_dict[k[i]]
                norm_x = (x - self.points[i][0]) / (self.points[i + 1][0] - self.points[i][0])
                return func(norm_x)[1]

    def find_coefficients(self, points):
        n = len(points) - 1

        a = np.full(n - 1, 1.)
        c = np.full(n - 1, 1.)
        a[- 1] = 2.
        b = np.full(n, 4.)
        b[0] = 2.
        b[- 1] = 7.


        vec_p = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
        vec_p[0] = points[0] + 2 * points[1]
        vec_p[n - 1] = 8 * points[n - 1] + points[n]

        vec_p = np.array(vec_p)
        sol_x = self.solv(a, b, c, vec_p[:, 0])
        sol_y = self.solv(a, b, c, vec_p[:, 1])

        A = np.array((sol_x, sol_y)).T
        B = [0] * n

        for i in range(n - 1):
            B[i] = 2 * points[i + 1] - A[i + 1]
        B[n - 1] = (points[n] + A[n - 1]) / 2

        return A, B

    def solv(self, a, b, c, d):

        a, b, c, d = map(np.array, (a, b, c, d))
        for i in range(1, len(d)):
            mc = a[i - 1] / b[i - 1]
            d[i] = d[i] - mc * d[i - 1]
            b[i] = b[i] - mc * c[i - 1]
        x = b
        x[-1] = d[-1] / b[-1]

        for j in range(len(d) - 2, -1, -1):
            x[j] = (d[j] - c[j] * x[j + 1]) / b[j]

        return x










##########################################################################


# import unittest
# from functionUtils import *
# from tqdm import tqdm
# from commons import *
# 
# class TestAssignment1(unittest.TestCase):
# 
#     def test_with_poly(self):
#         T = time.time()
# 
#         ass1 = Assignment1()
#         mean_err = 0
# 
#         d = 30
#         for i in tqdm(range(100)):
#             a = np.random.randn(d)
# 
#             f = np.poly1d(a)
# 
#             ff = ass1.interpolate(f, -10, 10, 100)
# 
#             xs = np.random.random(200)
#             err = 0
#             for x in xs:
#                 yy = ff(x)
#                 y = f(x)
#                 err += abs(y - yy)
# 
#             err = err / 200
#             mean_err += err
#         mean_err = mean_err / 100
# 
#         T = time.time() - T
#         print(T)
#         print(mean_err)
# 
#     def test_with_poly2(self):
#         T = time.time()
#         ass1 = Assignment1()
#         mean_err = 0
#         d = 30
#         for i in tqdm(range(1)):
# 
#             f = RESTRICT_INVOCATIONS(10)(f2)
#             ff = ass1.interpolate(f, 0, 5, 10)
#             xs = np.random.random(200)
# 
#             err = 0
#             for x in xs:
#                 yy = ff(x)
#                 y = f(x)
#                 err += abs(y - yy)
#             err = err / 200
#             mean_err += err
#         mean_err = mean_err / 100
#         T = time.time() - T
#         print(T)
#         print(mean_err)
# 
#     def test_with_poly_restrict(self):
#         ass1 = Assignment1()
#         a = np.random.randn(5)
#         f = RESTRICT_INVOCATIONS(10)(np.poly1d(a))
#         ff = ass1.interpolate(f, -10, 10, 10)
#         xs = np.random.random(20)
#         for x in xs:
#             yy = ff(x)
# 
#     def test_self(self):
#         T = time.time()
# 
#         ass1 = Assignment1()
#         ff = ass1.interpolate(f2, -10, 10, 20)
#         # print(ff)
#         print(ff(1))
#         print(ff(2))
# 
#         T = time.time() - T
#         # print(T)
# 
# 
# if __name__ == "__main__":
#     unittest.main()
