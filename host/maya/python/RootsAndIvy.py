# F. Hiba, C. Mendes, B. Lefebvre, P. Hubert
import maya.api.OpenMaya as om
import maya.cmds as cmds
from math import radians, sin, cos
from random import gauss, random, uniform, shuffle
from copy import copy

# 4 utilities function related to transformations


# give the quaternion corresponding to the rottion from vector 1 to vector 2
def getQuaternion(vector1=om.MVector(0, 0, 0), vector2=om.MVector(0, 0, 0)):
    dot = vector1 ^ vector2  # get axis
    dot = dot.normalize()  # normalize axis
    angle = vector1.angle(vector2)  # get angle (in rad)

    quaternion = om.MQuaternion(
        dot[0] * sin(angle / 2),
        dot[1] * sin(angle / 2),
        dot[2] * sin(angle / 2),
        cos(angle / 2),
    )  # convert. to quaternion

    return quaternion


# convert axis + angle to quaternion
def toQuaternion(axe=om.MVector(0, 1, 0), angle=0):
    angle = radians(angle)
    quaternion = om.MQuaternion(
        axe[0] * sin(angle / 2),
        axe[1] * sin(angle / 2),
        axe[2] * sin(angle / 2),
        cos(angle / 2),
    )
    return quaternion


def getMatrix(MVectorx, MVectory, MVectorz, MVectorPos):
    matrix = om.MMatrix(
        [
            MVectorx.x,
            MVectorx.y,
            MVectorx.z,
            0,
            MVectory.x,
            MVectory.y,
            MVectory.z,
            0,
            MVectorz.x,
            MVectorz.y,
            MVectorz.z,
            0,
            MVectorPos.x,
            MVectorPos.y,
            MVectorPos.z,
            1,
        ]
    )
    return matrix


# return closest point on the mesh and the corresponding normal.
# Result as [mVector,mVector]
def getPointNormal(mMesh, point):
    point = om.MPoint(point)
    result = mMesh.getClosestPointAndNormal(point, om.MSpace.kWorld)
    res0 = om.MVector(result[0])
    result = [res0, result[1]]
    return result


def getClosestVertex(mayaMesh, mVector):
    selectionList = om.MSelectionList()
    selectionList.add(mayaMesh)
    dPath = selectionList.getDagPath(0)
    mMesh = om.MFnMesh(dPath)
    ID = mMesh.getClosestPoint(om.MPoint(mVector), space=om.MSpace.kWorld)[
        1
    ]  # getting closest face ID
    list = cmds.ls(
        cmds.polyListComponentConversion(
            mayaMesh + ".f[" + str(ID) + "]", ff=True, tv=True
        ),
        flatten=True,
    )  # face's vertices list
    # setting vertex [0] as the closest one
    d = mVector - om.MVector(cmds.xform(list[0], t=True, ws=True, q=True))
    smallerDist2 = (
        d.x * d.x + d.y * d.y + d.z * d.z
    )  # using distance squared to compare distance
    closest = list[0]
    # iterating from vertex [1]
    for i in range(1, len(list)):
        d = mVector - om.MVector(cmds.xform(list[i], t=True, ws=True, q=True))
        d2 = d.x * d.x + d.y * d.y + d.z * d.z
        if d2 < smallerDist2:
            smallerDist2 = d2
            closest = list[i]
    return closest


def getLastVertex(mayaMesh):
    list = cmds.ls(
        cmds.polyListComponentConversion(mayaMesh, tv=True),
        flatten=True
    )
    last = list[-1]
    return last


def getFirstVertex(mayaMesh):
    list = cmds.ls(
        cmds.polyListComponentConversion(mayaMesh, tv=True),
        flatten=True
    )
    first = list[0]
    return first


# CLASSES

