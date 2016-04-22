import unittest

from ..point_pattern import PointPattern
from ..point import Point


class TestPointPattern(unittest.TestCase):
    def setUp(self):
        self.point_pattern = PointPattern()
        self.point_pattern.add_point(Point(5, 6, color='red'))
        self.point_pattern.add_point(Point(6, 5, color='orange'))
        self.point_pattern.add_point(Point(5, 6, color='orange'))
        self.point_pattern.add_point(Point(5, 6))

    def test_coincident(self):
        self.assertEqual(self.point_pattern.count_coincident(), 3)

    def test_list_marks(self):
        self.assertEqual(self.point_pattern.list_marks(), ['red', 'orange'])

    def test_find_subset_with_mark(self):
        self.assertEqual(len(self.point_pattern.find_subset_with_mark('orange')), 2)
        self.assertEqual(len(self.point_pattern.find_subset_with_mark('red')), 1)

    def test_generate_random(self):
        # First test does not pass in n, making n = length of current point pattern.
        self.assertEqual(len(self.point_pattern.generate_random_points()), 4)
        # Second test explicitly passes in n.
        self.assertEqual(len(self.point_pattern.generate_random_points(10)), 10)

    def test_generate_realizations(self):
        self.assertEqual(len(self.point_pattern.generate_realizations(100)), 100)

    def test_compute_g(self):
        self.assertAlmostEqual(self.point_pattern.compute_g(10), 0.111, places=3)
        self.assertAlmostEqual(self.point_pattern.compute_g(50), 0.020, places=3)
        self.assertAlmostEqual(self.point_pattern.compute_g(100), 0.010, places=3)
        self.assertAlmostEqual(self.point_pattern.compute_g(1000), 0.001, places=3)

    def test_nearest_neighbor(self):
        # Test the KDTree implementation against the original implementation.
        self.assertEqual(
            self.point_pattern.average_nearest_neighbor_distance_kdtree(),
            self.point_pattern.average_nearest_neighbor_distance())
        self.assertAlmostEqual(self.point_pattern.average_nearest_neighbor_distance_kdtree(), 0.354, places=3)
        self.assertAlmostEqual(self.point_pattern.average_nearest_neighbor_distance_numpy(), 0.354, places=3)

    def test_generate_random(self):
        points_list = []
        marks_list = []
        for point in self.point_pattern.generate_random_points(count = 3, seed = 1234):
            points_list.append(point.get_array())
            marks_list.append(point.mark['color'])
        self.assertAlmostEqual(points_list[0][0], 0.19, places=2)
        self.assertAlmostEqual(points_list[0][1], 0.62, places=2)
        self.assertAlmostEqual(points_list[1][0], 0.44, places=2)
        self.assertAlmostEqual(points_list[1][1], 0.79, places=2)
        self.assertAlmostEqual(points_list[2][0], 0.78, places=2)
        self.assertAlmostEqual(points_list[2][1], 0.27, places=2)
        self.assertEqual(marks_list, ['violet', 'green', 'red'])
