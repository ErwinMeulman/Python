#python nodes in dynamo 1.0.0
#proposed by Nicklas Østertgaard  nvo@bimshark.com

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)
# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *
# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# Create the Revit Link Type
# creae a for loop
#mp = ModelPathUtils.ConvertUserVisiblePathToModelPath(UnwrapElement(IN[1]))
mp = ModelPathUtils.ConvertUserVisiblePathToModelPath("C:\Dynamo\parkeringspace.rvt")
lnkOp = RevitLinkOptions("")
loadedLnkType = RevitLinkType.Create(doc, mp, lnkOp)
 
# Create the Revit Link Instance
lnkInstance = RevitLinkInstance.Create(doc, loadedLnkType.ElementId)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

OUT="Worked"