# custom mesh class. Used to point open maya's mMesh object
# (will be mesh.mMesh)
class Mesh:
    def setmMesh(self, mayamesh):
        self.mayamesh = mayamesh
        self.refMesh = cmds.duplicate(self.mayamesh, n="referenceMesh")[0]
        cmds.parent(self.refMesh, grp.grp)
        cmds.polySetToFaceNormal(self.refMesh)
        cmds.hide(self.refMesh)
        selectionList = om.MSelectionList()
        selectionList.add(self.refMesh)
        dPath = selectionList.getDagPath(0)
        self.mMesh = om.MFnMesh(dPath)

    def reset(self):
        self.refMesh = cmds.duplicate(self.mayamesh, n="referenceMesh")[0]
        cmds.parent(self.refMesh, grp.grp)
        cmds.polySetToFaceNormal(self.refMesh)
        cmds.hide(self.refMesh)
        selectionList = om.MSelectionList()
        selectionList.add(self.refMesh)
        dPath = selectionList.getDagPath(0)
        self.mMesh = om.MFnMesh(dPath)

    # Add is used to add a copy of a given mesh to the reference.
    # Used to update ref. mesh in real time.
    def add(self, mayamesh):
        self.toAdd = cmds.duplicate(mayamesh, n="referenceMesh")[0]
        self.refMesh = cmds.polyUnite([self.refMesh, self.toAdd], ch=False)[0]
        cmds.parent(self.refMesh, grp.grp)
        cmds.hide(self.refMesh)
        selectionList = om.MSelectionList()
        selectionList.add(self.refMesh)
        dPath = selectionList.getDagPath(0)
        self.mMesh = om.MFnMesh(dPath)


# class to point locator
class Locator:
    def setup(self, locator):
        self.pos = om.MVector(cmds.xform(
            locator,
            query=True,
            t=True,
            worldSpace=True
        ))


# custom group class. Used to store generated geo.
class Grp:
    def __init__(self):
        self.grp = cmds.group(em=True, n="generation")

    def reset(self):
        if hasattr(self, "grp"):
            if cmds.objExists(self.grp):
                cmds.delete(self.grp)
                print("deleted")
        self.grp = cmds.group(em=True, n="generation")

    def unite(self):
        geo = cmds.polyUnite(
            cmds.listRelatives(self.grp),
            ch=False,
            n="Geometry"
        )
        return geo


# custom Vector class. Vectors associate : Vector direction
# (as openmaya MVector), Vector position (as om MVector),
# corresponding normal and point on mesh (both as om MVector), and
# corresponding NEXT normal and Point (Normal an Point at vector's extremity).
# Theses last parameters are used to calculate next vector's position
class Vector:
    def __init__(
        self,
    ):  # creates a standard Vector. On position 0, value 1 z, normal 1 y
        self.mVector = om.MVector(0, 0, 1) * var.scaleFactor
        self.pos = om.MVector()
        self.mNormal = om.MVector(0, 1, 0)

    # set up the first vector : establish his parameters for a given mesh
    # (mMesh custom class) and a given starting postion(locator custom class).
    def firstSetup(
        self, locator, mMesh
    ):
        # to avoid glitch when used on a allready set up vector
        self.__init__()

        self.pos = locator.pos  # moves vector to locator's position
        result = getPointNormal(mMesh, self.pos)  # get point an normal on mesh
        self.mNormal = result[1]
        # move vector next to the surface. Distance controlled by var.distance.
        self.pos = result[0] + (
            self.mNormal * var.distance
        )
        # get quat. corresponding to the rotation between y axis and
        # the normal on starting point.
        quat = getQuaternion(
            om.MVector(0, 1, 0), self.mNormal
        )
        self.mVector = self.mVector.rotateBy(
            quat
        )  # uses quad to align vector tangent to the surface.

        self.mVector = (
            self.mVector.normalize() * var.scaleFactor
        )  # scale vector's length by var.scaleFactor
        result = getPointNormal(
            mMesh, self.pos + self.mVector
        )  # calculate next point and normal to pass it to the next vector
        self.pointNext = result[0]
        self.mNormalNext = result[1]

    # apply a rotation to a given allready set up vector.
    # Use for first vector setup and for bigger angle variation at divisions
    def startRotation(
        self, mMesh, angle=0.0
    ):
        self.origin = self.mVector
        self.mVector = self.origin.rotateBy(
            toQuaternion(self.mNormal, angle)
        )  # modify start angle

        # redefine other parameters
        self.mVector = self.mVector.normalize() * var.scaleFactor
        result = getPointNormal(mMesh, self.pos + self.mVector)
        self.pointNext = result[0]
        self.mNormalNext = result[1]

    # Setup method sets up a vector from a given previous vector.
    # Use to align one vector after the other.
    def setup(
        self, mMesh, vector, distance
    ):  # vector must be of type : custom Vector class.
        self.mVector = vector.mVector  # get previous vector's parameter

        self.pos = vector.pos + vector.mVector  # get his new position
        self.mNormal = (
            vector.mNormalNext
        )  # get his normal and point (calculated by previous vector)
        self.point = vector.pointNext

        # apply a rotation. Random variation based on gauss distrib.
        # with variance = var.angleAmplitude
        self.mVector = self.mVector.rotateBy(
            toQuaternion(self.mNormal, gauss(0, var.angleAmplitude))
        )

        # calculate next normal and point
        result = getPointNormal(mMesh, self.pos + self.mVector)
        self.pointNext = result[0]
        self.mNormalNext = result[1]

        # adjust vector with parameters : next point and next normal.
        # Normalize en rescale to keep a constant length.
        self.mVector = (
            self.pointNext + (self.mNormalNext * distance) - self.pos
        ).normalize() * var.scaleFactor

    # mehtod similar to setup without angle variation and without correction.
    # Used to obtain vector colinear to the previous one.
    # Used at divisions to avoid extrusion glitch.
    def setupStraight(self, mMesh, vector, distance):
        self.mVector = vector.mVector  # get previous vector's parameter

        self.pos = vector.pos + vector.mVector  # get his new position
        self.mNormal = (
            vector.mNormalNext
        )  # get his normal and point (calculated by previous vector)
        self.point = vector.pointNext

        result = getPointNormal(
            mMesh, self.pos + self.mVector
        )  # calculate next normal and point
        self.pointNext = result[0]
        self.mNormalNext = result[1]

    # creates a new point on the bezier curve 'bezier' corresponding to
    # self.pos. Used to store points during generation loop.
    def display(self, bezier):
        cmds.curve(bezier, append=True, p=(self.pos + self.mVector))

    # invert vector. Used to create the reverse branch on first iteration
    # (to fill hole)
    def invert(self):
        self.copy = copy(self)
        self.pos = self.copy.pos + self.copy.mVector
        self.mVector = -(self.copy.mVector)


