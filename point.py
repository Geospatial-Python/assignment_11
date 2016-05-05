#from utils import check_coincident
import utils
import random
import analytics
import numpy as np
import scipy.spatial as ss
#from .utils import *

class Point(object):

	#Create a point class with three attributes, x, y, and a keyword argument mark. Please place the point pattern class in point.py.
	def __init__(self, x, y, mark={}):
		self.x = x
		self.y = y
		self.mark = mark

	#Update your Point class to utilize at least 3 magic methods. You are free to choose what magic methods to implement.
	
	#check if the two objects are equal
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	#add the x and y courdinates of both objects
	def __add__(self,other):
		return Point(self.x + other.x,self.y + other.y)
	#negate the x and y courdinates of the point objects
	def __neg__(self):
		return Point(-self.x,-self.y,self.mark)

	#Add a method to the Point class to chec if another point, passed as an argument, is coincident. Remember that you already wrote this logic.
	def check_coincident(self,other):
		return utils.check_coincident((self.x, self.y), (other.x, other.y))

	#Add a method to shift the point in some direction. This logic is also already written.
	def shift_point(self, dx, dy):
		return utils.shift_point((self.x,self.y),dx,dy)

#Create a PointPattern class. This class should be able to compute statistics about your point pattern. It should be able to:
class PointPattern:

	#initialize an array of points as empty
	def __init__(self, theList):
		self.points = theList

	#Average nearest neighbor distance (with or without mark specification)
	def average_nearest_neighbor_distance(self, mark=None):
		return utils.average_nearest_neighbor_distance(self.points, mark)

	#Number of coincident points
	def num_coincident(self):
		count = 0
		coincidnet_list = []
		for i in range(len(self.points)):
			for j in range(len(self.points)):
				if i in coincidnet_list or i==j:
					continue
				if self.points[i] == self.points[j]:
					count = count+1
					coincidnet_list.append(j)
		return count
	
	#Add a point to the point list
	def add_point(self,point):
		self.points.append(point)
		#print('sup')

	#Remove a point from the point list
	def remove_point(self,index):
		del(self.points[index])

	#List the marks, for example if the points are marked 'r' and 'b', this should return ['r', 'b']
	def list_marks(self):
		markList = []
		for point in self.points:
			if point.mark not in markList:
				markList.append(point.mark)
		return markList

	#Return a subset of points by mark type
	def subset_by_mark(self, mark):
		subset = []
		for point in self.points:
			if point.mark == mark:
				subset.append(p)
		return subset

	#Generate n random points where n is either provided by the user or equal to the current size of the point pattern.
	def create_n_random_points(self,n =None):
		randos = create_random_marked_points(n = len(self.points),marks = [])
		return randos
	
	#Generate k realizations of random points. That is, simulate k random point patterns for use in Monte Carlo simulation.
	def create_k_patterns(self, k):
		return utils.permutations(k)

	#Return the critical points from the nearest neighbor simulation
	def critical_points(self):
		return analytics.compute_critical(self.create_k_patterns(100))

	def check_significant(self, s, l, X):
		return analytics.check_significant(s,l, X)
	
	
	##################
	##A8 Begins Here##
	##################
	
	#utilize a scipy.spatial.KDTree to compute the nearest neighbor distance
	def nearest_neighbor_KD(self, mark=None):
		currentPoints = []

		if mark is None:
			currentPoints = self.points
		else:
			for p in self.points:
				if p.mark is mark:
					currentPoints.append(p)

		courdinates = []		
		for p in currentPoints:
			courdinates.append((p.x, p.y))
			
		kdtree = ss.KDTree(courdinates)

		nnDistance = []		
		for p in courdinates:
			nearest_neighbor_distance, nearest_neighbor = kdtree.query(p, k=2)
			nnDistance.append(nearest_neighbor_distance)
			
		return np.mean(nnDistance)
			

	#compute the nearest neighbor distance using numpy (ndarray and mean)
	def nearest_neighbot_numpy(self, mark=None):
		pList = []
		points = self.points
		for p in points:
			pList.append(p.array())
			
		
		nd_array = np.ndarray(pList)
		dist = []
		
		temp = None
		
		for i, p1 in enumerate(nd_array):
			for j, p2 in enumerate(nd_array):
				if i==j:
					continue
				d = ss.distance.euclidean(p1, p2)
				
				if temp is None:
					temp= d
				elif temp > d:
					temp = d
					
			dist.append(temp)
			
		return np.mean(dist)
	
	#compute the G function using numpy
	#Add the ability to compute a G function on the point pattern class (more below).
	def compute_g(self, nsteps):
		ds = np.linspace(0, 100, nsteps)
		#nsteps is the number of discrete d that are used to compute G
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
			g_sum = g_sum + min_dis
		return g_sum / nsteps
	
	
	#Generate random points within some domain (you have this 99% coded already). If the domain is not speficied use (0,1). If it is specified (as will be the case when you use the New Haven example), set the domain using the points MBR.
	def np_gen_random_points(self, n = None, nlow = 0, nhi = 1, marks = []):
		points = []
		
		randList = np.random.uniform(nlow, nhi, (n,2))
		
		for x in range(n):
			if len(marks) != 0:
				points.append(Point(randList[x][0], randList[x][1],random.choice(marks)))
			else:
				points.append(Point(randList[x][0], randList[x][1]))
		
		
		return points
			
	

	