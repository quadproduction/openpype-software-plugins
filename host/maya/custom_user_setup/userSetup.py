from os import getenv, environ, pathsep, path, sep
from distutils.spawn import find_executable
from pathlib import Path
import sys
import subprocess
import json
import maya.mel as mel
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
    if environ.get("MAYA_SCRIPT_PATH"):
        environ["MAYA_SCRIPT_PATH"] = f"{path}{pathsep}{environ['MAYA_SCRIPT_PATH']}"
    else:
        environ["MAYA_SCRIPT_PATH"] = str(path)

    sub_dir = [x for x in path.iterdir() if x.is_dir()]
    if sub_dir:
        for dir in sub_dir:
            add_mel_folder_to_MAYA_SCRIPT_PATH(dir)

def get_deadlinecommand():
    """
    Finds the Deadline Command executable as it is installed on your machine by searching in the following order:
    * The DEADLINE_PATH environment variable
    * The PATH environment variable
    * The file /Users/Shared/Thinkbox/DEADLINE_PATH
    """

    for env in ("DEADLINE_PATH", "PATH"):
        try:
            env_value = environ[env]
        except KeyError:
            # if the error is a key error it means that DEADLINE_PATH is not set.
            # however Deadline command may be in the PATH or on OSX it could be in the file /Users/Shared/Thinkbox/DEADLINE_PATH
            continue

        exe = find_executable("deadlinecommand", env_value)
        if exe:
            return exe

    # On OSX, we look for the DEADLINE_PATH file if the environment variable does not exist.
    if path.exists("/Users/Shared/Thinkbox/DEADLINE_PATH"):
        with open("/Users/Shared/Thinkbox/DEADLINE_PATH") as dl_file:
            deadline_bin = dl_file.read().strip()
        exe = find_executable("deadlinecommand", deadline_bin)
        if exe:
            return exe

    raise Exception("Deadline could not be found.  Please ensure that Deadline is installed.")


def call_deadlinecommand(arguments, format_output_as_json=False):
    """
    Calls DeadlineCommand with a given list of arguments.
    If json_output is true the output is returned as a json dictionary.
    Otherwise the raw string is output is returned.
    """
    command = [get_deadlinecommand()]
    if format_output_as_json:
        # JSON formatting option must come directly after the Deadline Command executable in the argument list.
        command.append('-prettyJSON')
    command.extend(arguments)
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = proc.communicate()

    # py2/3 compatible manner to ensure we have a str
    if not isinstance(output, str):
        output = output.decode()  # type: ignore

    if format_output_as_json:
        json_out = json.loads(output)
        if json_out["ok"]:
            return json_out["result"]
        else:
            raise Exception(json_out["result"])
    else:
        if proc.returncode:
            raise Exception(output)
        return output  # type: ignore


def GetMayaSubmissionDir():
    """
    Uses Deadline command to pull the main Maya integrated submitter.
    """
    # Maya always uses / for it's path separators regardless of platform
    PATH_SEP = '/'
    json_out = call_deadlinecommand(["-GetRepositoryPath", "submission/Maya/Main"], format_output_as_json=True)
    return json_out.replace(sep, PATH_SEP)


def load_deadline_submitters():
    """
    Pulls the Deadline integrated submitter from the Deadline repository and sources the mel file.
    """
    # Get the repository path
    try:
        submission_dir = GetMayaSubmissionDir()
    except Exception as e:
        print("Failed to pull Deadline Integrated submitter: %s" % e)
        return

    submission_file = '{}/SubmitMayaToDeadline.mel'.format(submission_dir)
    if path.isfile(submission_file):
        mel.eval('source "{}";'.format(submission_file))
    else:
        print('Deadline submission directory does not contain SubmitMayaToDeadlne.mel')

    print('Deadline has been successfully loaded')


if __name__ == "__main__":

    print("#" * 10, f" Starting custom userSetup.py for openpype_software_plugins from {getenv('OPENPYPE_SOFTWARE_PLUGINS')} ", "#" * 10)

    python_folder = Path(getenv("OPENPYPE_SOFTWARE_PLUGINS")) / "host" / "maya" / "python"
    add_python_folder_to_path(python_folder)

    mel_folder = Path(getenv("OPENPYPE_SOFTWARE_PLUGINS")) / "host" / "maya" / "mel"
    add_mel_folder_to_MAYA_SCRIPT_PATH(mel_folder)

    # Have maya load the submitters after it finishes loading all mel script files.
    cmds.evalDeferred(load_deadline_submitters)

    print("#" * 10, f" Finishing custom userSetup.py for openpype_software_plugins from {getenv('OPENPYPE_SOFTWARE_PLUGINS')} ", "#" * 10)