# branch class is used to create vectors un loop and store them as a
# maya bezier curve. Has a fonction to create geo too.
# firstVector and lastVector are first and last vectors of the branch.
# first vector used for extrusion and last vector used to align next branch.
class Branch:

    # make a branch from a single vector. Used for first vector.
    def firstSetup(self, vector):
        self.bezier = cmds.curve(p=vector.pos, d=1)  # creates a curve
        # parent to grp.grp (custom group class)
        cmds.parent(self.bezier, grp.grp)
        vector.display(self.bezier)  # add point
        self.firstVector = copy(
            vector
        )  # fistvector used to set up extrusion in makeGeo
        self.lastVector = self.firstVector

    # similar to firstSetup but without creating geo.
    # and inverting first vector. Used to fill hole at strat
    # (expand in both extremities)
    def firstSetupInv(self, branch):
        self.firstVector = copy(
            branch.firstVector
        )  # fistvector used to set up extrusion in makeGeo
        self.lastVector = self.firstVector
        self.lastVector.invert()
        self.geo = branch.geo

    # Setup a branch for a given previous branch.
    # Store points in a bezier curve. use vector.setup in a loop
    # creates 2 vectors before starting the loop :
    # the first one is a straight one (to avoid extrusion glitch)
    # the second one gets an extra rotation to make branches
    # expand at division.
    def setup(self, branch, iterations, close=False):
        i = 0
        self.bezier = cmds.curve(
            p=branch.lastVector.pos + branch.lastVector.mVector, d=2
        )  # creates curve
        cmds.parent(self.bezier, grp.grp)

        # first vector
        self.vector0 = Vector()  # creates vector0
        self.vector0.setupStraight(
            myMesh.mMesh, branch.lastVector, distance=var.distance
        )  # set up vector0
        self.vector0.display(self.bezier)  # add point to the curve
        self.firstVector = copy(self.vector0)  # store firstVector in memory

        # second vector = the one affected by the
        # "rotation at division" factor.
        # creates and sets up a second vector (not straight)
        self.vector1 = Vector()
        self.vector1.setup(myMesh.mMesh, self.vector0, distance=var.distance)
        self.vector1.startRotation(
            mMesh=myMesh.mMesh, angle=gauss(0, var.angleAmplitudeDiv)
        )  # rotates it for a bigger offset
        self.vector1.display(self.bezier)
        self.vector0 = self.vector1

        # loop
        while i < iterations - 2:
            # close is used for last branches.
            # The vector as to be progressively closer to match with
            # the extrusion witch will have a reduced diamater.
            if (close is True):
                self.vector1.setup(
                    myMesh.mMesh,
                    self.vector0,
                    distance=var.distance * (1 - i / (iterations - 2)),
                )
            else:
                self.vector1.setup(
                    myMesh.mMesh,
                    self.vector0,
                    distance=var.distance
                )
                leaves.append(copy(self.vector1))
            self.vector1.display(self.bezier)
            self.vector0 = self.vector1
            i = i + 1

        self.lastVector = self.vector1  # point last vector

    # makeGeo extrude the curve. Close argument used for extremities.
    def makeGeo(self, branch=0, close=False, inv=False, first=False):

        if first is True:
            z = self.firstVector.mVector
            y = self.firstVector.mNormal
            x = (y ^ z).normal()
            y = z ^ x
            mat1 = getMatrix(
                x.normal(),
                y.normal(),
                z.normal(),
                self.firstVector.pos
            )

            sliceTest = cmds.circle(r=var.radius, s=8)[
                0
            ]  # creating the "slice" circle for extrusion
            # rotating and moving it to match curve
            cmds.xform(sliceTest, matrix=mat1)

        else:
            if inv is True:
                vertex = om.MVector(cmds.xform(
                        getFirstVertex(branch.geo),
                        t=True,
                        ws=True,
                        q=True
                    ))
            else:
                vertex = om.MVector(cmds.xform(
                    getLastVertex(branch.geo),
                    t=True,
                    ws=True,
                    q=True
                ))
            x = (vertex - self.firstVector.pos).normal()
            z = self.firstVector.mVector.normal()
            y = z ^ x

            # cmds.curve(p=[self.firstVector.pos,self.firstVector.pos+x],d=1)

            mat1 = getMatrix(
                x.normal(),
                y.normal(),
                z.normal(),
                self.firstVector.pos
            )

            sliceTest = cmds.circle(r=var.radius, s=8)[
                0
            ]  # creating the "slice" circle for extrusion
            # rotating and moving it to match curve
            cmds.xform(sliceTest, matrix=mat1)

        if close is True:
            self.nurbs = cmds.extrude(
                sliceTest,
                self.bezier,
                po=0,
                upn=False,
                scale=0
            )[0]  # [0] : extrude returns a list
        else:
            self.nurbs = cmds.extrude(
                sliceTest,
                self.bezier,
                po=0,
                upn=False,
                scale=1
            )[0]

        self.geo = cmds.nurbsToPoly(self.nurbs, f=3, pt=1, mnd=True)[0]
        cmds.delete(self.nurbs)
        cmds.parent(self.geo, grp.grp)

        cmds.delete(self.bezier)
        cmds.delete(sliceTest)

        return self.geo


