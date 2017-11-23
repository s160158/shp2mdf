#!/usr/bin/env python

from osgeo import ogr
from mdf import Mdf, MdfPoint

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
            # print 'Point: ({}, {})'.format(geom.GetPoint(i)[0], geom.GetPoint(i)[1])
            p = MdfPoint(geom.GetPoint(i)[0], geom.GetPoint(i)[1], 0, 0, 0)
            mdf_roads.add_point(p)
            # mdf_roads.arc_add_vertex() # remove this shit
        # print 'adding: {}'.format(str(mdf_roads.arc))

        mdf_roads.end_arc()
        print 'post %s' % str(mdf_roads.arc.vertices)

    mdf_roads.save('./test/roads.mdf')

if __name__=='__main__':
    #read_line('./test/test_line.shp')
    #shp2mdf_line('./test/VEJKANT_UDSNIT.shp')
    #shp2mdf_line('./test/VEJKANT_UDSNIT_2_DISCONNECTED.shp')
    #shp2mdf_line('./test/VEJKANT_UDSNIT_CONNECTED.shp')
    shp2mdf_line('./test/VEJKANT_UDSNIT_CLOSED.shp')
