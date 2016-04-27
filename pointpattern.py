from point import Point
import analytics
import random
import numpy as np
import scipy.spatial as ss

class PointPattern(object):
    def __init__(self):
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def average_nearest_neighbor_distance(self, mark=None):
        return analytics.average_nearest_neighbor_distance(self.points, mark)

    def average_nearest_neighbor_distance_kdtree(self, mark_name=None):
        temp_points = []
        real_points = []
        distances = []

        if mark_name is None:
            temp_points = self.points
        else:
            for point in self.points:
                if point.mark is mark:
                    temp_points.append(point)

        for point in temp_points:
            real_points.append((point.x, point.y))

        kdtree = ss.KDTree(real_points)

        for p in real_points:
            nearest_neighbor_distance, nearest_neighbor = kdtree.query(p, k=2)
            distances.append(nearest_neighbor_distance)

        return np.mean(distances)

    def remove_point(self, index):
        del(self.points[index])

    def count_coincident_points(self):
        count = 0
        coincident_list = []

        for i, point in enumerate(self.points):
            for j, point2 in enumerate(self.points):
                if i is j:
                    continue
                if j in coincident_list:
                    continue
                #Should use the magic method in point class
                if point == point2:
                    count += 1
                    coincident_list.append(j)
        return count

    def list_marks(self):
        marks = []

        for point in self.points:
            if point.mark is not None and point.mark not in marks:
                marks.append(point.mark)

        return marks

    def return_subset(self, mark):
        #creates a list of points that have the same mark as passed
        return [i for i in self.points if i.mark is mark]

    def create_random_points(self, n=None):
        rand_points = []
        rand = random.Random()
        marks = ['North', 'East', 'South', 'West']

        if n is None:
            n = len(self.points)

        for i in range(n):
            rand_points.append(Point(rand.randint(1,100), rand.randint(1,100), mark=rand.choice(marks)))

        return rand_points

    def generate_random_points(self, min=0, max=1, count=2):
        marks = ['North', 'East', 'South', 'West']
        rand_points = np.random.uniform(min, max, (count,2))
        generated_points = []

        for i, rpoint in enumerate(rand_points):
            generated_points.append(point.Point(rpoint[0], rpoint[1], mark=random.choice(marks)))

        return generated_points

    def create_realizations(self, k):
        return analytics.permutations(k)

    def critical_points(self):
        return analytics.find_criticals(self.create_realizations(99))

    def compute_g(self, nsteps):
        ds = np.linspace(0, 100, nsteps)
        g_sum = 0

        for step in range(nsteps):
            o_i = ds[step]
            min_dis = None
            for i, j in enumerate(ds):

                temp = abs(j - o_i)

                if i is step:
                    continue
                if min_dis is None:
                    min_dis = temp
                elif min_dis > temp:
                    min_dis = temp
                else:
                    continue
            g_sum += min_dis
        return g_sum / nsteps



