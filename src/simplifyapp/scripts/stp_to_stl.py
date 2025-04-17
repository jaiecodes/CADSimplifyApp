# src/simplifyapp/scripts/stp_to_stl.py

import sys
import os

try:
    import FreeCAD as App
    import Part
    import Mesh
except Exception as e:
    print("Failed to import FreeCAD modules:", e, flush=True)
    sys.exit(1)

if len(sys.argv) < 4:
    print("Too few arguments. Usage: freecadcmd script.py model_path export_dir")
    sys.exit(1)

model_path = sys.argv[2]
export_dir = sys.argv[3]

print(f"[FreeCAD] Input file: {model_path}", flush=True)
print(f"[FreeCAD] Output dir: {export_dir}", flush=True)

shape = Part.Shape()
shape.read(model_path)

doc = App.newDocument('Doc')
pf = doc.addObject("Part::Feature","TempShape")
pf.Shape = shape

file_name = os.path.splitext(os.path.basename(model_path))[0]
output_path = os.path.join(export_dir, f"{file_name}.stl")

Mesh.export([pf], output_path)
print(f"[FreeCAD] Exported to: {output_path}", flush=True)
print(output_path, flush=True)