# Branchlist class is used to makes several branches.
# It stores the list of the last branches and
# uses this list to creates new branches at their extremities
class Branchlist:
    def __init__(self):
        self.list = []
        self.listClose = []

    def initialize(self, branch, branchInv):
        self.list = [branch]
        self.branchInv = branchInv

        # print self.branchInv.lastVector.mVector
        # print self.list[0].lastVector.mVector

    def iterate(self, number=1):
        # Check if this is the first iteration.
        # If yes, sets up an extra branch to fill hole.
        if var.firstIteration is True:
            print("first")
            var.firstIteration = False
            branchI = Branch()
            branchI.setup(
                branch=self.branchInv,
                iterations=var.iterations
                + (var.iterations - 1) * var.iterationsVar * uniform(-1, 1),
                close=True,
            )
            geo = copy(
                branchI.makeGeo(
                    branch=self.branchInv, first=False, inv=True, close=True
                )
            )
            myMesh.add(geo)
            cmds.refresh()

        # Next block is the loop generation algorithm
        n = 0
        while n < number:
            n = n + 1
            self.listClose = []
            shuffle(self.list)
            self.templist = []
            self.delIndex = []
            if len(self.list) > 1:
                for i in range(1, len(self.list)):
                    if random() < var.closeRate:
                        self.listClose.append(copy(self.list[i]))
                        self.delIndex.append(i)

                if len(self.delIndex) > 0:
                    for i in sorted(self.delIndex, reverse=True):
                        del self.list[i]
            for branch in self.list:
                branch1 = Branch()
                branch1.setup(
                    branch=branch,
                    iterations=var.iterations
                    + (var.iterations - 1)
                    * var.iterationsVar * uniform(-1, 1),
                )
                geo1 = copy(branch1.makeGeo(branch=branch))
                self.templist.append(branch1)
                cmds.refresh()
                if random() < var.divRate:
                    branch2 = Branch()
                    branch2.setup(
                        branch=branch,
                        iterations=var.iterations
                        + (var.iterations - 1)
                        * var.iterationsVar * uniform(-1, 1),
                    )
                    geo2 = copy(branch2.makeGeo(branch=branch))
                    myMesh.add(geo2)
                    self.templist.append(branch2)
                    cmds.refresh()
                myMesh.add(geo1)
            self.list = copy(self.templist)
            for branch in self.listClose:
                branch1 = Branch()
                branch1.setup(
                    branch=branch,
                    iterations=var.iterations
                    + (var.iterations - 1)
                    * var.iterationsVar * uniform(-1, 1),
                    close=True,
                )
                geo = copy(branch1.makeGeo(branch=branch, close=True))
                myMesh.add(geo)
                cmds.refresh()

    def close(self):
        for branch in self.list:
            branch1 = Branch()
            branch1.setup(
                branch=branch,
                iterations=var.iterations
                + (var.iterations - 1) * var.iterationsVar * uniform(-1, 1),
                close=True,
            )
            geo = copy(branch1.makeGeo(branch=branch, close=True))
            myMesh.add(geo)
            cmds.refresh()


