# src/simplifyapp/scripts/config.py

import os
import platform

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

WRAPPER_BIN_NAME = "mesh_wrapper.exe" if platform.system() == "Windows" else "mesh_wrapper"
WRAPPER_BIN_DIR = os.path.join(APP_DIR, "resources", "bin", WRAPPER_BIN_NAME)

BLENDER_DIR = os.path.join(APP_DIR, "resources", "blender")
os.makedirs(BLENDER_DIR, exist_ok=True)
