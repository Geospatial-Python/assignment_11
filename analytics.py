import random
import math


def p_perms(p=99,n=100,mark=None):
    mean_nn_dist =  []
    for i in range(p):
        temp=create_n_rand_pts(100)
        temp1=average_nearest_neighbor_distance(temp)
        mean_nn_dist.append(temp1);

    return mean_nn_dist

def create_n_rand_pts(n):
    n_pts = [(random.uniform(0,1), random.uniform(0,1)) for i in range(n)]
    return n_pts

def p_perms_marks(p=99,n=100,marks=None):
    marks=['mercury', 'venus', 'earth', 'mars']
    mean_nn_dist =  []
    for i in range(p):
        temp=utils.create_marked_rand_pts(100,marks)
        #print(temp.)
        temp1=average_nearest_neighbor_distance(temp,marks)
        mean_nn_dist.append(temp1)

    return mean_nn_dist

def create_marked_rand_pts(n,marks=None):
    n_pts=[]
    for i in range(n):
        chosen_mark=random.choice(marks)
        temppt=point.Point(random.uniform(0,1), random.uniform(0,1),chosen_mark)
        #print(temppt.x)
        n_pts.append(temppt)
    return n_pts
def monte_carlo_critical_bound_check(lb,ub,obs):
    return obs<lb or obs>ub

def critical_pts(distances):
    return min(distances), max(distances)

def minimum_bounding_rectangle(points):
    xmin=points[1][0]
    ymin=points[1][1]
    xmax=points[1][0]
    ymax=points[1][1]

    for i in points:
        curr_x=i[0]
        curr_y=i[1]
        if curr_x < xmin:
            xmin= curr_x
        elif curr_x > xmax:
            xmax= curr_x

        if curr_y < ymin:
            ymin= curr_y
        elif curr_y > ymax:
            ymax= curr_y
    mbr = [xmin,ymin,xmax,ymax]

    return mbr

def find_largest_city(gj):
    maximum=0;
    features=gj['features']

    for i in features:
        if (i['properties']['pop_max']>maximum):
            maximum=i['properties']['pop_max']
            city=i['properties']['nameascii']
    return city, maximum


def write_your_own(gj):
    features=gj['features']
    count = 0
    for i in features:
        if(' ' in i['properties']['name']):
            count= count+1

    return count

def mean_center(points):
    x_tot=0
    y_tot=0

    for i in points:
        x_tot+=i[0]
        y_tot+=i[1]

    x = x_tot/len(points)
    y = y_tot/len(points)

    return x, y

def average_nearest_neighbor_distance(points,mark=None):
    mean_d = 0

    if(mark==None):
        for i in range(len(points)):
            dist_nearest=math.inf
            for j in range(len(points)):
                temp_p1 = (points[i].x, points[i].y)
                temp_p2 = (points[j].x, points[j].y)
                dist = utils.euclidean_distance(temp_p1, temp_p2)
                if temp_p1 == temp_p2:
                    continue
                elif dist < dist_nearest:
                    dist_nearest = dist;
                    mean_d += dist_nearest;
                    mean_d=mean_d/(len(points))
    else:
        for i in range(len(points)):
            dist_nearest=math.inf
            for j in range(len(points)):
                dist = utils.euclidean_distance((points[i].x, points[i].y), (points[j].x,points[j].y))
                if temp_p1 == temp_p2:
                    continue
                elif dist < dist_nearest and temp_p1==temp_p2:
                    dist_nearest = dist;
                    mean_d += dist_nearest;
                    mean_d=mean_d/(len(points))

    return mean_d


"""
def average_nearest_neighbor_distance_marks(points,mark=None):
    mean_d = 0
    for i in range(len(points)):
        dist_nearest=1e9
        for j in range(len(points)):
            temp_p1 = (points[i].x, points[i].y)
            temp_p2 = (points[j].x, points[j].y)
            dist = utils.euclidean_distance(temp_p1, temp_p2)
            if temp_p1 == temp_p2:
                continue
            elif dist < dist_nearest:
                dist_nearest = dist;
        mean_d += dist_nearest;
    mean_d=mean_d/(len(points))
    return mean_d


def average_nearest_neighbor_distance(points):
    mean_d = 0
    for i in points:
        dist_nearest=1e9
        for j in points:
            dist = utils.euclidean_distance(i, j)
            if i==j:
                continue
            elif dist < dist_nearest:
                dist_nearest = dist;
        mean_d += dist_nearest;
    mean_d=mean_d/(len(points))
    return mean_d
"""