# variables class. Is used to create a single object
# representing all the variables.
class Var:
    def __init__(self):
        self.scaleFactor = 1
        self.radius = 0.5
        self.penetration = 0
        self.distance = self.radius * (1 - self.penetration)
        self.startAngle = 0
        self.angleAmplitude = 30
        self.angleAmplitudeDiv = 45
        self.iterations = 50
        self.iterationsVar = 30
        self.divRate = 0.3
        self.closeRate = 0.2
        self.loopNumber = 1

        self.leafScaleVar = 0.2
        self.leafRot1Var = 15
        self.leavesDensity = 0.4

        self.firstIteration = True

    # updates value based on sliders. Called by slider.
    def update(self):
        self.scaleFactor = cmds.floatSliderGrp(scaleFactor, v=True, query=True)

        self.radius = cmds.floatSliderGrp(radius, v=True, query=True)
        self.penetration = cmds.floatSliderGrp(penetration, v=True, query=True)
        self.distance = self.radius * (1 - self.penetration)

        self.startAngle = cmds.intSliderGrp(startAngle, v=True, query=True)
        self.angleAmplitude = cmds.floatSliderGrp(
            angleAmplitude, v=True, query=True
        )
        self.angleAmplitudeDiv = cmds.floatSliderGrp(
            angleAmplitudeDiv, v=True, query=True
        )
        self.iterations = cmds.intSliderGrp(iterations, v=True, query=True)
        self.iterationsVar = cmds.floatSliderGrp(
            iterationsVar, v=True, query=True
        )
        self.divRate = cmds.floatSliderGrp(divRate, v=True, query=True)
        self.closeRate = cmds.floatSliderGrp(closeRate, v=True, query=True)
        self.loopNumber = cmds.intSliderGrp(loopNumber, v=True, query=True)

        self.leavesScaleVar = cmds.floatSliderGrp(
            leavesScaleVar, v=True, query=True
        )
        self.leavesRot1Var = cmds.intSliderGrp(
            leavesRot1Var, v=True, query=True
        )
        self.leavesDensity = cmds.floatSliderGrp(
            leavesDensity, v=True, query=True
        )

        self.leavesPlacementIntMin = cmds.intSliderGrp(
            leavesPlacementIntMin, v=True, query=True
        )
        self.leavesPlacementIntMax = cmds.intSliderGrp(
            leavesPlacementIntMax, v=True, query=True
        )


