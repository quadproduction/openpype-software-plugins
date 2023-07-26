import logging

import maya.cmds as cmds

format = "%(asctime)s %(levelname)s\t%(module)s.%(funcName)s | %(message)s"
logging.basicConfig(format=format)
logger = logging.getLogger("ppTools")
logger.setLevel(logging.INFO)


def snap(source, destination=None, snap_method="snap_transform"):
    """
    snap object
    """

    if snap_method == "snap_transform":
        cmds.parentConstraint(
            source,
            destination,
            skipTranslate="none",
            skipRotate="none",
            maintainOffset=False,
        )
        cmds.scaleConstraint(source, destination, maintainOffset=False)
        cmds.delete(destination, constraints=True)
        return True

    if snap_method == "constraint_t_r_s":
        constraint_translate = False
        constraint_rotate = False
        constraint_scale = False
        # split constraint
        constraint = snap_method.replace("constraint_", "")
        if "t" in constraint:
            constraint_translate = True
        if "r" in constraint:
            constraint_rotate = True
        if "s" in constraint:
            constraint_scale = True

        if constraint_translate or constraint_rotate:
            # set
            skipTranslate = "none"
            skipRotate = "none"
            if not constraint_translate:
                skipTranslate = ["x", "y", "z"]
            if not constraint_rotate:
                skipRotate = ["x", "y", "z"]

            cmds.parentConstraint(
                source,
                destination,
                skipTranslate=skipTranslate,
                skipRotate=skipRotate,
                maintainOffset=True,
            )

        if constraint_scale:
            cmds.scaleConstraint(source, destination, maintainOffset=True)

        return True

    return


def create_outMesh_inMesh(source, destination=None):
    """
    this awesome function, connect source.outMesh to destination.inMesh
    if destination not specified we create a polyCube and
    connect outMesh to it.
    """

    # check name
    if cmds.objExists("{source}.outMesh".format(source=source)):

        if not destination:
            # create polyCube
            destination = "{source}_inMesh".format(source=source)
            destination = cmds.polyCube(name=destination, ch=False)[0]
            # snap mesh to source
            snap(
                source=source,
                destination=destination,
                snap_method="snap_transform",
            )

        if cmds.objExists(
            "{destination}.inMesh".format(destination=destination)
        ):
            # try connect to connect
            cmds.connectAttr(
                "{source}.outMesh".format(source=source),
                "{destination}.inMesh".format(destination=destination),
                force=True,
            )

        else:
            logging.error(
                "No destination object found, can't perform connection."
            )
            return
    else:
        logging.error("Can't create outMesh inMesh without {source}.outMesh")
        return


def create_outMesh_inMesh_selection():
    """
    this awesome function, connect source.outMesh to destination.inMesh
    if destination not specified we create a polyCube and
    connect outMesh to it.
    """

    sels = cmds.ls(sl=True, l=True)

    if sels:
        if len(sels) == 1:
            return create_outMesh_inMesh(source=sels[0], destination=None)
        elif len(sels) == 2:
            return create_outMesh_inMesh(source=sels[0], destination=sels[1])
