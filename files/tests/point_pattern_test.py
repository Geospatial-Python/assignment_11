import unittest
from ..point_pattern import PointPattern
from ..point import Point


class TestPointPattern(unittest.TestCase):
    def setUp(self):
        self.point_pattern = PointPattern()
        self.point_pattern.add_point(point.Point(1,1, 'Blue'))
        self.point_pattern.add_point(point.Point(2,2, 'Rare'))
        self.point_pattern.add_point(point.Point(3,3, 'Medium-Rare'))
        self.point_pattern.add_point(point.Point(4,4, 'Medium'))
        self.point_pattern.add_point(point.Point(5,5, 'Medium-Well'))
        self.point_pattern.add_point(point.Point(6,6, 'Well-Done'))
        self.point_pattern.add_point(point.Point(1,1,))

    def test_coincident(self):
        self.assertEqual(self.point_pattern.number_of_coincident(), 3)

    def test_list_marks(self):
        self.assertEqual(self.point_pattern.list_marks(), ['Blue', 'Rare', 'Medium-Rare', 'Medium', 'Medium-Well', 'Well-Done'])

    def test_subsets_with_mark(self):
        self.assertEqual(len(self.point_pattern.subsets_with_mark()))