import math  # I am guessing that you will need to use the math module
import random
from point import Point

import numpy as np
import scipy.spatial as ss


class PointPattern(object):

    def __init__(self):
        self.points = []

    def add_pt (self,point):
        self.points.append(point)

    def remove_pt (self,index):
        del(self.points[index])

    def number_coincident_points(self):
        num=0;
        coincident_list=[]
        for i, p1 in enumerate(self.points):
            for j, p2 in enumerate(self.points):
                if i!=j:
                    if p2 not in coincident_list:
                        if p1==p2:
                            num+=1
                            coincident_list.append(p2)
        return num


    def list_marks(self):
        mark_list=[]
        for i in self.points:
            if i.mark not in mark_list:
                mark_list.append(i.mark)
        return mark_list

    def points_by_mark(self):
    #return a subset of points by the mark
        return 0;

    def n_rand_pts(self,n=None,marks=None):
        temp=[]
        if(n==None):
            n=len(self.points);

        for i in range(n):
            temp.append(Point(random.uniform(0,1),random.uniform(0,1),random.choice(self.marks)));

        return temp

    def gen_rand_pts(self,upper_bound=1,lower_bound=0,num_pts=100):

        return np.random.uniform(lower_bound,upper_bound, (num_pts,2));

    def critical_pts(distances):
        return min(distances), max(distances)

    def nearest_neighbor_dist_numpy(self):

        return

    def average_nearest_neighbor_distance_kd(self,pts=None):
        mean=0;


        if pts==None:
            points = self.points
        else:
            points=pts

        kdtree = ss.KDTree(points);
        for i in points:
            dist_nearest, nn_pt = kdtree.query(i, k=2)
            mean+=dist_nearest.item(1);

            #print(dist_nearest.item(1))
        return mean/len(points);

    def average_nearest_neighbor_distance_numpy(self,pts=None):
        '''
            computing using numpy
        '''
        points=[]
        if pts==None:
            points = self.points
        else:
            points=pts

        nn_dists = np.array([])

        n_dist_current=math.inf
        #print(pts)
        for i, point1 in enumerate(points):
            for j, point2 in enumerate(points):

                if i==j:
                    continue
                elif(ss.distance.euclidean(point1, point2)<n_dist_current):
                    n_dist_current=ss.distance.euclidean(i,j);

            nn_dists=np.concatenate((nn_dists,[n_dist_current]),axis=0);
            n_dist_current=math.inf;

        return np.mean(nn_dists);

    def g_func(self,nsteps):
        '''
            computing using numpy
        '''

        nn_dists = []

        for i, point1 in enumerate(self.points):
            nn_dist=math.inf
            for j, point2 in enumerate(self.points):
                if i==j:
                    continue
                elif(ss.distance.euclidean(point1,point2)<nn_dist):
                    nn_dist = ss.distance.euclidean(point1,point2)
            nn_dists.append(nn_dist)


        max_nn_dist=max(nn_dists)
        min_nn_dist=min(nn_dists)
        big_n = len(self.points)
        #print(big_n)

        ds = np.linspace(0,max_nn_dist+0.1,nsteps) #apply numpy


        #print(nn_dists)
        g_func_results=[]
        ds_outputs=[]
        for i in range(nsteps):
            #print(ds[i])
            count=0
            for curr_nn_dist in nn_dists:
                if curr_nn_dist<ds[i]:
                    count+=1
            ds_outputs.append(ds[i])
            g_func_results.append(count/big_n)

        return (g_func_results,ds_outputs)
