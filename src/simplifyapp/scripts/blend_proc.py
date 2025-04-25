# src/simplifyapp/scripts/blend_proc.py

import os
import subprocess
import platform
from shutil import which

from simplifyapp.scripts.config import BLENDER_DIR

def find_blender():
    blender = which("blender")
    if blender:
        return blender

    system = platform.system()
    candidates = []
    if system == "Windows":
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Blender Foundation\Blender\blender.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Blender Foundation\Blender\blender.exe"),
            r"C:\Blender\blender.exe",
        ]
    elif system == "Darwin":
        candidates = [
            "/Applications/Blender.app/Contents/MacOS/Blender",
        ]
    else:
        candidates = [
            "/usr/bin/blender",
            "/snap/bin/blender",
            "/usr/local/bin/blender",
        ]

    for path in candidates:
        if os.path.isfile(path):
            return path

    raise FileNotFoundError("Blender executable not found. Please install Blender or add it to your PATH.")

def run_blender_process(model_path, export_dir, logger):
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Input file not found: {model_path}")

    blender_script = os.path.join(os.path.dirname(__file__), "blend_utils.py")
    blender_path = find_blender()

    try:
        result = subprocess.run([
            blender_path,
            "--background",
            "--python", blender_script,
            "--", model_path, export_dir, BLENDER_DIR
        ], capture_output=True, text=True, check=True)

        print(result.stdout)
        logger(result.stdout)
        output_lines = result.stdout.strip().splitlines()
        path_line = next((line for line in reversed(output_lines) if line.startswith("Export:")), None)
        if path_line:
            path_line = path_line.replace("Export: ", "").strip()

        if not path_line:
            raise RuntimeError("No exported file path found in Blender output.")

        print(f"[Blender] Exported file to: {path_line}")
        logger(f"[Blender] Exported file to: {path_line}")
        return path_line

    except subprocess.CalledProcessError as e:
        print("[Blender] Blender process failed:", e.stderr)
        raise
