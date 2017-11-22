#!/usr/bin/env python

"""
TODO:
- Class initialisers need checks (many things can go wrong!) raise errors : e.g., raise ValueError("A polygon most have at least 3 arcs!")
- polygon default x, y to 0, 0. Not needed. can be generated as a centroid from its defining points when attached to an Mdf instance
- how do the colors and border thickness values look like? ("hard-code" some sensible default ones)

"""


class Mdf:
    points = []
    arcs = []
    polygons = []

    def __init__(self):
        pass

    def add_point(self, point):
        if point.__class__.__name__ == 'MdfPoint':
            self.points.append(point)
            return 0
        else:
            return 1

    def add_arc(self, arc):
        if arc.__class__.__name__ == 'MdfArc':
            self.arcs.append(arc)
            return 0
        else:
            return 1

    def add_polygon(self, polygon):
        if polygon.__class__.__name__ == 'MdfPolygon':
            self.polygons.append(polygon)
            return 0
        else:
            return 1

    def _nrepr(self, lst):
        line = ''
        for i in range(0, len(lst)):
            line += '{} {} '.format(str(i), repr(lst[i]))  # Adds index number to join
        return line

    def __repr__(self):
        mdf = ''
        # Points
        mdf += """
[POINTS]
    Data = '{} {}'
EndSect // Points""".format(len(self.points), self._nrepr(self.points))
        # Arcs
        mdf += """
[ARCS]
    Data = '{} {}'
EndSect // Arcs""".format(len(self.arcs), self._nrepr(self.arcs))
        # Polygons
        mdf += """
[POLYGONS]
    Data = '{}'
EndSect // Polygons""".format(' '.join(map(repr, self.polygons)))

        return mdf

    def save(self, filename):
        fh = open(filename, 'w')
        fh.write(self.__repr__())
        fh.close()


class MdfPoint:
    def __init__(self, x, y, attr1 = 0, attr2 = 0):
        self.x = x
        self.y = y
        self.attr1 = attr1
        self.attr2 = attr2
        self.isNode = False

    def __str__(self):
        return 'MdfPoint: (x, y) = ({}, {}), attr1 = {}, attr2 = {}, isNode : {}'.format(self.x, self.y, self.attr1,
                                                                                         self.attr2, self.isNode)

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.x, self.y, self.attr1, self.attr2, int(self.isNode))


class MdfArc:
    def __init__(self, vertices, start_node = -1, end_node = -1, attr = 0):
        if start_node == end_node == -1 and len(vertices) > 1:  # Not defined, take start/end nodes from vertices
            self.vertices = vertices
            self.startNode = vertices[0]
            self.endNode = vertices[-1]
            self.vertices.pop(0)
            self.vertices.pop(-1)
        elif (start_node != -1 and end_node == -1) or (start_node == -1 and end_node != -1):
            return  # No object should be created
        elif start_node == end_node == -1 and len(vertices) < 2:  # At least two points needed to define an arc
            return  # No object should be created
        else:
            self.vertices = vertices
            self.startNode = start_node
            self.endNode = end_node
        self.attr = attr

    def __str__(self):
        return '{}, {}, {}, attr : {}'.format(self.startNode, str(self.vertices), self.endNode, self.attr)

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.startNode, self.endNode, len(self.vertices),
                                       ' '.join(map(str, self.vertices)), self.attr)  # Mapping list of integers to
                                                                                      # list of strings


class MdfPolygon:

    # Default values:
    visuals = [0, 0, 1]  # Fill color, border color, and border thickness
    localMin = 1
    maxArea = 100
    res = (1, 1)  # Resolution eta and xi
    unknowns = '0 0 0 0 0 1 1000 2 2 0 10'
    method = 0  # Quadrilateral mesh generation method. 0: algebraic, 1: transfinite

    def __init__(self, name, x, y, start_arc, end_arc, arcs = [], mesh_code = 1):  # A polygon needs at least 3 arcs! So arcs can't be empty
        self.name = name
        self.nLetters = len(name)
        self.x = x
        self.y = y
        self.startArc = start_arc
        self.endArc = end_arc
        self.arcs = arcs
        self.nArcs = len(arcs)
        self.meshCode = mesh_code

    def __str__(self):
        return 'MdfPolygon: name = {}, x = {}, y = {}, mesh_code = {}'.format(self.name, self.x, self.y, self.meshCode)

    def __repr__(self):
        arcs = ' '.join(map(str, self.arcs))
        return ' '.join(map(str, [self.nLetters, self.name, self.x, self.y, self.meshCode, 0, self.startArc,
                                  self.endArc, self.visuals[0], self.visuals[1], self.visuals[2], self.localMin,
                                  self.maxArea, self.method, 0, self.res[0], self.res[1], self.unknowns,
                                  self.nArcs, arcs]))


if __name__=='__main__':
    mdf1 = Mdf()

    p1 = MdfPoint(3, 4, 100, 0)
    mdf1.add_point(p1)
    p2 = MdfPoint(5, 6, 100, 0)
    mdf1.add_point(p2)
    p3 = MdfPoint(3, 7, 100, 0)
    mdf1.add_point(p3)


    a1 = MdfArc([], 0, 1)
    mdf1.add_arc(a1)
    a2 = MdfArc([], 1, 2)
    mdf1.add_arc(a2)
    a3 = MdfArc([], 2, 0)
    mdf1.add_arc(a3)

    h1 = MdfPolygon('poly1', 5, 5, 0, 2, [1])
    mdf1.add_polygon(h1)

    # Check
    print repr(mdf1)
    mdf1.save('./test/t1.mdf')
