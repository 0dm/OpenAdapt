import os
import subprocess
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

import nicegui

datas = collect_data_files("en_core_web_trf")

spec = [
    "pyi-makespec",
    f"{Path(__file__).parent}/main.py",
    f"--icon={Path(__file__).parent}/assets/logo.ico",
    "--name",
    "OpenAdapt",  # name
    # "--onefile", # trade startup speed for smaller file size
    "--onedir",
    "--windowed",  # prevent console appearing, only use with ui.run(native=True, ...)
    "--add-data",
    f"{Path(nicegui.__file__).parent}{os.pathsep}nicegui",
    "--add-data",
    f"{Path(__file__).parent}{os.pathsep}assets",
    "--hidden-import=pydicom.encoders.gdcm",
    "--hidden-import=pydicom.encoders.pylibjpeg",
    # add spacy model en_core_web_trf
    "--hidden-import=en_core_web_trf",
]

subprocess.call(spec)

# add import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5) to line 2 of OpenAdapt.spec
with open("OpenAdapt.spec", "r+") as f:
    lines = f.readlines()
    lines[1] = "import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)\n"
    f.seek(0)
    f.truncate()
    f.writelines(lines)

subprocess.call(["pyinstaller", "OpenAdapt.spec"])
