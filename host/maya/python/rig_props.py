# coding: utf-8
#
# - rig_props -
#
# Autorig and skin for props
#
# Copyright © FixStudio
#             All rights reserved
#
# This file is part of the project *pipeline-studio*
#
# *pipeline-studio* can not be copied and / or distributed without the express
# permission of FixStudio.


import maya.cmds as cmds
from maya import mel


WINDOW_NAME = "auto_rig_props"
WINDOW_TITLE = "Simple Rig"
WINDOW_W = 400
WINDOW_H = 80


def create_window():
    """definit UI"""
    if cmds.window(WINDOW_NAME, query=True, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    cmds.window(
        WINDOW_NAME,
        w=WINDOW_W+2,
        h=WINDOW_H,
        title=WINDOW_TITLE
    )

    cmds.columnLayout("main_column", w=WINDOW_W, h=WINDOW_H)
    cmds.separator(h=10)
    cmds.rowColumnLayout(adj=1, w=WINDOW_W, nc=2)
    cmds.button(l="Create Rig", c=createRig, w=WINDOW_W / 2)
    cmds.button(l="Create Skin", c=lambda x: bindskin(), w=WINDOW_W / 2)
    cmds.rowColumnLayout(adj=1, w=WINDOW_W)
    cmds.separator(h=10)
    cmds.button(l="Rig All", c=lambda x: createRig(True), w=WINDOW_W)

    cmds.showWindow(WINDOW_NAME)


def bindskin():
    """Create a skin for the selected objects in mel command.
    """

    selected = cmds.ls(sl=True)

    if not selected:
        cmds.confirmDialog(
            title="Empty Selection",
            message="You have to select the mesh",
            button=['Ok']
        )
        return

    for select in selected:
        cmds.select(select, 'joint_{}_prop'.format(select.split(":", 1)[-1]))
        mel.eval('createSkinCluster "-mi 5 -dr 4"')


def createRig(with_skin=False):
    """Create a rig for the selected objects with two controllers
    which adapt to the object ratio.

    Keyword Arguments:
        with_skin {bool} -- Skin the mesh to the rig or not (default: {False})
    """
    selected = cmds.ls(sl=True, transforms=True)

    if not selected:
        cmds.confirmDialog(
            title="Empty Selection",
            message="You have to select the mesh",
            button=['Ok']
        )
        return

    for item in selected:
        rot = cmds.xform(item, ws=1, q=1, rp=1)

        translate_x_value = rot[0]
        translate_y_value = rot[1]
        translate_z_value = rot[2]

        # Create main group and parent it to the rig group
        group_rig = cmds.group(
            empty=True,
            world=True,
            name='grp_{}_ctrl'.format(item.split(":", 1)[-1])
        )
        cmds.xform(t=(
            translate_x_value,
            translate_y_value, translate_z_value)
        )
        # Freeze transform
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)

        if cmds.objExists("rig"):
            cmds.parent(group_rig, "rig")
        else:
            cmds.group(empty=True, world=True, name='rig')
            cmds.parent(group_rig, "rig")

        # Create world group and controller
        group_world = cmds.group(
            n="group_{}_WORLD".format(item.split(":", 1)[-1]),
            empty=True,
            world=True
        )
        cmds.xform(t=(
            translate_x_value,
            translate_y_value,
            translate_z_value)
        )
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
        cmds.parent(group_world, group_rig)

        ctrl_name = 'c_{}_WORLD'.format(item.split(":", 1)[-1])
        world_controller = create_controller(ctrl_name, item, 5)

        cmds.xform(t=(
            translate_x_value,
            translate_y_value,
            translate_z_value)
        )

        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
        cmds.parent(world_controller, group_world)
        change_controller_color(world_controller, 17)

        # Create object group and controller
        group_object = cmds.group(
            n="group_{}_OBJECT".format(item.split(":", 1)[-1]),
            empty=True,
            world=True
        )
        cmds.xform(t=(
            translate_x_value,
            translate_y_value,
            translate_z_value)
        )
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
        cmds.parent(group_object, world_controller)

        ctrl_name = 'c_{}_OBJECT'.format(item.split(":", 1)[-1])
        object_controller = create_controller(ctrl_name, item, 3)

        cmds.xform(t=(
            translate_x_value,
            translate_y_value,
            translate_z_value)
        )

        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
        cmds.parent(object_controller, group_object)
        change_controller_color(object_controller, 9)

        cmds.joint(p=(
            translate_x_value,
            translate_y_value,
            translate_z_value),
            n='joint_{}_prop'.format(item.split(":", 1)[-1])
        )

        if with_skin:
            cmds.select(item)
            bindskin()


def change_controller_color(controller, color_index):
    """Change the color of the controller

    Arguments:
        controller {str} -- The controller you want to change the color
    """
    cmds.select(controller)
    selected_items = cmds.ls(selection=True)
    if selected_items:
        cmds.listRelatives(selected_items[0], shapes=True)
        # Enable color override for the shape
        cmds.setAttr(selected_items[0]+".overrideEnabled", 1)
        cmds.setAttr(selected_items[0]+".overrideColor", color_index)


def create_controller(ctrl_name, geo, offset):
    """Create a circle or a square controller based
    on the ratio of the selected geometry

    Arguments:
        ctrl_name {str} -- The name of the controller
        geo {str} -- The selected geometry
        offset {int} -- The offset to apply to the controller size

    Returns:
        str -- The name of the newlly created controller
    """
    cmds.select(geo)
    bounding_box = cmds.xform(bb=True, q=True)
    x_axis = bounding_box[3] - bounding_box[0]
    z_axis = bounding_box[5] - bounding_box[2]

    # Check if the ratio of the bounding box is smaller than 1.3
    if max(z_axis, x_axis) / min(z_axis, x_axis) <= 1.3:
        controller = cmds.circle(
            n=ctrl_name,
            sw=360,
            nr=(0, 1, 0),
            r=max(x_axis, z_axis) / 2 + offset
        )
    else:
        # Create a square nurbs (a group of curves that forms a square)
        cmds.nurbsSquare(
            n=ctrl_name,
            nr=(0, 1, 0),
            sl1=x_axis + offset,
            sl2=z_axis + offset
        )
        # Attach all the curves of the square
        # and then delete the original square + rename the new one
        cmds.select(ctrl_name, hi=True)
        selection = cmds.ls(selection=True)
        controller = cmds.attachCurve(selection, rpo=False)
        cmds.delete(ctrl_name)
        cmds.rename(controller, ctrl_name)

    return ctrl_name
