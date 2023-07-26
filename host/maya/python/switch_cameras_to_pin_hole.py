from maya import cmds
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def set_camera_to_pin_hole():
    """
    This is an adapted version of the ppma function for OpenPype
    """
    cameras = cmds.ls(type="camera")
    for camera in cameras:
        if cmds.objExists("{}.mxLensType".format(camera)):
            try:
                cmds.setAttr("{}.mxLensType".format(camera), 1)
            except Exception:
                logger.warning(
                    "Can't set Pin Hole on Camera : {}".format(camera)
                )

    return True
