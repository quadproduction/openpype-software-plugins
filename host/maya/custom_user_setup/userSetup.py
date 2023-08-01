from os import getenv, environ, pathsep
from pathlib import Path
import sys


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
    if environ.get("MAYA_SCRIPT_PATH"):
        environ["MAYA_SCRIPT_PATH"] = f"{path}{pathsep}{environ['MAYA_SCRIPT_PATH']}"
    else:
        environ["MAYA_SCRIPT_PATH"] = str(path)

    sub_dir = [x for x in path.iterdir() if x.is_dir()]
    if sub_dir:
        for dir in sub_dir:
            add_mel_folder_to_MAYA_SCRIPT_PATH(dir)


if __name__ == "__main__":

    print("#" * 10, f" Starting custom userSetup.py for openpype_software_plugins from {getenv('OPENPYPE_SOFTWARE_PLUGINS')} ", "#" * 10)

    python_folder = Path(getenv("OPENPYPE_SOFTWARE_PLUGINS")) / "host" / "maya" / "python"
    add_python_folder_to_path(python_folder)

    mel_folder = Path(getenv("OPENPYPE_SOFTWARE_PLUGINS")) / "host" / "maya" / "mel"
    add_mel_folder_to_MAYA_SCRIPT_PATH(mel_folder)

    print("#" * 10, f" Finishing custom userSetup.py for openpype_software_plugins from {getenv('OPENPYPE_SOFTWARE_PLUGINS')} ", "#" * 10)