# leaves class is used to store a vector list and to place leaves
# along these vectors.
class Leaves:
    def __init__(self):
        self.vectorList = []

    def setMesh(self, mayamesh):

        cmds.xform(mayamesh, piv=(0, 0, 0))
        cmds.makeIdentity(mayamesh, apply=True)
        self.mesh = mayamesh

    def append(self, vector):
        self.vectorList.append(vector)

    def reset(self):
        if hasattr(self, "grp"):
            if cmds.objExists(self.grp):
                print("del")
                cmds.delete(self.grp)
        self.grp = cmds.group(em=True, n="Leaves")
        """cmds.parent (self.grp,grp.grp)"""

    def placeGeo(self):
        for vector in self.vectorList:

            if random() < var.leavesDensity:

                z = vector.mVector.normal()
                x = vector.mNormal
                y = z ^ x
                x = y ^ z
                pos = vector.pos
                mat1 = getMatrix(x, y, z, pos)
                mat2 = getMatrix(x, -y, z, pos)
                leaf = cmds.duplicate(self.mesh)
                loc = cmds.spaceLocator()
                cmds.parent(leaf, loc)
                if uniform(0, 1) > 0.5:
                    cmds.xform(loc, matrix=mat1)  # place on the branch
                else:
                    cmds.xform(loc, matrix=mat2)  # place on the branch

                cmds.move(
                    0.9 * var.radius, 0, 0, leaf, os=True, r=True
                )  # place on the surface
                placementAngle = uniform(
                    var.leavesPlacementIntMin, var.leavesPlacementIntMax
                )
                # place at various angle around Z.
                # Zero angle = leaf orientation follows normal.
                cmds.rotate(
                    0, 0, -placementAngle, loc, os=True, r=True, fo=True
                )

                cmds.rotate(
                    gauss(0, var.leavesRot1Var),
                    gauss(0, var.leavesRot1Var),
                    0,
                    leaf,
                    os=True,
                    r=True,
                    fo=True,
                )  # random rotation

                s = gauss(1, var.leavesScaleVar)
                cmds.scale(s, s, s, leaf, r=True)
                cmds.parent(leaf, world=True)

                cmds.parent(leaf, self.grp)
                cmds.delete(loc)

                cmds.refresh()


# FONCTIONS CALL BY BUTTONS


# update vector with new variables and set it relative to locator.
# Use to tweak the first vector's parameters or to display it after reset.
def updateVector(vector):

    var.update()
    vector.firstSetup(locator=myLocator, mMesh=myMesh.mMesh)
    vector.startRotation(mMesh=myMesh.mMesh, angle=var.startAngle)
    if hasattr(branch0, "bezier"):
        if cmds.objExists(branch0.bezier):
            cmds.delete(branch0.bezier)
    branch0.firstSetup(vector0)

    if hasattr(branch0, "geo"):
        if cmds.objExists(branch0.geo):
            cmds.delete(branch0.geo)
    branch0.makeGeo(first=True)
    branchInv.firstSetupInv(branch0)
    branchlist.initialize(branch0, branchInv)  # put first branch in branchlist


def reset():
    grp.reset()
    myMesh.reset()
    leaves.reset()
    vector0.__init__()
    branch0 = Branch()  # noqa F841
    branchInv = Branch()  # noqa F841
    branchlist = Branchlist()  # noqa F841
    updateVector(vector0)
    leaves.vectorList = []


def resetButton():
    var.firstIteration = True
    try:
        reset()
    except Exception:
        print("Nothing to reset !")


def setLocatorButton():  # launched when setlocator button is pressed.
    ls = cmds.ls(sl=True)
    if ls:
        myLocator.setup(ls[0])
        updateVector(vector0)  # update to display vector
        cmds.viewFit(ls[0])


def setMeshButton():
    try:
        mesh = cmds.ls(sl=True)[0]
        grp.reset()
        myMesh.setmMesh(mesh)
    except Exception:
        print("please select a mesh object !")


def iterateButton():
    try:
        if var.firstIteration is True:
            reset()
        branchlist.iterate(var.loopNumber)
    except Exception:
        print("set mesh and location first !")


def finishButton():
    try:
        branchlist.close()
        cmds.delete(myMesh.refMesh)

    except Exception:
        print("No generation to terminate !")


def combineGeo():
    try:
        geo = grp.unite()
        grp.reset()
        var.firstIteration = True
        cmds.select(geo)
    except Exception:
        print("No geo to combine !")


def setLeafButton():

    leaves.setMesh(cmds.ls(sl=True)[0])


def placeLeavesButton():
    leaves.reset()
    leaves.placeGeo()


# Objects created at launch to easy variable access.

var = Var()
myMesh = Mesh()
vector0 = Vector()
myLocator = Locator()
branch0 = Branch()
branchInv = Branch()
branchlist = Branchlist()
grp = Grp()
leaves = Leaves()

# WINDOW

if cmds.window("RootsAndIvy", exists=True):
    cmds.deleteUI("RootsAndIvy", window=True)

myWindow = cmds.window("RootsAndIvy", iconName="mw")
if cmds.windowPref(myWindow, exists=True):
    cmds.windowPref(myWindow, remove=True)

