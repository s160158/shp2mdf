# shp2mdf?
Conversion of .shp to .mdf to be used with MIKE Zero Mesh Generator. Can currently only convert from single file to single file. See shp2mdf.py for an example of how to convert a point, line, and a polygon type shapefile.
The VEJKANT.shp and BYGNING.shp in /test/ is real data from Denmark from the danish map supplier. It contains road edges(line type) and building footprints(polygon type) respectively. POINT.shp just contains points randomly placed.

# The .mdf filetype
Sparse information about this filetype exists. Code is partly based on reverse engineering. (link)

# Notice
The Mesh Generator can be problematic to work with. If a shapefile has overlapping polygons, polygons sharing edges, or possibly other characteristics, then it might not work. Beware.

# Todo
- Class initialisers need checks (many things can go wrong!) raise errors : e.g., raise ValueError("fdlafladl") - maybe fewer tests? simpler code (as simple as possible)
- how do the colors and border thickness values look like? ("hard-code" some sensible default ones) (probably 24 bit color values - or something)
- make header function
- make it accept some field values? which? whY?

header sample:

// Created     : 2017-11-23 9:8:28
// DLL id      : C:\Program Files (x86)\DHI\2016\bin\x64\pfs2004.dll
// PFS version : Nov 16 2016 19:57:46

(not required)

