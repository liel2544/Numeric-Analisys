"""
In this assignment you should fit a model function of your choice to data 
that you sample from a contour of given shape. Then you should calculate
the area of that shape. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you know that your iterations may take more 
than 1-2 seconds break out of any optimization loops you have ahead of time.

Note: You are allowed to use any numeric optimization libraries and tools you want
for solving this assignment. 
Note: !!!Despite previous note, using reflection to check for the parameters 
of the sampled function is considered cheating!!! You are only allowed to 
get (x,y) points from the given shape by calling sample(). 
"""
import math
import matplotlib.patches as patches
from shapely.geometry import Polygon
import numpy as np
import time
import random
import sklearn
from functionUtils import AbstractShape
from sklearn.datasets import *
from functionUtils import AbstractShape
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors


class MyShape(AbstractShape):
    # change this class with anything you need to implement the shape
    def __init__(self,S):
        self.S = S
        pass

    def area(self):
        return np.float32(self.S)

class Assignment5:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def area(self, contour: callable, maxerr=0.001) -> np.float32:
        """
        Compute the area of the shape with the given contour. 

        Parameters
        ----------
        contour : callable
            Same as AbstractShape.contour 
        maxerr : TYPE, optional
            The target error of the area computation. The default is 0.001.

        Returns
        -------
        The area of the shape.

        """

        points = contour(400)
        x = points[:, 0]
        y = points[:, 1]
        res = 0
        for i in range(len(points)):
            res += 0.5 * (x[i] - x[i - 1]) * (y[i - 1] + y[i])
        return np.float32(res)

    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        
        Parameters
        ----------
        sample : callable. 
            An iterable which returns a data point that is near the shape contour.
        maxtime : float
            This function returns after at most maxtime seconds. 

        Returns
        -------
        An object extending AbstractShape. 
        """
        n = 5000
        m = 5
        samples = np.array([sample() for _ in range(n)])
        points = db_scan(samples, n, m)
        R = radial_sorting(points)
        x, y = R
        polygon = Polygon(list(zip(x, y)))
        return MyShape(polygon.area)


def db_scan(samples, n, m):
    nbrs = NearestNeighbors(n_neighbors=m).fit(samples)
    distances = np.sort(nbrs.kneighbors(samples)[0][:, 1])
    x = np.arange( n)
    data = np.column_stack((x, distances))
    theta = np.arctan2(data[:, 1].max() - data[:, 1].min(),data[:, 0].max() - data[:, 0].min())
    rotation_matrix = np.array(((np.cos(theta), -np.sin(theta)), (np.sin(theta), np.cos(theta))))
    rotated_vector = data.dot(rotation_matrix)
    idx = np.where(rotated_vector == rotated_vector.min())[0][0]
    elbow = data[idx][1]
    db = DBSCAN(eps=elbow, min_samples=m).fit(samples)
    return db.components_


def radial_sorting(points):
    x, y = points.T
    x0 = np.mean(x)
    y0 = np.mean(y)
    r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
    angles = np.where((y - y0) > 0, np.arccos((x - x0) / r), 2 * np.pi - np.arccos((x - x0) / r))
    mask = np.argsort(angles)
    x_sorted = x[mask]
    y_sorted = y[mask]
    return x_sorted, y_sorted





##########################################################################


# import unittest
# from sampleFunctions import *
# from tqdm import tqdm
# 
# 
# class TestAssignment5(unittest.TestCase):
# 
#     def test_return(self):
#         circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
#         ass5 = Assignment5()
#         T = time.time()
#         shape = ass5.fit_shape(sample=circ, maxtime=5)
#         T = time.time() - T
#         self.assertTrue(isinstance(shape, AbstractShape))
#         self.assertLessEqual(T, 5)
# 
#     def test_delay(self):
#         circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
# 
#         def sample():
#             time.sleep(0.1)
#             return circ()
# 
#         ass5 = Assignment5()
#         T = time.time()
#         shape = ass5.fit_shape(sample=sample, maxtime=5)
#         T = time.time() - T
#         self.assertTrue(isinstance(shape, AbstractShape))
#         self.assertGreaterEqual(T, 5)
# 
#     def test_circle_area(self):
#         circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
#         ass5 = Assignment5()
#         T = time.time()
#         shape = ass5.fit_shape(sample=circ, maxtime=30)
#         T = time.time() - T
#         a = shape.area()
#         self.assertLess(abs(a - np.pi), 0.01)
#         self.assertLessEqual(T, 32)
# 
#     def test_bezier_fit(self):
#         circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
#         ass5 = Assignment5()
#         T = time.time()
#         shape = ass5.fit_shape(sample=circ, maxtime=30)
#         T = time.time() - T
#         a = shape.area()
#         self.assertLess(abs(a - np.pi), 0.01)
#         self.assertLessEqual(T, 32)
# 
# 
# if __name__ == "__main__":
#     unittest.main()
