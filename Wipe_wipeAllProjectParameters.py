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

__doc__ = 'This tool tries to remove all cutom project parameters in the file but sometimes fails.'

import clr
from Autodesk.Revit.DB import InstanceBinding, TypeBinding, FilteredElementCollector, Transaction, ElementId

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

pm = doc.ParameterBindings
it = pm.ForwardIterator()
it.Reset()

deflist = []
paramidlist = set()
while it.MoveNext():
    p = it.Key
    b = pm[p]

    if isinstance(b, InstanceBinding):
        bind = 'Instance'
    elif isinstance(b, TypeBinding):
        bind = 'Type'
    else:
        bind = 'Uknown'

    print('\n')
    print('-' * 100)
    print('PARAM: {0:<30} UNIT: {1:<10} TYPE: {2:<10} GROUP: {3:<20} BINDING: {4:<10} VISIBLE: {6}\n'
          'APPLIED TO: {5}\n'.format(p.Name,
                                     str(p.UnitType),
                                     str(p.ParameterType),
                                     str(p.ParameterGroup),
                                     bind,
                                     [cat.Name for cat in b.Categories],
                                     p.Visible
                                     ))
    deflist.append(p)

    for cat in b.Categories:
        try:
            elements = FilteredElementCollector(doc).OfCategoryId(cat.Id).WhereElementIsNotElementType()
            if bind == 'Type' and p.Visible:
                elementTypes = FilteredElementCollector(doc).OfCategoryId(cat.Id).WhereElementIsElementType()
                print('Searching through {0} ElementTypes of Category {1}'.format(len(list(elements)), cat.Name))
                for elType in elementTypes:
                    paramidlist.add(elType.LookupParameter(p.Name).Id.IntegerValue)
            elif p.Visible:
                print('Searching through {0} Elements of Category {1}'.format(len(list(elements)), cat.Name))
                for el in elements:
                    paramidlist.add(el.LookupParameter(p.Name).Id.IntegerValue)
        except Exception as e:
            print('---ERROR---\n', p.Name, cat.Name, cat.Id, e)
            continue

t = Transaction(doc, 'Remove all project parameters')
t.Start()

for pid in paramidlist:
    try:
        doc.Delete(ElementId(pid))
    except Exception as e:
        print(pid, e)
        continue

for p in deflist:
    pm.Remove(p)

t.Commit()
