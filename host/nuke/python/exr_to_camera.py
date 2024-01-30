# -*- coding: utf-8 -*-

""" Create a 3D camera based on EXR metadata.

    As Maya does not export all necessary data, this script is dependent to
    arnold maya>plugins_python>arnold_custom_metadata.py
"""

import os
import math
import re
import nuke


def getMetadataMatrix(meta_list):
    """ Get a matrix4 from the data list
    """
    m = nuke.math.Matrix4()
    try:
        for i in range(0, 16):
            m[i] = meta_list[i]
    except Exception:
        m.makeIdentity()
    return m


def run():
    """ Bake Camera from exr info
    """
    selected_node = nuke.selectedNode()

    if not selected_node:
        print("Please select a Read node.")
        return

    if nuke.getNodeClassName(selected_node) != 'Read':
        nuke.message('Please select a read node')
        print('Please select a read node')
        return
    metaData = selected_node.metadata()
    reqFields = ['exr/%s' % i for i in ('worldToCamera', 'worldToScreen')]
    if not set(reqFields).issubset(metaData):
        nuke.message('no basic matrices for camera found')
        print('no basic matrices for camera found')
        return
    else:
        print('found needed data')
    # imageWidth = metaData['input/width']
    # imageHeight = metaData['input/height']

    # generate camera name
    camera_name = "Camera"
    file_name = os.path.basename(selected_node.knob('file').value())
    regex_result = re.findall(
        r"(^[0-9]{3}_[0-9]{4})\w+_(v[0-9]{3})",
        file_name
    )
    if regex_result:
        camera_name = "Camera {} {}".format(
            regex_result[0][0],
            regex_result[0][1]
        )

    camera_fov = metaData['exr/CameraFov']

    # aspectRatio = float(imageWidth)/float(imageHeight)
    hAperture = metaData['exr/custom/CameraApertureHorizontal']
    vAperture = metaData['exr/custom/CameraApertureVertical']

    # get additional stuff
    first = selected_node.firstFrame()
    last = selected_node.lastFrame()
    ret = nuke.getFramesAndViews(
        'Create Camera from Metadata', '%s-%s' % (first, last)
    )
    if not ret:
        return

    frameRange = nuke.FrameRange(ret[0])
    camViews = (ret[1])

    for act in camViews:
        cam = nuke.nodes.Camera(name="{} {}".format(camera_name, act))
        # enable animated parameters
        cam['useMatrix'].setValue(True)
        cam['haperture'].setValue(hAperture)
        cam['vaperture'].setValue(vAperture)

        for k in ('focal', 'matrix', 'win_translate', 'focal_point', 'fstop'):
            cam[k].setAnimated()

        task = nuke.ProgressTask(
            'Baking camera from meta data in %s' % selected_node.name()
        )

        for curTask, frame in enumerate(frameRange):
            if task.isCancelled():
                break
            task.setMessage('processing frame %s' % frame)
            # get the data out of the exr header
            wTC = selected_node.metadata('exr/worldToCamera', frame, act)

            focusDistance = selected_node.metadata(
                'exr/custom/focusDistance', frame, act)
            fStop = selected_node.metadata('exr/custom/fStop', frame, act)
            # set the lenshiift if additional metadata is available or
            # manage to calculate it from the toNDC matrix
            # cam['win_translate'].setValue( lensShift, 0 , frame )

            focal = hAperture / (2 * math.tan(math.radians(camera_fov)/2.0))
            cam['focal'].setValueAt(float(focal), frame)
            cam['focal_point'].setValueAt(float(focusDistance), frame)
            cam['fstop'].setValueAt(float(fStop), frame)
            # 36 / (2 * tan(radians([metadata -n Read1 exr/CameraFov] / 2)))

            # do the matrix math for rotation and translation
            matrixList = wTC
            camMatrix = getMetadataMatrix(wTC)

            flipZ = nuke.math.Matrix4()
            flipZ.makeIdentity()
            flipZ.scale(1, 1, -1)

            transposedMatrix = nuke.math.Matrix4(camMatrix)
            transposedMatrix.transpose()
            transposedMatrix = transposedMatrix*flipZ
            invMatrix = transposedMatrix.inverse()

            for i in range(0, 16):
                matrixList[i] = invMatrix[i]

            for i, v in enumerate(matrixList):
                cam['matrix'].setValueAt(v, frame, i)
            # UPDATE PROGRESS BAR
            task.setProgress(
                int(float(curTask) / frameRange.frames() * 100)
            )
