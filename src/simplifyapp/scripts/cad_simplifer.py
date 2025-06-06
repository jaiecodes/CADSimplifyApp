# src/simplifyapp/scripts/cad_simplifer.py

import os
# from simplifyapp.scripts.converter import convert_to_stl
from simplifyapp.scripts.mesh_wrap import run_alpha_wrap
from simplifyapp.scripts.blend_proc import run_blender_process

def run_simplifer(model_path, export_dir, decimate_raio, wrap_offset, wrap_alpha, logger):
    print(f"[CAD Simplifier] Processing... {model_path}")
    logger(f"[CAD Simplifier] Processing... {model_path}")
    
    filename, _ = os.path.splitext(os.path.basename(model_path))

    print("[CAD Simplifier] Running first alpha wrap...")
    logger("[CAD Simplifier] Running first alpha wrap...")
    wrapped_path_1 = run_alpha_wrap(model_path, export_dir, wrap_alpha, wrap_offset, logger)

    print("[CAD Simplifier] Running second alpha wrap...")
    logger("[CAD Simplifier] Running second alpha wrap...")
    wrapped_path_2 = run_alpha_wrap(wrapped_path_1, export_dir,(wrap_alpha-200.0), (wrap_offset-500.0), logger)

    print("[CAD Simplifier] Running Blender processing via subprocess...")
    logger("[CAD Simplifier] Running Blender processing via subprocess...")
    final_path = run_blender_process(wrapped_path_2, export_dir, filename, decimate_raio, logger)

    print(f"[CAD Simplifier] Done! Final output at: {final_path}")
    logger(f"[CAD Simplifier] Done! Final output at: {final_path}")
    return final_path
