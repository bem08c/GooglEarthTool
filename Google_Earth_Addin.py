#Created By Benjamin Mittler Updated 6/8/15

import arcpy
import pythonaddins

class Google_Tools(object):
    """Implementation for GoogleTest3_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.

    def onMouseDownMap(self, x, y, button, shift):
        import os
        import arcpy
        import sys
        import functools
        import threading

        
#This is a workaround provided by ESRI, running os.startfile without threading will cause arcmap to crash
        def run_in_other_thread(function):
            @functools.wraps(function)
            def fn_(*args, **kwargs):
                thread = threading.Thread(target=function, args=args, kwargs=kwargs)
                thread.start()
                thread.join()
            return fn_
        arcpy.env.overwriteOutput = True
#Checks to see if folder exists, creates folder if it doesnt exist
        direct = "C:\GoogleEarthPointFolder"
        if not os.path.exists(direct):
            os.makedirs(direct)
#Identifies the Map Document/Dataframe/Spatial Reference of the Dataframe
        mxd=arcpy.mapping.MapDocument("current")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        sr_df = df.spatialReference
#Creates an empty list which will temporarily host the information gained from clicking on the map
        ptgeom = []
        pt = arcpy.Point()
        pt.X = x
        pt.Y = y
#Appends information from click to the list, creating a point with the same spatial reference as the datafram        
        ptgeom.append(arcpy.PointGeometry(pt, sr_df))

#Copies the information from the list to C: folder and creates a shp, this shp will be added to the TOC now
        arcpy.CopyFeatures_management(ptgeom, r"C:\GoogleEarthPointFolder\pt.shp")
#Converts the new shp to a KML
        arcpy.LayerToKML_conversion("pt", "C:\GoogleEarthPointFolder\pt.kmz")
        arcpy.RefreshTOC
#Opens the KML (which will open GoogleEarth if its installed on the machine)
        startfile = run_in_other_thread(os.startfile)
        startfile("C:\GoogleEarthPointFolder\pt.kmz")
    