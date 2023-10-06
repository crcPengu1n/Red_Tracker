import math

class Slope:
    def __init__(self, slope, point1, point2):
        self.slope = slope
        self.point1 = point1
        self.point2 = point2

    def calculate_distance(self):
        x1, y1 = self.point1
        x2, y2 = self.point2
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance

    def __str__(self):
        return f"Slope: {self.slope}, Point 1: {self.point1}, Point 2: {self.point2}, Distance: {self.calculate_distance()}"