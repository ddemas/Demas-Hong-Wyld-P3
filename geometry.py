class Point():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        string = str(self.id) + ": (" + str(self.x) + "," + str(self.y) + ")"
        return string

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 1000 + self.y

class Line():
    def __init__(self, point1, point2):
        self.id = id
        self.point1 = point1
        self.point2 = point2

        if point1.x == point2.x:
            self.slope = float('inf')
        else:
            self.slope = (point1.y - point2.y) / (point1.x - point2.x)

    def __str__(self):
        return str(self.point1) + ", " + str(self.point2)

    def __eq__(self, other):
        return (self.point1 == other.point1 and self.point2 == other.point2) or \
               (self.point1 == other.point2 and self.point2 == other.point1)

    def __hash__(self):
        return hash(self.point1) * 1000000 + hash(self.point2)

    def set_id(self, id):
        self.id = id

    def has_any(self, points):
        '''
        Return true if the line touches any of the given points
        '''
        return self.point1 in points or self.point2 in points

    def not_point(self, point):
        '''
        Returns the point on this line that is not the given point
        '''
        if self.point1 == point:
            return self.point2
        else:
            return self.point1

class Circle():
    def __init__(self, center, radius, points):
        self.center = center
        self.radius = radius
        self.points = points
        self.id = None

class Quadrilateral():
    def __init__(self, points):
        self.points = points