# shp2mdf?
Conversion of .shp to .mdf to be used with MIKE Zero Mesh Generator. Can currently only convert from single file to single file. See shp2mdf.py for an example of how to convert a point, line, and a polygon type ESRI Shapefile.
The VEJKANT.shp and BYGNING.shp in ./test/ is real data from Denmark provided by the danish map supplier. It contains road edges(line type) and building footprints(polygon type), respectively. POINT.shp contains points randomly placed in the same area as the previous two test files.

# The .mdf filetype
Sparse information about this filetype exists. Code is partly based on reverse engineering. The program is based on the least possible amount of information required to create .mdf files and is very limited in terms of supported functionality.

# Notice
The Mesh Generator can be problematic to work with. If a shapefile has overlapping polygons, polygons sharing edges, or possibly other characteristics, then MIKE Mesh Generator might not be able to load the file. Beware.

# Todo
- Class initialisers need checks (many things can go wrong!) raise errors : e.g., raise ValueError("fdlafladl") - maybe fewer tests? simpler code (as simple as possible)
Simplest code! refactore code and remove all unused lines, make it easier to read
- how do the colors and border thickness values look like? ("hard-code" some sensible default ones) (probably 24 bit color values - or something)
- make header function

header sample:

// Created     : 2017-11-23 9:8:28
// DLL id      : C:\Program Files (x86)\DHI\2016\bin\x64\pfs2004.dll
// PFS version : Nov 16 2016 19:57:46

(not required)

- What is Curve object in template?

-change the data area to be bounding box of input features

   [DATA_AREA]
      x0 = 495000
      y0 = -2500
      x1 = 505000
      y1 = 2500

