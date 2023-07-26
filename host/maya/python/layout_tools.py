# ppLayoutTools
import maya.cmds as cmds
import maya.mel as mel


def duplicate_as_instance_selection():
    """
    """
    sl = cmds.ls(sl=True)
    for item in sl:
        duplicate_as_instance(node=item)


def duplicate_as_instance(node):
    """
    """
    new_name = "{0}_i001".format(node.replace(":", "_"))
    return cmds.instance(node, n=new_name)


def create_proxy_selection():
    """
    """
    sl = cmds.ls(sl=True)
    for item in sl:
        create_proxy(node=item)


def create_proxy(node):
    """
    """
    # duplicate mesh
    r = cmds.duplicate(node, returnRootsOnly=True)

    # reduce polygon
    cmds.polyReduce(
        r,
        ver=1,
        trm=2,
        shp=False,
        keepBorder=False,
        keepMapBorder=False,
        keepColorBorder=False,
        keepFaceGroupBorder=False,
        keepHardEdge=False,
        keepCreaseEdge=False,
        useVirtualSymmetry=False,
        preserveTopology=True,
        keepQuadsWeight=True,
        cachingReduce=True,
        ch=False,
        tct=250,
        replaceOriginal=True
    )

    new_name = "proxy_{0}".format(node.split(":")[-1])
    n = cmds.rename(r, new_name)
    print(n)
    # delete non mesh shape
    children = cmds.listRelatives(n, children=True, shapes=True)
    for c in children:
        if cmds.nodeType(c) != "mesh":
            cmds.delete(c)


def replace_node_by_instance():
    """
    """
    nodes = cmds.ls(sl=True, l=True)
    source_node = nodes[len(nodes) - 1]

    for i in range(0, len(nodes) - 1):

        n = nodes[i]

        # get transform
        world_matrix = cmds.xform(n, query=True, worldSpace=True, matrix=True)

        # build node info
        n_instance = duplicate_as_instance(source_node)[0]

        cmds.xform(n_instance, matrix=world_matrix, worldSpace=True)


def launch_layout_tools():
    """
    """
    mel.eval(
        """if (`layout -ex LT_form` && `dockControl -q -visible LT_Dock` &&
        (`optionVar -q LT_UIMode` != 0)) {
            dockControl -e -visible 0 LT_Dock;
            optionVar -iv LT_UIMode 1;
            raiseChannelBox;
        }else if (`layout -ex LT_form` && `dockControl -q -visible LT_Dock` &&
        (`optionVar -q LT_UIMode` == 0)) {
            optionVar -intValue LT_RebuildUI 0;
            optionVar -iv LT_UIMode 1;
            LT_UI;
        }else if (`layout -ex LT_form` && (
            !`dockControl -q -visible LT_Dock`
        )) {
            optionVar -intValue LT_RebuildUI 0;
            optionVar -iv LT_UIMode 1;
            LT_UI;
        } else {
            optionVar -intValue LT_RebuildUI 1;
            optionVar -iv LT_UIMode 1;
            LT_UI;
        };"""
    )
