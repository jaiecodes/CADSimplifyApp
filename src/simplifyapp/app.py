import os
import shutil
import toga
import asyncio
from toga import Size
from toga.style import Pack
from toga.style.pack import COLUMN, PACK
from pathlib import Path
from simplifyapp.scripts.cad_simplifer import run_simplifer

class SimplifyApp(toga.App):
    def startup(self):
        self.file_path = None

        self.export_dir = None

        self.left_container = toga.Box(style=Pack(direction=COLUMN, padding=(25,15,25,25)))
        self.right_container = toga.Box(style=Pack(direction=COLUMN, padding=(25,25,25,15)))

        self.select_button = toga.Button("Browse STL File", on_press=self.browse_file, style=Pack(padding=5))
        self.status_label = toga.Label("No file selected.", style=Pack(font_size=8, padding=(10, 0, 10, 0)))
        self.choose_export_btn = toga.Button("Choose Export Folder", on_press=self.select_export_folder, style=Pack(padding=5))
        self.export_label = toga.Label("No export folder selected.", style=Pack(font_size=8, padding=(10, 0, 10, 0)))
        self.simplify_button = toga.Button("Run Simplify Program", on_press=self.run_simplify, style=Pack(padding=5))
        self.result_label = toga.Label("", style=Pack(padding=5))
        self.output_log = toga.MultilineTextInput(
            readonly=True, 
            value="[CAD Simplifier] Output Log:\n",
            style=Pack(flex=1, font_family="monospace", font_size=10, padding=5))

        self.left_container.add(self.select_button)
        self.left_container.add(self.status_label)
        self.left_container.add(self.choose_export_btn)
        self.left_container.add(self.export_label)
        self.left_container.add(self.simplify_button)
        self.right_container.add(self.output_log)

        blender_path = shutil.which("blender")

        if blender_path:
            self.left_container.add(toga.Label(f"✅ Blender found at:\n{blender_path}", style=Pack(flex=1, font_size=8, padding=(10, 0, 10, 0))))
        else:
            self.left_container.add(toga.Label("❌ Blender not found in PATH", style=Pack(flex=1, font_size=8, padding=(10, 0, 10, 0))))
            
        self.left_container.add(self.result_label)
        self.split = toga.SplitContainer()
        self.split.content = [(self.left_container, 1), (self.right_container, 3)]

        self.main_window = toga.MainWindow(title=self.formal_name, size=Size(1280, 720))
        self.main_window.content = self.split
        self.main_window.show()


    async def select_export_folder(self, widget):
        folder = await self.dialog(toga.SelectFolderDialog("Choose Export Folder"))
        if folder is not None:
            self.export_dir = folder
            self.export_label.text = f"Export folder set to:\n{folder}"

    async def browse_file(self, widget):
        dialog = toga.OpenFileDialog("Select STL File", file_types=[".stl", ".STL"])
        selected = await self.dialog(dialog)

        if selected is not None:
            self.file_path = str(selected)
            self.status_label.text = f"Selected: {Path(selected).name}"

    async def append_log(self, msg):
        self.output_log.value += msg + "\n"

    async def run_simplify(self, widget):
        if not self.file_path or not os.path.exists(self.file_path):
            self.result_label.text = "Invalid or missing file."
            return

        if self.export_dir:
            output_dir = self.export_dir
        else:
            output_dir = os.path.join(os.path.expanduser("~"), ".cad_simplifier", "exports")
            os.makedirs(output_dir, exist_ok=True)
            self.export_label.text = f"Export folder set to:\n{output_dir}"


        self.result_label.text = "Running Simplifying Algorithm...\nCheck Output Log"
        self.output_log.value += f"[CAD Simplifier] Starting background processes...\n"

        main_loop = asyncio.get_running_loop()

        def thread_logger(msg):
            asyncio.run_coroutine_threadsafe(self.append_log(msg), main_loop)

        try:
            output_path = await main_loop.run_in_executor(
                None,
                run_simplifer,
                self.file_path,
                output_dir,
                thread_logger
            )
            self.result_label.text = f"Output saved to:\n{output_path}"
            await self.append_log(f"[SUCCESS] View Model at Output")
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"
            await self.append_log(f"[ERROR] {str(e)}")

def main():
    return SimplifyApp("CAD Simplifier", "com.example.simplifyapp")