import maya.cmds as mc


def oneCurveGrid(rezx=10, rezy=10, scalex=1, scaley=1):

    points = []

    sx = 1.0 / (rezx - 1)
    sy = 1.0 / (rezy - 1)

    for i in range(rezx / 2):

        for j in range(rezy):
            points.append(
                [(2.0 * i * sx - 0.5) * scalex, (j * sy - 0.5) * scaley, 0]
            )
        for j in reversed(range(rezy)):
            points.append(
                [
                    ((2.0 * i + 1) * sx - 0.5) * scalex,
                    (j * sy - 0.5) * scaley,
                    0
                ]
            )

    for i in range(rezy / 2):
        for j in reversed(range(rezx)):
            points.append(
                [
                    (j * sx - 0.5) * scalex,
                    (i * 2.0 * sy - 0.5) * scaley,
                    0
                ]
            )
        for j in range(rezx):
            points.append(
                [
                    (j * sx - 0.5) * scalex,
                    ((i * 2.0 + 1) * sy - 0.5) * scaley,
                    0
                ]
            )

    for i in reversed(range(rezx)):
        points.append(
            [((i * sx - 0.5) * scalex), ((i * sx - 0.5) * scaley), 0]
        )

    return points


def createZDistanceTool():
    """Creates controllers to help with the focus distance.
    Plugs into 'focusDistance' of camera shape
    """

    # choose cam

    selection = mc.ls(sl=True)

    chosenCamera = False

    if len(selection) > 0:
        selShp = (selection[0], mc.listRelatives(selection[0], s=True))[
            mc.nodeType(selection[0]) == "transform"
        ]  # gives us the shape
        if mc.nodeType(selShp) == "camera":
            chosenCamera = selShp
    else:
        currentPanel = mc.getPanel(withFocus=True)
        if mc.getPanel(typeOf=currentPanel) == "modelPanel":
            chosenCamera = mc.modelPanel(currentPanel, q=True, cam=True)
            chosenCamera = mc.listRelatives(chosenCamera, s=True)

    if not chosenCamera:
        mc.warning("Select camera or run in a perspective viewport")
    else:

        isMaxwell = (
            1
            if mc.getAttr("defaultRenderGlobals.currentRenderer") == "maxwell"
            else 0
        )
        camObj = mc.listRelatives(chosenCamera, p=1)[0]
        camShape = chosenCamera[0]

        rendererText = [
            "No specific renderer found, plugging in:\n'"
            + camShape
            + ".focusDistance'",
            "Maxwell render detected, plugging in:\n'"
            + camShape +
            ".mxFocusDistance'",
        ]

        confirm = mc.confirmDialog(
            title="Confirm",
            message=rendererText[isMaxwell]
            + '\n\nCreate a z-depth controller for "'
            + camObj
            + '" ?',
            button=["Yes", "No"],
            defaultButton="Yes",
            cancelButton="No",
            dismissString="No",
        )
        if confirm == "Yes":

            # spaghetti code below

            # floating locator system

            floatingZLoc = mc.curve(
                p=[
                    [-0.319, -0.001, 0.0],
                    [0.621, 0.94, 0.0],
                    [-1.0, 0.94, 0.0],
                    [-1.0, 1.06, 0.0],
                    [1.392, 1.06, 0.0],
                    [-0.608, -0.94, 0.0],
                    [1.0, -0.94, 0.0],
                    [1.0, -1.06, 0.0],
                    [-1.379, -1.06, 0.0],
                    [-0.319, -0.001, 0.0],
                    [0.0, 0.0, 0.0],
                    [-0.233, -0.233, -0.233],
                    [0.233, 0.233, 0.233],
                    [0.0, 0.0, 0.0],
                    [-0.233, -0.233, 0.233],
                    [0.233, 0.233, -0.233],
                    [0.0, 0.0, 0.0],
                    [-0.233, 0.233, -0.233],
                    [0.233, -0.233, 0.233],
                    [0.0, 0.0, 0.0],
                    [0.233, -0.233, -0.233],
                    [-0.233, 0.233, 0.233],
                ],
                d=1,
                n=camObj + "_zDepth_FloatCtrl",
            )
            projCurve = mc.curve(
                p=[[0, 0, 0], [0, 0, 1000]], d=1, n=camObj + "_longCurve"
            )  # create a curve to project our locator on
            pc = mc.parentConstraint(camObj, projCurve, mo=False)[
                0
            ]  # curve follows camera
            mc.setAttr(pc + ".target[0].targetOffsetRotateY", 180)
            cameraLocator = mc.spaceLocator(n=camObj + "_camLocator")[
                0
            ]  # locator on camera to get world position later
            mc.pointConstraint(camObj, cameraLocator, mo=False)
            floatingLocator = mc.spaceLocator(n=camObj + "_floatLocator")[
                0
            ]  # locator to get floating controller world pos
            mc.parent(floatingLocator, floatingZLoc)
            projectionLocator = mc.spaceLocator(n=camObj + "_projLocator")[
                0
            ]  # locator to project on curve

            nPoc = mc.createNode("nearestPointOnCurve")
            mc.connectAttr(
                mc.listRelatives(
                    floatingLocator,
                    s=True
                )[0] + ".worldPosition",
                nPoc + ".inPosition",
                f=True,
            )
            mc.connectAttr(
                mc.listRelatives(projCurve, s=True)[0] + ".worldSpace",
                nPoc + ".inputCurve",
                f=True,
            )
            mc.connectAttr(
                nPoc + ".position",
                projectionLocator + ".translate",
                f=True
            )

            db = mc.createNode("distanceBetween")
            mc.connectAttr(
                mc.listRelatives(
                    projectionLocator,
                    s=True
                )[0] + ".worldPosition",
                db + ".point1",
            )
            mc.connectAttr(
                mc.listRelatives(cameraLocator, s=True)[0] + ".worldPosition",
                db + ".point2",
            )

            # end result locator and grid

            resultLocator = mc.spaceLocator(n=camObj + "resultLocator")[0]
            resultGrid = mc.curve(
                p=oneCurveGrid(14, 8, 3.84, 2.16),
                d=1,
                n=camObj + "_resultGrid"
            )
            mc.setAttr(resultGrid + ".tz", keyable=False, channelBox=False)
            mc.setAttr(
                resultGrid + ".visibility",
                keyable=False,
                channelBox=False
            )

            # camera based system

            cameraGrid = mc.curve(
                p=oneCurveGrid(28, 16, 8, 4.5), d=1, n=camObj + "_zDepth_Ctrl"
            )  # create a grid to visualize standard focus distance z
            cameraGridNull = mc.group(em=True, n=camObj + "_zDepth_Ctrl_ZERO")
            mc.parent(cameraGrid, cameraGridNull)
            mc.parent(resultLocator, cameraGridNull)
            mc.parent(resultGrid, cameraGridNull)
            pc2 = mc.parentConstraint(projCurve, cameraGridNull, mo=False)[0]

            # grab existing zdepth focus distance,
            # with renderer specific options (maxwell for now)

            currentDistance = 5.0

            if isMaxwell:
                currentDistance = mc.getAttr(camShape + ".mxFocusDistance")
                mc.setAttr(camShape + ".mxUseFocusDistance", 1)
            else:
                currentDistance = mc.getAttr(camShape + ".focusDistance")

            mc.setAttr(cameraGrid + ".tz", currentDistance)

            # choice system

            sr = mc.createNode("setRange")
            sr2 = mc.createNode("setRange")

            mc.setAttr(sr + ".oldMaxX", 1)
            mc.setAttr(sr + ".oldMaxY", 1)
            mc.setAttr(sr + ".maxY", 0)
            mc.setAttr(sr + ".minY", 1)

            mc.setAttr(sr2 + ".maxX", 1)
            mc.setAttr(sr2 + ".maxY", 0)
            mc.setAttr(sr2 + ".minY", 1)
            mc.setAttr(sr2 + ".oldMaxX", 0.001)
            mc.setAttr(sr2 + ".oldMinY", 0.999)
            mc.setAttr(sr2 + ".oldMaxY", 1)

            mc.connectAttr(db + ".distance", sr + ".maxX", f=1)
            mc.connectAttr(cameraGrid + ".tz", sr + ".minX", f=1)
            mc.connectAttr(
                sr + ".outValue.outValueX",
                resultLocator + ".tz",
                f=True
            )

            arrow = mc.annotate(resultLocator, p=(0, 0, 0))
            arrowObj = mc.listRelatives(arrow, p=1)[0]
            arrowObj = mc.rename(arrowObj, camObj + "_zDistance")
            arrow = mc.listRelatives(arrowObj, s=1)[0]
            mc.parent(arrowObj, cameraGridNull, r=True)

            md = mc.createNode(
                "multiplyDivide"
            )  # ridiculous hack to force annoation update
            mc.connectAttr(camObj + ".tx", md + ".input2.input2X")
            mc.connectAttr(sr + ".outValue.outValueX", md + ".input2.input2Y")
            mc.connectAttr(floatingZLoc + ".tx", md + ".input2.input2Z")
            mc.connectAttr(
                md + ".output", mc.listRelatives(arrow, p=1)[0] + ".translate"
            )

            # mostly controls and cosmetic stuff

            for o in (
                projCurve,
                resultLocator,
                floatingLocator,
                projectionLocator,
                cameraLocator,
                pc2,
            ):
                mc.setAttr(o + ".visibility", False)

            for o in (cameraGrid, arrowObj):
                for p in (
                    "tx", "ty", "tz", "sx", "sy", "sz", "rx", "ry", "rz"
                ):
                    mc.setAttr(o + "." + p, keyable=False, channelBox=False)

            mc.setAttr(cameraGrid + ".tz", keyable=True, channelBox=False)
            mc.setAttr(cameraGrid + ".tx", lock=True)
            mc.setAttr(cameraGrid + ".ty", lock=True)

            mc.addAttr(arrowObj, ln="focusDistance")
            mc.setAttr(
                arrowObj + ".focusDistance",
                e=0,
                keyable=False,
                channelBox=True
            )
            mc.connectAttr(
                sr + ".outValue.outValueX", arrowObj + ".focusDistance", f=True
            )
            mc.connectAttr(
                sr + ".outValue.outValueX", resultGrid + ".tz", f=True
            )
            mc.connectAttr(
                sr2 + ".outValue.outValueX", resultGrid + ".visibility", f=True
            )
            mc.connectAttr(
                sr2 + ".outValue.outValueY", cameraGrid + ".visibility", f=True
            )

            mc.setAttr(resultGrid + ".overrideEnabled", 1)
            mc.setAttr(resultGrid + ".overrideColor", 1)

            mc.addAttr(
                arrowObj, ln="useFloatingLocator", dv=0.0, min=0.0, max=1.0
            )
            mc.setAttr(
                arrowObj + ".useFloatingLocator",
                e=1,
                keyable=True,
                channelBox=False
            )
            mc.connectAttr(
                arrowObj + ".useFloatingLocator", sr + ".valueX", f=True
            )
            mc.connectAttr(
                arrowObj + ".useFloatingLocator", sr + ".valueY", f=True
            )
            mc.connectAttr(
                arrowObj + ".useFloatingLocator", sr + ".valueZ", f=True
            )
            mc.connectAttr(
                arrowObj + ".useFloatingLocator", sr2 + ".valueX", f=True
            )
            mc.connectAttr(
                arrowObj + ".useFloatingLocator", sr2 + ".valueY", f=True
            )

            mc.setAttr(arrow + ".overrideEnabled", 1)
            mc.setAttr(arrow + ".overrideColor", 17)

            mc.setAttr(cameraGrid + ".overrideEnabled", 1)
            mc.setAttr(cameraGrid + ".overrideColor", 12)
            mc.setAttr(floatingZLoc + ".overrideEnabled", 1)
            mc.setAttr(floatingZLoc + ".overrideColor", 12)

            zFocusGroup = mc.group(em=True, n=camObj + "_zFocusGroup")
            mc.parent(
                cameraGridNull,
                floatingZLoc,
                projCurve,
                projectionLocator,
                cameraLocator,
                zFocusGroup,
            )

            if isMaxwell:
                mc.connectAttr(
                    resultLocator + ".tz", camShape + ".mxFocusDistance", f=1
                )
            mc.connectAttr(
                resultLocator + ".tz", camShape + ".focusDistance", f=1
            )

            mc.select(arrowObj)


# createZDistanceTool()
