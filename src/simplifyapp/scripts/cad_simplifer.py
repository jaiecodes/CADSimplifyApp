# src/simplifyapp/scripts/cad_simplifer.py

import os
# from simplifyapp.scripts.converter import convert_to_stl
from simplifyapp.scripts.mesh_wrap import run_alpha_wrap
from simplifyapp.scripts.blend_proc import run_blender_process

def run_simplifer(model_path, export_dir):
    print(f"[Simplifer] Processing... {model_path}")
    # print("[Simplifer] Starting conversion to STL...")
    # stl_path = convert_to_stl(model_path, export_dir)

    print("[Simplifer] Running first alpha wrap...")
    wrapped_path_1 = run_alpha_wrap(model_path, export_dir, relative_alpha=500.0, relative_offset=6500.0)

    print("[Simplifer] Running second alpha wrap...")
    wrapped_path_2 = run_alpha_wrap(wrapped_path_1, export_dir, relative_alpha=300.0, relative_offset=6000.0)

    print("[Simplifer] Running Blender processing via subprocess...")
    final_path = run_blender_process(wrapped_path_2, export_dir)

    print("[Simplifer] Done! Final output at:", final_path)
    return final_path
