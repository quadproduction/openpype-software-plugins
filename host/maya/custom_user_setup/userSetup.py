import os
from pathlib import Path
import sys

from maya import cmds


def add_python_folder_to_path(path: Path):
    print(f"Adding {path} to sys.path")
    sys.path.append(str(path))


def add_mel_folder_to_MAYA_SCRIPT_PATH(path: Path):
    if not path.exists():
        print(f"Path {path} does not exist. Skipping.")
        return

    if not list(path.glob("*.mel")):
        print(f"Path {path} does not contain any mel files. Skipping.")
        return

    print(f"Adding {path} to MAYA_SCRIPT_PATH")
    if os.environ.get("MAYA_SCRIPT_PATH"):
        os.environ["MAYA_SCRIPT_PATH"] = str(Path(path).joinpath(os.environ['MAYA_SCRIPT_PATH']).resolve())
    else:
        os.environ["MAYA_SCRIPT_PATH"] = str(path)

    sub_dir = [x for x in path.iterdir() if x.is_dir()]
    if sub_dir:
        for dir in sub_dir:
            add_mel_folder_to_MAYA_SCRIPT_PATH(dir)


def install_python_plugins():
    # Plugin: Studio Library
    from studiolibrary_installer import install
    install()
    # ----------------------


if __name__ == "__main__":
    OPENPYPE_SOFTWARE_PLUGINS = os.getenv('OPENPYPE_SOFTWARE_PLUGINS')
    print("#" * 10, f" Starting custom userSetup.py for openpype_software_plugins from {OPENPYPE_SOFTWARE_PLUGINS} ", "#" * 10)

    # Add Python scripts to PYTHONPATH
    python_folder = Path(OPENPYPE_SOFTWARE_PLUGINS).joinpath("host", "maya", "python").resolve()
    add_python_folder_to_path(python_folder)

    # Install annexes Python plugins
    cmds.evalDeferred(install_python_plugins)

    # Mel Plugins
    mel_folder = Path(OPENPYPE_SOFTWARE_PLUGINS).joinpath("host", "maya", "mel").resolve()
    add_mel_folder_to_MAYA_SCRIPT_PATH(mel_folder)

    print("#" * 10, f" Finishing custom userSetup.py for openpype_software_plugins from {OPENPYPE_SOFTWARE_PLUGINS} ", "#" * 10)
