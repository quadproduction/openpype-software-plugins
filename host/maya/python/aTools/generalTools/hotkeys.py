'''
========================================================================================================================
Author: Alan Camilo
www.alancamilo.com

Requirements: aTools Package

------------------------------------------------------------------------------------------------------------------------
To install aTools, please follow the instructions in the file how_to_install.txt

------------------------------------------------------------------------------------------------------------------------
To unistall aTools, go to menu (the last button on the right), Uninstall

========================================================================================================================
'''

def getHotkeys():

    yellow  = [{
                "name":"RepeatLastTweenMachineCommand",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.tweenMachine.repeatLastCommand()",
                "hotkey":"t",
                "alt":0,
                "ctl":0,
                "toolTip":"Repeat the last Tween Machine command"
                },{
                "name":"SetSmartKey",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.setSmartKey()",
                "hotkey":"s",
                "alt":0,
                "ctl":0,
                "toolTip":"Set a key without changing the tangents"
                },{
                "name":"SetSmartKeyOnScrub",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.setSmartKey(insert=False)",
                "hotkey":"s",
                "alt":1,
                "ctl":0,
                "toolTip":"Copy a key dragged with middle mouse"
                },{
                "name":"smartSnapKeys",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.smartSnapKeys()",
                "hotkey":"S",
                "alt":0,
                "ctl":1,
                "toolTip":"Snap decimal frame keys to the closest integer frame and preserve the curves"
                },{
                "name":"SelectOnlyKeyedObjects",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.selectOnlyKeyedObjects()",
                "hotkey":"s",
                "alt":1,
                "ctl":1,
                "toolTip":"Select the objects which the selected keys belong to"
                }]

    green   = [{
                "name":"EulerFilterSelection",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.eulerFilterSelection()",
                "hotkey":"E",
                "alt":0,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"ResetValue",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.keyTransform.resetValue()",
                "hotkey":"0",
                "alt":0,
                "ctl":0,
                "toolTip":"The same as the reset value button"
                },{
                "name":"NudgeKeyLeft",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.nudge.nudgeKey(-1)",
                "hotkey":",",
                "alt":0,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"NudgeKeyRight",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.nudge.nudgeKey(1)",
                "hotkey":".",
                "alt":0,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"AddInbetween",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.keyTransform.inbetween(1)",
                "hotkey":".",
                "alt":1,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"RemoveInbetween",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.keyTransform.inbetween(-1)",
                "hotkey":",",
                "alt":1,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"InbetweenUI",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.keyTransform.inbetweenUI()",
                "hotkey":"<",
                "alt":1,
                "ctl":1,
                "toolTip":"A GUI to help timing keys"
                },{
                "name":"CropTimelineAnimation",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.cropTimelineAnimation()",
                "hotkey":"X",
                "alt":1,
                "ctl":1,
                "toolTip":"Delete all keys from timeline but the range selected"
                }]

    blue    = [{
                "name":"FlowTangent",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.tangents.setTangent('flow')",
                "hotkey":"z",
                "alt":1,
                "ctl":1,
                "toolTip":"It is the same command as the one in the aTools bar"
                },{
                "name":"FlowTangentAround",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.tangents.flowAround(2)",
                "hotkey":"Z",
                "alt":1,
                "ctl":1,
                "toolTip":"Will apply Flow Tangent to the selected keys plus two neighbor keys"
                },{
                "name":"AutoTangent",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.tangents.setTangent('auto')",
                "hotkey":"z",
                "alt":0,
                "ctl":0,
                "toolTip":"It is the same command as the one in the aTools bar"
                }]

    purple  = [{
                "name":"alignSelection",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.align.alignSelection()",
                "hotkey":"a",
                "alt":1,
                "ctl":0,
                "toolTip":"Align selection\nSelect the slaves and a master object"
                },{
                "name":"toggleMicroTransform",
                "command":"from host.maya.python.aTools.generalTools.aToolsGlobals import aToolsGlobals as G; G.aToolsBar.microTransform.switch()",
                "hotkey":"m",
                "alt":0,
                "ctl":0,
                "toolTip":"Toggle Micro Transform mode"
                }]

    red     = [{
                "name":"Playblast",
                "command":"from maya import mel; mel.eval('performPlayblast false')",
                "hotkey":"p",
                "alt":1,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"FrameSection",
                "command":"from host.maya.python.aTools.commonMods import animMod; animMod.frameSection()",
                "hotkey":"f",
                "alt":1,
                "ctl":0,
                "toolTip":"In the Graph Editor, frame/zoom according to the current timeline range"
                },{
                "name":"FramePlaybackRange",
                "command":"from host.maya.python.aTools.animTools import framePlaybackRange; framePlaybackRange.framePlaybackRangeFn()",
                "hotkey":"f",
                "alt":1,
                "ctl":1,
                "toolTip":"In the Graph Editor, frame/zoom according to the current timeline range"
                },{
                "name":"FilterNonAnimatedCurves",
                "command":"from host.maya.python.aTools.commonMods import animMod; animMod.filterNonAnimatedCurves()",
                "hotkey":"f",
                "alt":0,
                "ctl":1,
                "toolTip":"Hide curves in the Graph Editor that have only keys with the same value"
                },{
                "name":"JumpToSelectedKey",
                "command":"from host.maya.python.aTools.commonMods import animMod; animMod.jumpToSelectedKey()",
                "hotkey":"z",
                "alt":1,
                "ctl":0,
                "toolTip":"In the Graph Editor, will go to the selected key"
                },{
                "name":"CopyKeyframesFromTimeline",
                "command":"from maya import mel; mel.eval('timeSliderCopyKey')",
                "hotkey":"c",
                "alt":1,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"CutKeyframesFromTimeline",
                "command":"from maya import mel; mel.eval('timeSliderCutKey')",
                "hotkey":"x",
                "alt":1,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"PasteKeyframesFromTimeline",
                "command":"from maya import mel; mel.eval('timeSliderPasteKey false')",
                "hotkey":"v",
                "alt":1,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"DeleteKeyframesFromTimeline",
                "command":"from maya import mel; mel.eval('timeSliderClearKey')",
                "hotkey":"d",
                "alt":1,
                "ctl":1,
                "toolTip":"It is what is says"
                },{
                "name":"TogglePanelLayout",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.togglePanelLayout()",
                "hotkey":"`",
                "alt":0,
                "ctl":0,
                "toolTip":"Toggle between graph editor and persp in the main viewport"
                }]

    orange  = [{
                "name":"ToggleRotateMode",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.toggleRotateMode()",
                "hotkey":"e",
                "alt":1,
                "ctl":0,
                "toolTip":"Toggle the rotate tool mode (world, local, gimbal)"
                },{
                "name":"ToggleMoveMode",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.toggleMoveMode()",
                "hotkey":"w",
                "alt":1,
                "ctl":0,
                "toolTip":"Toggle the move tool mode (world, local, object)"
                },{
                "name":"OrientMoveManip",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.orientMoveManip()",
                "hotkey":"W",
                "alt":0,
                "ctl":1,
                "toolTip":"Orient the move tool axis to the local axis of the last selected object"
                },{
                "name":"CameraOrientMoveManip",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.cameraOrientMoveManip()",
                "hotkey":"W",
                "alt":1,
                "ctl":1,
                "toolTip":"Toggle the move tool mode (world, local, object)"
                },{
                "name":"ToggleGeometry",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.toggleObj(['polymeshes', 'nurbsSurfaces'])",
                "hotkey":"G",
                "alt":0,
                "ctl":0,
                "toolTip":"Show or hide polygons"
                },{
                "name":"ToggleNurbCurves",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.toggleObj(['nurbsCurves'])",
                "hotkey":"N",
                "alt":0,
                "ctl":0,
                "toolTip":"Show or hide nurb curves"
                },{
                "name":"ToggleLocators",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.toggleObj(['locators'])",
                "hotkey":"L",
                "alt":0,
                "ctl":0,
                "toolTip":"Show or hide locators"
                },{
                "name":"CameraViewMode",
                "command":"from host.maya.python.aTools.commonMods import utilMod; utilMod.cameraViewMode()",
                "hotkey":"C",
                "alt":0,
                "ctl":1,
                "toolTip":"Shows only polygons"
                },{
                "name":"AnimViewportViewMode",
                "command":"from host.maya.python.aTools.commonMods import utilMod; utilMod.animViewportViewMode()",
                "hotkey":"V",
                "alt":0,
                "ctl":1,
                "toolTip":"Shows only polygons and nurb curves"
                }]

    gray    = [{
                "name":"setThreePanelLayout",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.setThreePanelLayout()",
                "hotkey":"3",
                "alt":0,
                "ctl":1,
                "toolTip":"Set layout with 3 panels - camera, perspective and graph editor. Sets a couple of other attributes to the perspective camera."
                },{
                "name":"UnselectChannelBox",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.unselectChannelBox()",
                "hotkey":"C",
                "alt":1,
                "ctl":1,
                "toolTip":"Unselect channels in the channel box\nGood when you want to show all channels keys in the timeline"
                },{
                "name":"NextFrame",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.goToKey('next', 'frame')",
                "hotkey":".",
                "alt":1,
                "ctl":0,
                "toolTip":"Go to next frame without saving the undo state and refreshes in background, \nwhich means you can jump several frames way faster without waiting rigs refresh on every frame"
                },{
                "name":"NextKeyframe",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.goToKey('next')",
                "hotkey":".",
                "alt":0,
                "ctl":0,
                "toolTip":"Go to next keyframe without saving the undo state and refreshes in background, \nwhich means you can jump several frames way faster without waiting rigs refresh on every frame"
                },{
                "name":"PrevFrame",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.goToKey('previous', 'frame')",
                "hotkey":",",
                "alt":1,
                "ctl":0,
                "toolTip":"Go to previous frame without saving the undo state and refreshes in background, \nwhich means you can jump several frames way faster without waiting rigs refresh on every frame"
                },{
                "name":"PrevKeyframe",
                "command":"from host.maya.python.aTools.commonMods import commandsMod; commandsMod.goToKey('previous')",
                "hotkey":",",
                "alt":0,
                "ctl":0,
                "toolTip":"Go to previous keyframe without saving the undo state and refreshes in background, \nwhich means you can jump several frames way faster without waiting rigs refresh on every frame"
                },{
                "name":"GraphEditor",
                "command":"from maya import mel; mel.eval('tearOffPanel \\\"Graph Editor\\\" \\\"graphEditor\\\" true;')",
                "hotkey":"`",
                "alt":0,
                "ctl":1,
                "toolTip":"Open the Graph Editor"
                },{
                "name":"Outliner",
                "command":"from maya import mel; mel.eval('tearOffPanel \\\"Outliner\\\" \\\"outlinerPanel\\\" false;')",
                "hotkey":"o",
                "alt":0,
                "ctl":0,
                "toolTip":"Open the Outliner"
                }]




    return [yellow, green, blue, purple, red, orange, gray]




