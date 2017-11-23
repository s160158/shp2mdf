#!/usr/bin/env python

"""
TODO:
- Class initialisers need checks (many things can go wrong!) raise errors : e.g., raise ValueError("fdlafladl")
- polygon default x, y to 0, 0. Not needed. can be generated as a centroid from its defining points when attached to an Mdf instance
- how do the colors and border thickness values look like? ("hard-code" some sensible default ones)
- make header function
- number of whitespaces does no difference

header sample:

// Created     : 2017-11-23 9:8:28
// DLL id      : C:\Program Files (x86)\DHI\2016\bin\x64\pfs2004.dll
// PFS version : Nov 16 2016 19:57:46

(not required)

"""

class MdfPoint:
    x = 0; y = 0
    attr1 = 0; attr2 = 0

    isNode = 0
    def __init__(self, x, y, attr1 = 0, attr2 = 0, isNode = 0):
        self.x = x
        self.y = y
        self.attr1 = attr1
        self.attr2 = attr2
        if isNode:
            self.isNode = True
        else:
            self.isNode = False

    def __str__(self):
        return 'MdfPoint: (x, y) = ({}, {}), attr1 = {}, attr2 = {}, isNode : {}'.format(self.x, self.y, self.attr1,
                                                                                         self.attr2, self.isNode)

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.x, self.y, self.attr1, self.attr2, int(self.isNode))


class MdfArc:  # desirable to make the class more loose and allow user to not define start and end (empty arcs)?
    vertices = []
    startNode = -1
    endNode = -1
    attr = 0

    def __init__(self, vertices = [], start_node = -1, end_node = -1, attr = 0):
        self.vertices = vertices
        self.startNode = start_node
        self.endNode = end_node
        self.attr = attr

    def set_start_node(self):
        pass

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

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

    def __init__(self, name, x, y, start_arc, end_arc, arcs = [], mesh_code = 1):  # Polygon can be formed by a single arc (give points)
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


