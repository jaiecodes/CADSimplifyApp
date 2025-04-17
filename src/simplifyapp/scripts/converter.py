# src/simplifyapp/scripts/converter.py

import os
import subprocess
import platform
from shutil import which

def find_freecad():
    fc_cmd = which("FreeCADCmd")
    if fc_cmd:
        return fc_cmd

    system = platform.system()
    if system == "Windows":
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\FreeCAD 0.21\bin\FreeCADCmd.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\FreeCAD\bin\FreeCADCmd.exe"),
        ]
    elif system == "Darwin":
        candidates = [
            "/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd",
            "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
        ]
    else:
        candidates = [
            "/usr/bin/freecadcmd",
            "/usr/local/bin/freecadcmd",
            "/snap/bin/freecadcmd",
            "/usr/bin/FreeCADCmd",
        ]

    for path in candidates:
        if os.path.isfile(path):
            return path

    raise FileNotFoundError("FreeCADCmd not found. Please install FreeCAD and add FreeCADCmd to your PATH.")

def convert_to_stl(cad_file_path, export_dir):
    if not os.path.isfile(cad_file_path):
        raise FileNotFoundError(f"Input file not found: {cad_file_path}")

    script_path = os.path.join(os.path.dirname(__file__), "stp_to_stl.py")
    freecad_cmd = find_freecad()

    try:
        result = subprocess.run([
            freecad_cmd,
            script_path,
            cad_file_path,
            export_dir
        ], capture_output=True, text=True, check=True)

        print(result.stdout)
        output_lines = result.stdout.strip().splitlines()
        path_line = next((line for line in reversed(output_lines) if line.strip().endswith(".stl")), None)

        if not path_line:
            raise RuntimeError("No exported file path found in FreeCad output.")

        print("[FreeCad] Exported file to:", path_line)
        return path_line

    except subprocess.CalledProcessError as e:
        print("[FreeCad] FreeCAD conversion failed:", e.stderr)
        raise
