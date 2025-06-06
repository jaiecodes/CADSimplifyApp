import os
import shutil
import toga
import asyncio
from toga import Size
from toga.style import Pack
from toga.style.pack import COLUMN, PACK, ROW
from pathlib import Path
from simplifyapp.scripts.cad_simplifer import run_simplifer

class SimplifyApp(toga.App):
    def startup(self):
        self.file_path = None
        self.export_dir = None

        self.decimate_ratio_slider = toga.Slider(
            min=0.0,  # Use min_value instead of range
            max=1.0,
            value=0.2, # Default value
            tick_count=11, # For 0.0, 0.1, ..., 1.0 (11 ticks)
            on_change=self._update_decimate_label, 
            style=Pack(flex=1) 
        )
        self.decimate_ratio_label = toga.Label(f"{self.decimate_ratio_slider.value:.2f}", style=Pack(width=50, text_align="right"))

        self.wrap_offset_slider = toga.Slider(
            min=1000.0, 
            max=7000.0,
            value=6500.0, # Default value
            tick_count=25, # For 1000, 2000, ..., 7000 (7 ticks for major intervals, increments by 250)
            on_change=self._update_wrap_label,
            style=Pack(flex=1)
        )
        self.wrap_offset_label = toga.Label(f"{self.wrap_offset_slider.value:.1f}", style=Pack(width=60, text_align="right"))


        self.alpha_offset_slider = toga.Slider(
            min=100.0, 
            max=600.0,
            value=500.0, # Default value
            tick_count=11, # For 100, 200, ..., 600 (6 ticks for major intervals, increments by 50)
            on_change=self._update_alpha_label,
            style=Pack(flex=1)
        )
        self.alpha_offset_label = toga.Label(f"{self.alpha_offset_slider.value:.1f}", style=Pack(width=60, text_align="right"))


        self.left_container = toga.Box(style=Pack(direction=COLUMN, padding=(25,15,25,25)))
        self.right_container = toga.Box(style=Pack(direction=COLUMN, padding=(25,25,25,15)))

        self.select_button = toga.Button("Browse STL File", on_press=self.browse_file, style=Pack(padding=5))
        self.status_label = toga.Label("No file selected.", style=Pack(font_size=8, padding=(10, 0, 10, 0)))
        self.choose_export_btn = toga.Button("Choose Export Folder", on_press=self.select_export_folder, style=Pack(padding=5))
        self.export_label = toga.Label("No export folder selected.", style=Pack(font_size=8, padding=(10, 0, 10, 0)))
        self.decimate_box = toga.Box(style=Pack(direction=ROW, alignment="center", padding=(5,0)))
        self.decimate_box.add(toga.Label("Decimate Ratio:", style=Pack(width=120)))
        self.decimate_box.add(self.decimate_ratio_slider)
        self.decimate_box.add(self.decimate_ratio_label) # Add label to display current value

        self.wrap_offset_box = toga.Box(style=Pack(direction=ROW, alignment="center", padding=(5,0)))
        self.wrap_offset_box.add(toga.Label("Wrap Offset:", style=Pack(width=120)))
        self.wrap_offset_box.add(self.wrap_offset_slider)
        self.wrap_offset_box.add(self.wrap_offset_label) # Add label to display current value

        self.alpha_offset_box = toga.Box(style=Pack(direction=ROW, alignment="center", padding=(5,0)))
        self.alpha_offset_box.add(toga.Label("Wrap Alpha:", style=Pack(width=120)))
        self.alpha_offset_box.add(self.alpha_offset_slider)
        self.alpha_offset_box.add(self.alpha_offset_label) 
        
        
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

        self.left_container.add(toga.Label("--- Simplifier Settings ---", style=Pack(padding_top=15, padding_bottom=5, font_size=9, color="gray")))
        self.left_container.add(self.decimate_box)
        self.left_container.add(self.wrap_offset_box)
        self.left_container.add(self.alpha_offset_box)

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

    def _update_decimate_label(self, slider):
        self.decimate_ratio_label.text = f"{slider.value:.2f}"

    def _update_wrap_label(self, slider):
        self.wrap_offset_label.text = f"{slider.value:.1f}"

    def _update_alpha_label(self, slider):
        self.alpha_offset_label.text = f"{slider.value:.1f}"

    async def select_export_folder(self, widget):
        folder = await self.dialog(toga.SelectFolderDialog("Choose Export Folder"))
        if folder is not None:
            self.export_dir = folder
            self.export_label.text = f"Export folder set to:\n{folder}"

    async def browse_file(self, widget):
        dialog = toga.OpenFileDialog("Select STL File", file_types=["stl", "STL"])
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

        decimate_ratio = self.decimate_ratio_slider.value
        wrap_offset = self.wrap_offset_slider.value
        wrap_alpha = self.alpha_offset_slider.value

        self.result_label.text = "Running Simplifying Algorithm...\nCheck Output Log"
        await self.append_log(f"[CAD Simplifier] Starting background processes with:\n"
                               f"  Decimate Ratio: {decimate_ratio:.2f}\n" # Format for display
                               f"  Wrap Offset: {wrap_offset:.1f}\n"
                               f"  Alpha Offset: {wrap_alpha:.1f}")

        main_loop = asyncio.get_running_loop()

        def thread_logger(msg):
            asyncio.run_coroutine_threadsafe(self.append_log(msg), main_loop)

        try:
            output_path = await main_loop.run_in_executor(
                None,
                run_simplifer,
                self.file_path,
                output_dir,
                decimate_ratio,
                wrap_offset,
                wrap_alpha,
                thread_logger
            )
            self.result_label.text = f"Output saved to:\n{output_path}"
            await self.append_log(f"[SUCCESS] View Model at Output")
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"
            await self.append_log(f"[ERROR] {str(e)}")

def main():
    return SimplifyApp("CAD Simplifier", "com.example.simplifyapp")