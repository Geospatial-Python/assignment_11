from point import Point
import math
import random
import numpy as np


class PointPattern():

    def __init__(self,points):
        self.points = points[:]


    def average_nearest_neighbor_distance(self,mark=None):

        """
        Given a set of points, compute the average nearest neighbor.

        Parameters
        ----------
        points : list
                 A list of points
        mark   : str

        Returns
        -------
        mean_d : float
                 Average nearest neighbor distance

        References
        ----------
        Clark and Evan (1954 Distance to Nearest Neighbor as a
         Measure of Spatial Relationships in Populations. Ecology. 35(4)
         p. 445-453.
        """
        mean_d = 0
        if mark==None:
            points_tmp=self.points
        else:
            points_tmp=[ point for point in self.points if point.mark==mark]

        length=len(points_tmp)

        #print(self.points)
        nearest_distances=[]
        for i in range(length):
            distance=[]
            for j in range(length):
                if i==j:
                    continue
                else:
                    distance.append(self.euclidean_distance((points_tmp[i].x,points_tmp[i].y),(points_tmp[j].x,points_tmp[j].y)))
            nearest_distances.append(min(distance))

        mean_d=float(sum(nearest_distances)/len(nearest_distances))
        return mean_d

    def number_of_coincident_points(self):

        length=len(self.points)
        number_of_coincident_points=0
        for i in range(length):
            for j in range(length):
                if i==j:
                    continue
                else:
                    if self.check_coincident((self.points[i].x,self.points[i].y),(self.points[j].x,self.points[j].y)):
                        number_of_coincident_points+=1
        return number_of_coincident_points

    def list_marks(self):

        points_marks=set()
        for point in self.points:
            if point.mark!=None:
                points_marks.add(point.mark)

        return list(points_marks)

    def list_subset_of_points(self,mark):

        return [point for point in self.points if point.mark==mark]

    def create_random_marked_points(self, n=None,domain_min=0,domain_max=1,marks=[]):

        if n == None:
            n=len(self.points)

        randoms_list=np.random.uniform(domain_min, domain_max, (n,2))
        points_list=[]
        for i in range(n):
            if len(marks)!=0:
                points_list.append(Point(randoms_list[i][0], randoms_list[i][1],random.choice(marks)))
            else:
                points_list.append(Point(randoms_list[i][0], randoms_list[i][1]))
        return points_list

    def create_realizations(self, k):

        return self.permutations(k)

    def permutations(self,p=99, n=100):
        """
        Return the mean nearest neighbor distance of p permutations.

        Parameters
        ----------
        p : integer
        n : integer

        Returns
        -------
        permutations : list
                the mean nearest neighbor distance list.

        """
        permutation_list=[]
        for i in range(p):
            permutation_list.append(self.average_nearest_neighbor_distance())
        return permutation_list

    def critical_points(self,permutations):
        """
        Return the mean nearest neighbor distance of p permutations.

        Parameters
        ----------
        permutations : list
            the mean nearest neighbor distance list.
        Returns
        -------
        smallest  : float
        largest   : float

        """

        return min(permutations),max(permutations)

    def compute_g(self,nsteps):

        ds = np.linspace(0, 1, nsteps)
        min_list=[]
        for i_index,di in enumerate(ds):
            tmp_list=[]
            for j_index,dj in enumerate(ds):
                if i_index != j_index:
                    tmp_list.append(np.abs(di-dj))

            min_list.append(np.min(tmp_list))

        return np.mean(min_list)



    def check_coincident(self,a, b):
        """
        Check whether two points are coincident
        Parameters
        ----------
        a : tuple
            A point in the form (x,y)

        b : tuple
            A point in the form (x,y)

        Returns
        -------
        equal : bool
                Whether the points are equal
        """
        return a == b

    def euclidean_distance(self,a, b):
        """
        Compute the Euclidean distance between two points

        Parameters
        ----------
        a : tuple
            A point in the form (x,y)

        b : tuple
            A point in the form (x,y)

        Returns
        -------

        distance : float
                   The Euclidean distance between the two points
        """
        distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
        return distance