class Mdf:
    points = []
    arcs = []
    polygons = []

    def __init__(self):
        pass

    def add_point(self, point):
        if point.__class__.__name__ == 'MdfPoint':
            if self.drawing_arc and self.arc.startNode == -1:
                point.isNode = True
                self.arc.startNode = len(self.points) # point not yet appended
                print 'adding node: %d ' % len(self.points)
            elif self.drawing_arc and self.arc.startNode != -1:
                point.isNode = False
                self.arc.add_vertex(len(self.points))
                print 'adding vertex: %d' % len(self.points)
            self.points.append(point)
        else:
            raise ValueError('not a MdfPoint object')

    def add_arc(self, arc):
        if arc.__class__.__name__ == 'MdfArc':
            self.arcs.append(arc)
        else:
            raise ValueError('not a MdfArc object')

    arc = MdfArc()
    drawing_arc = False
    def start_arc(self):
        if self.drawing_arc:
            raise ValueError('already drawing arc, please call .end_arc()')
        else:
            self.arc = MdfArc([], -1, -1, 0)
            self.drawing_arc = True

    def end_arc(self):
        if self.drawing_arc:
            self.arc.endNode = self.arc.vertices[-1] # Last point in vertices is end node
            print self.arc.vertices
            print self.arc.vertices[-1]
            print self.arc.endNode
            self.arc.vertices.pop() # No longer a vertex, is a node so remove it
            self.points[-1].isNode = True # Must be node (an arc ends point)
            self.arcs.append(self.arc)
            print 'added arc: {}'.format(str(self.arc))
            self.drawing_arc = False
            self.arc = MdfArc([], -1, -1, 0)
            print self.arc
        else:
            raise ValueError('ending arc before starting it, please call .start_arc()')

    def add_polygon(self, polygon):
        if polygon.__class__.__name__ == 'MdfPolygon':
            self.polygons.append(polygon)
        else:
            raise ValueError('not a MdfPolygon object')

    def get_centroid(self, MdfType): # what if startArc == endArc problem ...? only one arc in polygon
        if MdfType.__class__.__name__ == 'MdfPolygon':
            arcs = MdfType.arcs
            arcs.append(MdfType.startArc)
            arcs.append(MdfType.endArc)
            print arcs
            n = 0
            centroid_x = 0
            centroid_y = 0
            for arc in arcs:
                print arcs[arc]
                print self.arcs[arc].vertices
                for i in self.arcs[arc].vertices:
                    print self.points[i]
                    n += 1
                centroid_x += self.points[self.arcs[arc].startNode].x
                centroid_x += self.points[self.arcs[arc].endNode].x
                centroid_y += self.points[self.arcs[arc].startNode].y
                centroid_y += self.points[self.arcs[arc].endNode].y
                n += 2
        centroid_x = centroid_x / n
        centroid_y = centroid_y / n
        return (centroid_x, centroid_y)

    def _nrepr(self, lst):
        # MDF requires that each element is marked with a number. This methods adds the index number of list element
        # in front
        line = ''
        for i in range(0, len(lst)):
            line += '{} {} '.format(str(i), repr(lst[i]))  # Adds index number to join
        return line

    def __repr__(self):
        # A string representation the Mike Mesh Generator can understand
        mdf = ''
        # Points
        mdf += """
[POINTS]
    Data = '{} {}'
EndSect // POINTS""".format(len(self.points), self._nrepr(self.points))
        # Arcs
        mdf += """
[ARCS]
    Data = '{} {}'
EndSect // ARCS""".format(len(self.arcs), self._nrepr(self.arcs))
        # Polygons
        mdf += """
[POLYGONS]
    Data = '{} {}'
EndSect // POLYGONS""".format(len(self.polygons), ' '.join(map(repr, self.polygons)))

        return self.stitch_3parts(mdf)

    def stitch_3parts(self, mid):
        # Stitching MDF together. Consisting of top, mid, and bot. top and bot are given in ./template. mid must be
        # input as a string. The middle part mid is the generated POINTS, ARCS, POLYGONS
        mdf = ''

        fh_top = open('./template/top.txt', 'r')  # top part of MDF

        for line in fh_top:
            mdf += line

        fh_top.close()

        mdf += mid  # middle part of MDF (the part this class is used to generate)

        fh_bot = open('./template/bot.txt', 'r') # the bottom part of MDF

        for line in fh_bot:
            mdf += line

        fh_bot.close()

        return mdf

    def save(self, filename):
        fh = open(filename, 'w')
        fh.write(self.__repr__())
        fh.close()

if __name__=='__main__':
    # cornerbox example: (including polygon)
    mdf1 = Mdf()

    p1 = MdfPoint(722600, 6184020, 0, 0, 1)
    mdf1.add_point(p1)
    p1 = MdfPoint(722600, 6184300, 0, 0, 1)
    mdf1.add_point(p1)
    p1 = MdfPoint(722880, 6184020, 0, 0, 1)
    mdf1.add_point(p1)
    p1 = MdfPoint(722880, 6184300, 0, 0, 1)
    mdf1.add_point(p1)

    a1 = MdfArc([], 1, 0)
    mdf1.add_arc(a1)
    a2 = MdfArc([], 0, 2)
    mdf1.add_arc(a2)
    a3 = MdfArc([], 2, 3)
    mdf1.add_arc(a3)
    a3 = MdfArc([], 3, 1)
    mdf1.add_arc(a3)

    h1 = MdfPolygon('poly1', 722706, 6184140, 0, 2, [1, 3])
    cen = mdf1.get_centroid(h1)
    print cen
    h1.x = cen[0]
    h1.y = cen[1]
    mdf1.add_polygon(h1)

    print h1.arcs


    #print repr(mdf1)
    mdf1.save('./test/t1.mdf')

    # line example:

