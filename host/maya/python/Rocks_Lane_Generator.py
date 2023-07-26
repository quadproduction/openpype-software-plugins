import maya.cmds as cmds
import random as rand

# Rocks Lane Generator - RECYLUM
"""

PLEASE SELECT ROCKS THEN PRESS BUILD

PLEASE USE THE "rockOrigamiMiniLongA Asset"

"""


def create_rocks_lane(*Args):

    Rocks_Selection = cmds.ls(sl=True)

    try:
        NbsRocks = cmds.intField("Nbs_Rocks", query=True, value=True)
        RocksOffset = 0
        RocksOffsetAdd = cmds.floatField(
            "Rocks_Offset",
            query=True,
            value=True
        )

        cmds.group(em=True, name="Rocks_Lane_grp")

        for i in range(0, NbsRocks):

            Random_Rocks = rand.randint(0, len(Rocks_Selection) - 1)

            RockInstance = cmds.instance(Rocks_Selection[Random_Rocks])

            cmds.select(RockInstance)

            cmds.move(RocksOffset, 0, 0)
            RocksOffset = RocksOffset + RocksOffsetAdd

            cmds.rotate(0, rand.uniform(0, 360), 0)
            cmds.scale(
                rand.uniform(0.6, 1.25),
                rand.uniform(0.6, 1.25),
                rand.uniform(0.6, 1.25),
            )

            cmds.parent(RockInstance, "Rocks_Lane_grp")

    except Exception:
        if len(Rocks_Selection) == 0:
            cmds.warning("No Rocks in Selection")


# GUI
# CHECK IF WINDOWS EXISTS/DELETE UI IF NEEDED


def create_rocks_lane_gui():
    """
    gfgjkfjgfkgjfkjg
    """
    if cmds.window("window", exists=True):
        cmds.deleteUI("window")

    window = cmds.window(
        "window",
        title="Rock Lane Generator",
        widthHeight=(400, 120)
    )

    # MAIN LAYOUT

    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="Rock Lane Generator", align="center", fn="boldLabelFont")
    cmds.separator(h=10, style="none")

    cmds.text(label="Please Select Rocks", align="center", fn="boldLabelFont")
    cmds.separator(h=10, style="none")

    cmds.text(label="Nbs_Rocks", align="center")
    cmds.separator(h=5, style="none")

    cmds.intField("Nbs_Rocks", minValue=1, value=50)
    cmds.separator(h=5, style="none")

    cmds.text(label="Rocks_Offset", align="center")
    cmds.separator(h=5, style="none")

    cmds.floatField("Rocks_Offset", minValue=1, value=1)
    cmds.separator(h=5, style="none")

    cmds.button(
        label="Build",
        command=(
            "from host.maya.python import Rocks_Lane_Generator; \
Rocks_Lane_Generator.create_rocks_lane()"
        ),
    )
    cmds.button(label="Delete", command=('cmds.delete("Rocks_Lane_grp*")'))
    cmds.button(
        label="Close",
        command=('cmds.deleteUI("' + window + '", window=True)')
    )

    # MAIN LAYOUT SET PARENT

    cmds.setParent("..")

    cmds.showWindow(window)

    return True
