#!/usr/bin/env python

from osgeo import ogr

def point_inside_poly(x, y, geom):
    """
    Check if a point given by a x- and y-coordinate is within a polygon.
    :param x: x-coordinate (usually UTM coordinate)
    :param y: y-coordinate (..)
    :param geom: ogr geometry object of the polygon
    :return: Boolean
    """
    ring = geom.GetGeometryRef(0)
    poly = []
    for i in range(0, ring.GetPointCount()):
        poly.append((ring.GetPoint(i)[0], ring.GetPoint(i)[1]))

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def three_point_centroid(geom):
    """
    Return the centroid of the first three points found in polygon if their centroid is within the polygon.
    :param geom: ogr geometry object of polygon
    :return:
    """
    ring = geom.GetGeometryRef(0)
    poly = []
    for i in range(0, ring.GetPointCount()):
        poly.append((ring.GetPoint(i)[0], ring.GetPoint(i)[1]))

    n = len(poly)

    for i in range(0, n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                x = (poly[i][0] + poly[j][0] + poly[k][0] ) / 3
                y = (poly[i][1] + poly[j][1] + poly[k][1] ) / 3
                if point_inside_poly(x, y, geom):
                    return (x, y)
        raise ValueError('Could not find a suitable centroid!')