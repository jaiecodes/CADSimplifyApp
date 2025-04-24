import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from pathlib import Path
import os
import shutil
import platform
import subprocess
from simplifyapp.scripts.cad_simplifer import run_simplifer

class SimplifyApp(toga.App):
    def startup(self):
        self.file_path = None
        self.export_dir = None

        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.status_label = toga.Label("No file selected.", style=Pack(padding=(0, 0, 10, 0)))
        self.select_button = toga.Button("Browse", on_press=self.browse_file, style=Pack(padding=5))
        self.choose_export_btn = toga.Button("Choose Export Folder", on_press=self.select_export_folder, style=Pack(padding=5))
        self.simplify_button = toga.Button("Run Simplify", on_press=self.run_simplify, style=Pack(padding=5))

        self.result_label = toga.Label("", style=Pack(padding=5))
        self.main_box.add(self.status_label)
        self.main_box.add(self.select_button)
        self.main_box.add(self.choose_export_btn)
        self.main_box.add(self.simplify_button)
        self.main_box.add(self.result_label)

        #freecad_path = shutil.which("freecadcmd")
        blender_path = shutil.which("blender")

        # if freecad_path:
        #     self.main_box.add(toga.Label(f"✅ FreeCAD found at: {freecad_path}", style=Pack(padding=5)))
        # else:
        #     self.main_box.add(toga.Label("❌ FreeCAD not found in PATH", style=Pack(padding=5)))

        if blender_path:
            self.main_box.add(toga.Label(f"✅ Blender found at: {blender_path}", style=Pack(padding=5)))
        else:
            self.main_box.add(toga.Label("❌ Blender not found in PATH", style=Pack(padding=5)))
            
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()


    async def select_export_folder(self, widget):
        folder = await self.dialog(toga.SelectFolderDialog("Choose Export Folder"))
        if folder:
            self.export_dir = folder
            self.result_label.text = f"Export folder set to:\n{folder}"

    async def browse_file(self, widget):
        dialog = toga.OpenFileDialog("Select STL File", file_types=[".stl", ".STL"])
        selected = await self.dialog(dialog)

        if selected is not None:
            self.file_path = str(selected)
            self.status_label.text = f"Selected: {Path(selected).name}"

    def run_simplify(self, widget):
        if not self.file_path or not os.path.exists(self.file_path):
            self.result_label.text = "Invalid or missing file."
            return

        if self.export_dir:
            output_dir = self.export_dir
        else:
            output_dir = os.path.join(os.path.expanduser("~"), ".cad_simplifier", "exports")
            os.makedirs(output_dir, exist_ok=True)

        self.result_label.text = "Simplifying..."
        try:
            output_path = run_simplifer(self.file_path, output_dir)
            self.result_label.text = f"✅ Done! Output saved to:\n{output_path}"
        except Exception as e:
            self.result_label.text = f"❌ Error: {str(e)}"

def main():
    return SimplifyApp("CAD Simplifier", "com.example.simplifyapp")