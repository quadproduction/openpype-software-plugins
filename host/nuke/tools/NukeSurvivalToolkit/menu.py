#*****************************************************************
#*****************************************************************
# This file will setup the NukeSurvivalToolkit Menu on your Toolbar
# Written by Tony Lyons 09/2020 | www.CreativeLyons.com | www.CompositingMentor.com
#*****************************************************************
#*****************************************************************

import nuke
import sys
import os
import webbrowser

# Add PluginPaths to tools and icons
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./python')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./images')
nuke.pluginAddPath('./nk_files')

# Import some helpful functions for the NST
import NST_helper

# This is the prefix being used to customize the gizmo's in this toolkit
global prefixNST
prefixNST = "NST_"

# Store the location of this menu.py to help with nuke.nodePaste() which requires a filepath to paste
NST_FolderPath = os.path.dirname(__file__)
NST_helper.NST_FolderPath = NST_FolderPath

# give the name of the help doc .pdf in main folder
NST_helpDoc = "NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf"

# creating full filepath to the help doc
NST_helpDoc_os_path = os.path.join(NST_FolderPath, NST_helpDoc)
NST_helpDocPath = "file:///{}".format(NST_helpDoc_os_path)