# MENU
menuBarLayout = cmds.menuBarLayout()
cmds.menu(label="File")
cmds.menuItem(label="Reset")

cmds.menu(label="Help", helpMenu=True)
cmds.menuItem(label="About...")

# MAIN LAYOUT
mainColumn = cmds.columnLayout(adjustableColumn=True, w=500, co=["both", 5])

# FRAME 1
frame1 = cmds.frameLayout(label="Initial setup", mw=5, parent=mainColumn)
f1r = cmds.rowLayout(
    numberOfColumns=2, parent=frame1, rat=[1, "top", 0], adj=2
)
frame11 = cmds.frameLayout(
    label="Mesh setup", mw=5, mh=2, parent=f1r, bgs=True
)
frame12 = cmds.frameLayout(
    label="Standard division setup", mw=5, parent=f1r, bgs=True
)

cmds.rowColumnLayout(
    numberOfColumns=2, parent=frame11, rs=[[2, 5]], cs=[2, 5], cal=[1, "right"]
)
cmds.text(label="Reference Mesh")
cmds.button(label="Set mesh", command=("RootsAndIvy.setMeshButton()"))
cmds.text(label="")
cmds.button(
    label="Create locator", command=("cmds.spaceLocator(n='StartLocator')")
)

cmds.text(label="Start position")
cmds.button(label="Set position", command=("RootsAndIvy.setLocatorButton()"))

cmds.rowLayout(numberOfColumns=2, parent=frame12)


# FRAME 2
frame2 = cmds.frameLayout(
    label=" Generation's setup", mw=5, parent=mainColumn, bgs=True
)

scaleFactor = cmds.floatSliderGrp(
    label="Scale factor (length)\n Affects precision",
    field=True,
    minValue=0.0,
    maxValue=0.5,
    fieldMinValue=0.0,
    fieldMaxValue=5,
    step=0.01,
    value=0.1,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="updateVector(vector0)",
    dc="updateVector(vector0)",
    parent=frame12,
    ad3=1,
)
startAngle = cmds.intSliderGrp(
    label="Angle",
    field=True,
    minValue=0.0,
    maxValue=360,
    fieldMinValue=0.0,
    fieldMaxValue=360,
    step=1,
    value=0,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="updateVector(vector0)",
    dc="updateVector(vector0)",
    parent=frame12,
    ad3=1,
)
radius = cmds.floatSliderGrp(
    label="Radius",
    field=True,
    minValue=0.0,
    maxValue=0.5,
    fieldMinValue=0.0,
    fieldMaxValue=2,
    step=0.05,
    value=0.05,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="updateVector(vector0)",
    dc="updateVector(vector0)",
    parent=frame12,
    ad3=1,
)
penetration = cmds.floatSliderGrp(
    label="Penetration",
    field=True,
    minValue=0.0,
    maxValue=1,
    fieldMinValue=0.0,
    fieldMaxValue=1,
    step=0.05,
    value=0.05,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="updateVector(vector0)",
    dc="updateVector(vector0)",
    parent=frame12,
    ad3=1,
)


