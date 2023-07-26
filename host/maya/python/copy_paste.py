# -*- coding: utf-8 -*-

"""
Modified version of file /prod/studio/pipeline/latest/maya/common/python/ppma/action/ppCopyPaste.py from old Fix Studio pipeline.
Import of ppPath removed for openPype integration.
"""

__author__ = 'OBLET jeremy'
__email__ = 'jeremy.oblet@fixstudio.com'

import os
import tempfile
import maya.cmds as cmds

class CopyPaste(object):
	def __init__(self):
		super(CopyPaste, self).__init__()

		self.type = "mayaBinary"
		self.ext = ".mb"
		self.root_directory = tempfile.gettempdir()
		self.copy_paste_scene = os.path.join(self.root_directory, "CopyPaste_mayaScene")

	def copy(self):
		cmds.file(self.copy_paste_scene, force=True, options="v=1", type=self.type, preserveReferences=True, exportUnloadedReferences=True, exportSelected=True, uiConfiguration=False)
		return

	def paste(self):
		cmds.file(self.copy_paste_scene + self.ext, i=True, ignoreVersion=True, type=self.type, preserveReferences=True, mergeNamespacesOnClash=False)
		return


def copy():
	cp = CopyPaste()
	cp.copy()

def paste():
	cp = CopyPaste()
	cp.paste()