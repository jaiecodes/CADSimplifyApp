# src/simplifyapp/scripts/mesh_wrap.py

import os
import subprocess
from simplifyapp.scripts.config import WRAPPER_BIN_DIR

def run_alpha_wrap(input_path, export_dir, relative_alpha=20.0, relative_offset=600.0):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Mesh file not found: {input_path}")

    print(f"[Alpha Wrap] Running mesh_wrapper on: {input_path}")

    # Use bundled binary path
    if not os.path.isfile(WRAPPER_BIN_DIR):
        raise FileNotFoundError(f"mesh_wrapper binary not found at {WRAPPER_BIN_DIR}. Ensure it was built and bundled.")

    cmd = [
        WRAPPER_BIN_DIR,
        input_path,
        str(relative_alpha),
        str(relative_offset),
        export_dir
    ]
    print(cmd)
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)
        raise RuntimeError(f"Mesh Wrap failed with return code {e.returncode}")

    model_name = os.path.splitext(os.path.basename(input_path))[0]
    filename = f"{model_name}_{int(relative_alpha)}_{int(relative_offset)}.stl"
    export_path = os.path.join(export_dir, filename)

    if not os.path.exists(export_path):
        raise FileNotFoundError(f"Expected STL output not found: {export_path}")
    print(f"[Alpha Wrap] Exported file to: {export_path}")
    return export_path
