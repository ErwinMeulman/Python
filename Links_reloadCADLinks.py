"""
Copyright (c) 2014-2016 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

__doc__ = 'Reload all xref CAD links.'

from Autodesk.Revit.DB import ModelPathUtils, TransmissionData, RevitLinkType, ElementType
import clr

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
# selection = [ doc.GetElement( elId ) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds() ]

location = doc.PathName
try:
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(location)
    transData = TransmissionData.ReadTransmissionData(modelPath)
    externalReferences = transData.GetAllExternalFileReferenceIds()
    for refId in externalReferences:
        extRef = transData.GetLastSavedReferenceData(refId)
        if 'CADLink' == str(extRef.ExternalFileReferenceType):
            link = doc.GetElement(refId)
            # link = clr.Convert( link, ElementType )
            path = ModelPathUtils.ConvertModelPathToUserVisiblePath(extRef.GetPath())
            if '' == path:
                path = '--NOT ASSIGNED--'
            print("Reloading...\n{0}{1}".format(str(str(extRef.ExternalFileReferenceType) + ':').ljust(20), path))
            # link.Reload()
            # print('Done\n')
            print('Sorry. Revit API does not have a CADLinkType.Reload method yet')
except:
    print('Model is not saved yet. Can not aquire location.')
