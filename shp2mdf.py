#!/usr/bin/env python

from osgeo import ogr

def read_line(shpin):
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print 'found %d number of features!' % len(shp_lyr)

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print 'number of points: {}'.format(geom.GetPointCount())
        for i in range(0, geom.GetPointCount()):
            print 'Point: ({}, {})'.format(geom.GetPoint(i)[0], geom.GetPoint(i)[1])

if __name__=='__main__':

    read_line('./test/VEJKANT.shp')