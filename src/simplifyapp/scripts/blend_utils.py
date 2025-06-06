import bpy
import os
import sys

MODIFIER_NAME = "DECIMATE_MOD"

# --- Parse args ---
if "--" not in sys.argv or len(sys.argv) < sys.argv.index("--") + 6:
    print("Too few arguments. Usage: blender --background --python script.py -- model_path export_dir blender_dir filename decimate ratio")
    sys.exit(1)

args = sys.argv[sys.argv.index("--") + 1:]
model_path = args[0]
export_dir = args[1]
blender_dir = args[2]
filename = args[3]
decimate_ratio = float(args[4])

BLENDER_FILE = os.path.join(blender_dir, "workspace.blend")

# --- Utilities ---
def clear_meshes():
    for o in bpy.data.objects:
        if o.type == 'MESH':
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.ops.object.delete()

def clear_default_scene():
    bpy.ops.object.select_all(action='DESELECT')
    for name in ['Camera', 'Light']:
        if name in bpy.data.objects:
            bpy.data.objects[name].select_set(True)
            bpy.ops.object.delete()
    clear_meshes()

def open_blend_file():
    bpy.ops.wm.open_mainfile(filepath=BLENDER_FILE)

def create_blend_file():
    clear_default_scene()
    bpy.ops.wm.save_as_mainfile(filepath=BLENDER_FILE)

def close_blend_file():
    clear_meshes()
    bpy.ops.wm.save_mainfile(filepath=BLENDER_FILE, exit=True)

def import_stl_mesh(path):
    bpy.ops.wm.stl_import(filepath=path, global_scale=0.05, up_axis='Y', use_mesh_validate=False)

def import_gltf_mesh(path):
    bpy.ops.import_scene.gltf(filepath=path)

def get_main_mesh():
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    if not meshes:
        sys.exit("No mesh found after import.")
    return meshes[0]

# --- Apply modifier with full context ---
def apply_modifier(obj, modifier_name):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = obj
    for ob in bpy.data.objects:
        ob.select_set(False)
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=modifier_name)

def decimate_mesh(obj, ratio):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = obj
    for ob in bpy.data.objects:
        ob.select_set(False)
    obj.select_set(True)

    modifier = obj.modifiers.new(MODIFIER_NAME, 'DECIMATE')
    modifier.ratio = ratio
    modifier.use_collapse_triangulate = True
    apply_modifier(obj, MODIFIER_NAME)

def convert_to_quads(obj, bShouldSubDiv=True):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    if bShouldSubDiv:
        bpy.ops.mesh.tris_convert_to_quads(face_threshold=1.0472, shape_threshold=1.0472)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.unsubdivide(iterations=4)
    else:
        bpy.ops.mesh.tris_convert_to_quads()
    bpy.ops.object.mode_set(mode='OBJECT')

def convert_to_tris(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')

def export_mesh(obj):
    blender_filename = f"{obj.name}_simplified.fbx"
    filepath = os.path.join(export_dir, blender_filename)
    print(f"Exporting to: {filepath}")
    bpy.ops.export_scene.fbx(filepath=filepath)
    return filepath

# --- Main logic ---
def run_blender_processing(file_path):
    if os.path.isfile(BLENDER_FILE):
        open_blend_file()
    else:
        create_blend_file()

    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".stl":
        import_stl_mesh(file_path)
    else:
        import_gltf_mesh(file_path)

    mesh = get_main_mesh()
    print(filename)
    print(export_dir)
    mesh.name = filename
    mesh.data.name = filename

    print("Initial faces:", len(mesh.data.polygons))

    convert_to_quads(mesh)
    print("Post Quad Convert")
    decimate_mesh(mesh, decimate_ratio)
    decimate_mesh(mesh, 0.75)
    convert_to_quads(mesh, False)

    print("Final faces:", len(mesh.data.polygons))

    export_path = export_mesh(mesh)
    print(f"Export: {export_path}")

    close_blend_file()

run_blender_processing(model_path)