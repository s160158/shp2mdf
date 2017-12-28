#!/usr/bin/env python

# MIKE can't load the files when they become to large?
from osgeo import ogr
from mdf import Mdf, MdfPoint, MdfArc, MdfPolygon

def read_line(shp):
    shp_ds = ogr.Open(shp)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)


    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        for i in range(0, geom.GetPointCount()):
            print 'Point: ({}, {})'.format(geom.GetPoint(i)[0], geom.GetPoint(i)[1])


def shp2mdf_line(shp):
    shp_ds = ogr.Open(shp)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)

    mdf_object = Mdf()

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        print 'pre %s' % str(mdf_object.arc.vertices)
        mdf_object.start_arc()

        for i in range(0, geom.GetPointCount()):
            p = MdfPoint(geom.GetPoint(i)[0], geom.GetPoint(i)[1], 0, 0, 0)
            mdf_object.add_point(p)

        mdf_object.end_arc()
        print 'post %s' % str(mdf_object.arc.vertices)

    mdf = shp.split('/')[-1].split('.')[0] + '.mdf'
    mdf_object.save('./test/' + mdf)


def read_poly(shp):
    shp_ds = ogr.Open(shp)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)


    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        geom = feat.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        for i in range(0, ring.GetPointCount()):
                print ''.join([str(ring.GetPoint(i)[0]), ' ', str(ring.GetPoint(i)[1]), ' ', '1\n'])


def shp2mdf_poly(shp):
    shp_ds = ogr.Open(shp)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)

    mdf_object = Mdf()

    id = 1

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        print 'pre %s' % str(mdf_object.arc.vertices)
        mdf_object.start_arc()

        geom = feat.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        for i in range(0, ring.GetPointCount()):
            print ''.join([str(ring.GetPoint(i)[0]), ' ', str(ring.GetPoint(i)[1]), ' ', '1\n'])
            p = MdfPoint(ring.GetPoint(i)[0], ring.GetPoint(i)[1], 0, 0, 0)
            mdf_object.add_point(p)

        mdf_object.end_arc()

        poly = MdfPolygon('poly' + str(id), 0, 0, len(mdf_object.arcs) - 1, len(mdf_object.arcs) - 1)
         # need no necessarily be inside of the polygon if it is non-convex(concave)
        poly.x = geom.Centroid().GetX()
        poly.y = geom.Centroid().GetY()

        if not point_inside_poly(poly.x, poly.y, geom): #prefer centroid if inside polygon!
            poly.x, poly.y = three_point_centroid(geom)
            print 'Polygon defintion point: ({}, {})'.format(poly.x, poly.y)

        mdf_object.add_polygon(poly)

        print 'post %s' % str(mdf_object.arc.vertices)
        id += 1

    mdf = shp.split('/')[-1].split('.')[0] + '.mdf'
    mdf_object.save('./test/' + mdf)

def point_inside_poly(x, y, geom):
    #geom is a polygon geometry object
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
    #iterates over points in polygon and returns the triangel with centroid within the polygon
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

if __name__=='__main__':
    # Test line:
    #shp2mdf_line('./test/VEJKANT2.shp')

    # Test polygon:
    shp2mdf_poly('./test/BYGNING3.shp')