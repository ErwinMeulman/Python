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

__doc__ = 'Activates selection tool that picks only Model elements.'

__window__.Close()
from Autodesk.Revit.DB import ElementId
from Autodesk.Revit.UI.Selection import ISelectionFilter
from System.Collections.Generic import List

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


class MassSelectionFilter(ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
        if not element.ViewSpecific:
            return True
        else:
            return False

    # standard API override function
    def AllowReference(self, refer, point):
        return False


try:
    sel = MassSelectionFilter()
    sellist = uidoc.Selection.PickElementsByRectangle(sel)

    filteredlist = []
    for el in sellist:
        filteredlist.append(el.Id)

    uidoc.Selection.SetElementIds(List[ElementId](filteredlist))
    uidoc.RefreshActiveView()
except:
    pass