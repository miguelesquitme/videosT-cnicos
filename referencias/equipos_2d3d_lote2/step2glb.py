import sys
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.RWGltf import RWGltf_CafWriter
from OCP.OCP.collections import IndexedDataMap_TCollection_AsciiString_TCollection_AsciiString as IDM
from OCP.Message import Message_ProgressRange
from OCP.IFSelect import IFSelect_RetDone
inp,out=sys.argv[1],sys.argv[2]; defl=float(sys.argv[3]) if len(sys.argv)>3 else 0.5
doc=TDocStd_Document(TCollection_ExtendedString("doc"))
r=STEPCAFControl_Reader(); r.SetColorMode(True); r.SetNameMode(True)
assert r.ReadFile(inp)==IFSelect_RetDone
r.Transfer(doc)
sh=r.Reader().OneShape()
BRepMesh_IncrementalMesh(sh, defl, False, 0.3, True)
w=RWGltf_CafWriter(TCollection_AsciiString(out), True)
w.Perform(doc, IDM(), Message_ProgressRange())
print('ok',out)
