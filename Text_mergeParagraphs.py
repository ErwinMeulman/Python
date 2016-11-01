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

__doc__ = 'Removes the space and newlines between paragraphs in the selected text note element.'

__window__.Close()
from Autodesk.Revit.DB import Transaction

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

t = Transaction(doc, 'Merge Single-Line Text')
t.Start()

selection = [doc.GetElement(elId) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds()]
tnotes = sorted(selection, key=lambda txnote: 0 - txnote.Coord.Y)

mtxt = tnotes[0]
mtxtwidth = mtxt.Width
for txt in tnotes[1:]:
    if txt.Text[0] == '\r\n\r\n':
        mtxt.Text = mtxt.Text + txt.Text
    else:
        mtxt.Text = mtxt.Text + '\r\n\r\n' + txt.Text
    doc.Delete(txt.Id)

mtxt.Width = mtxtwidth
t.Commit()