iterations = cmds.intSliderGrp(
    label="Branches average length",
    field=True,
    minValue=1,
    maxValue=100,
    fieldMinValue=1,
    fieldMaxValue=100,
    step=1,
    value=20,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
iterationsVar = cmds.floatSliderGrp(
    label="Length variation amplitude",
    field=True,
    minValue=0,
    maxValue=1,
    fieldMinValue=0,
    fieldMaxValue=1,
    step=0.05,
    value=0.3,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
angleAmplitude = cmds.floatSliderGrp(
    label="Angle randomness variance",
    field=True,
    minValue=0.0,
    maxValue=45,
    fieldMinValue=0.0,
    fieldMaxValue=90,
    step=1,
    value=15,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
angleAmplitudeDiv = cmds.floatSliderGrp(
    label="Angle randomness variance\nat divisions",
    field=True,
    minValue=0.0,
    maxValue=45,
    fieldMinValue=0.0,
    fieldMaxValue=90,
    step=1,
    value=25,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
divRate = cmds.floatSliderGrp(
    label="Divisions rate",
    field=True,
    minValue=0,
    maxValue=1,
    fieldMinValue=0,
    fieldMaxValue=1,
    step=0.01,
    value=0.30,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
closeRate = cmds.floatSliderGrp(
    label="Closing rate",
    field=True,
    minValue=0,
    maxValue=1,
    fieldMinValue=0,
    fieldMaxValue=1,
    step=0.01,
    value=0.20,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
cmds.text(
    label="A high (division rate/closing rate) ratio will \
lead to exponential generation !"
)


# FRAME 3
frame3 = cmds.frameLayout(label="Create geometry", mw=5, parent=mainColumn)

frame31 = cmds.frameLayout(
    label="Main structure", mw=5, parent=frame3, bgs=True
)
# ROWCOLUMN with 2 column
f31r = cmds.rowColumnLayout(
    numberOfColumns=2, rs=[[2, 5]], cs=[2, 5], cal=[1, "right"]
)

# 1
loopNumber = cmds.intSliderGrp(
    label="Number of \n iteration's \nloop",
    field=True,
    minValue=1,
    maxValue=10,
    fieldMinValue=1,
    fieldMaxValue=50,
    step=1,
    value=1,
    columnWidth3=(100, 50, 50),
    ad3=1,
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    parent=f31r,
)
# 2
cmds.button(label="Iterate", command=("RootsAndIvy.iterateButton()"))

# 3
cmds.rowLayout(numberOfColumns=2, parent=f31r)
cmds.text(label="Reset current generation")
cmds.button(label="reset", command=("RootsAndIvy.resetButton()"))
# 4
cmds.rowLayout(numberOfColumns=2, parent=f31r)
cmds.text(label="Terminate\n (Plug extremities)")
cmds.button(label="Terminate", command=("RootsAndIvy.finishButton()"))

# FRAME4
frame32 = cmds.frameLayout(label="Leaves", mw=5, parent=frame3, bgs=True)
cmds.text(
    label="Leaf primitive orientation must be : \n UP = global Y, \
leaf direction = global Z, stem basis = 0,0,0"
)

f32r = cmds.rowLayout(numberOfColumns=2, ad2=2, ct2=("right", "right"))
f32rc = cmds.columnLayout()
f32rr = cmds.rowLayout(numberOfColumns=2)
cmds.text(label="Set leave primitive", parent=f32rr)

cmds.button(
    label="Set Mesh", command=("RootsAndIvy.setLeafButton()"), parent=f32rr
)

leavesDensity = cmds.floatSliderGrp(
    label="Density",
    field=True,
    minValue=0,
    maxValue=1,
    fieldMinValue=0,
    fieldMaxValue=1,
    step=0.01,
    value=0.4,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
    parent=f32rc,
)
leavesScaleVar = cmds.floatSliderGrp(
    label="Scale\n variance",
    field=True,
    minValue=0,
    maxValue=1,
    fieldMinValue=0,
    fieldMaxValue=1,
    step=0.01,
    value=0.3,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
    parent=f32rc,
)
leavesRot1Var = cmds.intSliderGrp(
    label="Rotation\n variance",
    field=True,
    minValue=0,
    maxValue=30,
    fieldMinValue=0,
    fieldMaxValue=45,
    step=1,
    value=15,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
    parent=f32rc,
)

cmds.columnLayout(parent=f32r)

cmds.text(label="Positionning interval (0 = normal, 90 = lateral segment) : ")
leavesPlacementIntMin = cmds.intSliderGrp(
    label="min",
    field=True,
    minValue=0,
    maxValue=90,
    fieldMinValue=0,
    fieldMaxValue=90,
    step=1,
    value=45,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
leavesPlacementIntMax = cmds.intSliderGrp(
    label="max",
    field=True,
    minValue=0,
    maxValue=90,
    fieldMinValue=0,
    fieldMaxValue=90,
    step=1,
    value=85,
    columnWidth3=(100, 50, 50),
    columnAlign3=("right", "center", "center"),
    cc="var.update()",
    dc="var.update()",
    ad3=1,
    co3=[0, 0, 30],
    ct3=("right", "center", "right"),
)
cmds.rowColumnLayout(
    numberOfColumns=2, rs=[[2, 5]], cs=[2, 5], cal=[1, "right"]
)
cmds.button(label="Place leaves", command=("RootsAndIvy.placeLeavesButton()"))
cmds.button(label="Reset", command=("leaves.reset()"))

# FRAME 5
frame5 = cmds.frameLayout(label="Utility", mw=5, parent=mainColumn, bgs=True)
cmds.rowLayout(numberOfColumns=2)
cmds.text(label="Combine geometry")
cmds.button(label="Combine geo", command=("RootsAndIvy.combineGeo()"))

var.update()
cmds.showWindow("RootsAndIvy")
