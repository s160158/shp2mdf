#!/usr/bin/env python

# MIKE can't load the files when they become to large?
from osgeo import ogr
from mdf import Mdf, MdfPoint, MdfArc, MdfPolygon

def read_line(shpin):
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)


    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        for i in range(0, geom.GetPointCount()):
            print 'Point: ({}, {})'.format(geom.GetPoint(i)[0], geom.GetPoint(i)[1])


def shp2mdf_line(shpin):
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)

    mdf_roads = Mdf()

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        print 'pre %s' % str(mdf_roads.arc.vertices)
        mdf_roads.start_arc()

        for i in range(0, geom.GetPointCount()):
            p = MdfPoint(geom.GetPoint(i)[0], geom.GetPoint(i)[1], 0, 0, 0)
            mdf_roads.add_point(p)

        mdf_roads.end_arc()
        print 'post %s' % str(mdf_roads.arc.vertices)

    mdf_roads.save('./test/roads.mdf')

def read_poly(shpin):
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)


    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        geom = feat.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        for i in range(0, ring.GetPointCount()):
                print ''.join([str(ring.GetPoint(i)[0]), ' ', str(ring.GetPoint(i)[1]), ' ', '1\n'])


def shp2mdf_poly(shpin):
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)

    mdf_roads = Mdf()

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())

        print 'pre %s' % str(mdf_roads.arc.vertices)
        mdf_roads.start_arc()

        geom = feat.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        for i in range(0, ring.GetPointCount()):
            print ''.join([str(ring.GetPoint(i)[0]), ' ', str(ring.GetPoint(i)[1]), ' ', '1\n'])
            p = MdfPoint(ring.GetPoint(i)[0], ring.GetPoint(i)[1], 0, 0, 0)
            mdf_roads.add_point(p)

        mdf_roads.end_arc()

        poly = MdfPolygon('poly1', 0, 0, len(mdf_roads.arcs) - 1, len(mdf_roads.arcs) - 1)
        cen = mdf_roads.get_centroid(poly)
        print cen
        poly.x = cen[0]
        poly.y = cen[1]
        mdf_roads.add_polygon(poly)

        print 'post %s' % str(mdf_roads.arc.vertices)

    mdf_roads.save('./test/buildings.mdf')



if __name__=='__main__':
    # Test line:
    #read_line('./test/test_line.shp')
    #shp2mdf_line('./test/VEJKANT_UDSNIT.shp')
    #shp2mdf_line('./test/VEJKANT_UDSNIT_2_DISCONNECTED.shp')
    #shp2mdf_line('./test/VEJKANT_UDSNIT_CONNECTED.shp')
    #shp2mdf_line('./test/VEJKANT_UDSNIT_CLOSED.shp')

    # Test polygon:
    #read_poly('./test/BYGNING_UDSNIT.shp')
    shp2mdf_poly('./test/BYGNING_SINGLE.shp')
    #shp2mdf_poly('./test/BYGNING.shp')