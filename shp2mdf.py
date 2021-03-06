#!/usr/bin/env python

from osgeo import ogr
from mdf import Mdf, MdfPoint, MdfArc, MdfPolygon
from ogr_helpers import *

def read_point(shp):
    shp_ds = ogr.Open(shp)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)


    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        for i in range(0, geom.GetPointCount()):
            print 'Point: ({}, {})'.format(geom.GetPoint(i)[0], geom.GetPoint(i)[1])


def shp2mdf_point(shp):
    shp_ds = ogr.Open(shp)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)

    mdf_object = Mdf()

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        for i in range(0, geom.GetPointCount()):
            node = 1 #  if 1 a vertex, 0 a node
            p = MdfPoint(geom.GetPoint(i)[0], geom.GetPoint(i)[1], 0, 0, node)
            mdf_object.add_point(p)


    mdf = '/'.join(shp.split('/')[0:-1]) + '/' + ''.join(shp.split('/')[-1].split('.')[0:-1]) + '.mdf'
    mdf_object.save(mdf)



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

        if geom.GetPointCount() > 1:  # 2 or more points to make line

            print 'pre %s' % str(mdf_object.arc.vertices)
            mdf_object.start_arc()

            for i in range(0, geom.GetPointCount()):
                p = MdfPoint(geom.GetPoint(i)[0], geom.GetPoint(i)[1], 0, 0, 0)
                mdf_object.add_point(p)

            mdf_object.end_arc()
            print 'post %s' % str(mdf_object.arc.vertices)

    mdf = '/'.join(shp.split('/')[0:-1]) + '/' + ''.join(shp.split('/')[-1].split('.')[0:-1]) + '.mdf'
    mdf_object.save(mdf)


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
        mdf_object.start_arc()  # Start drawing an arc (a polygon in this case)

        geom = feat.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        for i in range(0, ring.GetPointCount()):
            print ''.join([str(ring.GetPoint(i)[0]), ' ', str(ring.GetPoint(i)[1]), ' ', '1\n'])
            p = MdfPoint(ring.GetPoint(i)[0], ring.GetPoint(i)[1], 0, 0, 0)
            mdf_object.add_point(p)  # Add points to arc

        mdf_object.end_arc()  # End the arc

        # Add polygon definition point
        poly = MdfPolygon('poly' + str(id), 0, 0, len(mdf_object.arcs) - 1, len(mdf_object.arcs) - 1)
        # need no necessarily be inside of the polygon if it is non-convex(concave)
        poly.x = geom.Centroid().GetX()
        poly.y = geom.Centroid().GetY()

        poly.method = 0

        if not point_inside_poly(poly.x, poly.y, geom):  # prefer centroid if inside polygon!
            poly.x, poly.y = three_point_centroid(geom)
            print 'Polygon defintion point: ({}, {})'.format(poly.x, poly.y)

        mdf_object.add_polygon(poly)

        print 'post %s' % str(mdf_object.arc.vertices)
        id += 1

    mdf = '/'.join(shp.split('/')[0:-1]) + '/' + ''.join(shp.split('/')[-1].split('.')[0:-1]) + '.mdf'
    mdf_object.save(mdf)



if __name__=='__main__':
    # Test point:
    #shp2mdf_point('./test/POINT.shp')

    # Test line:
    #read_line('./test/VEJKANT1.shp')
    #shp2mdf_line('./test/VEJKANT.shp')

    # Test polygon:
    shp2mdf_poly('./test/BYGNING.shp')

    #shp2mdf_point('C:/Users/thsu/Desktop/thesis/quad_meshes/mesh_local/box_02816x02816_0.2_2x2_point.shp')
    #shp2mdf_point('C:/Users/thsu/Desktop/thesis/quad_meshes/mesh_regional/box_34672x28512_0.2_16x16_point.shp')


