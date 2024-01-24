from pathlib import Path

plugin_name = "Studio Library"
plugin_version = "2.13.2"
plugin_package_path = Path("/prod/softprod/apps/studiolibrary/{}/linux".format(plugin_version))
plugin_install_script_name = "install.py"
plugin_package_script_path = plugin_package_path.joinpath(plugin_install_script_name)

def install():
    globals_dict = globals()
    globals_dict["__file__"] = plugin_package_script_path.resolve()

    # Check if the Studio Library shelf icon is already present on the shelf of the user
    # If yes delete all occurrences
    import maya.cmds as cmds

    shelf_name = "Polygons"
    shelf_elems = cmds.shelfLayout(shelf_name, query=True, fullPathName=True, childArray=True)

    for shelf_elem in shelf_elems:
        shelf_elem_fullname = "{}|{}".format(shelf_name, shelf_elem)
        if cmds.objectTypeUI(shelf_elem, isType="shelfButton") and \
            cmds.shelfButton(shelf_elem_fullname, query=True, annotation=True) == plugin_name:
            cmds.deleteUI(shelf_elem_fullname, control=True)

    exec(open(plugin_package_script_path).read(), globals_dict)
