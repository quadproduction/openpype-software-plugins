import maya.cmds as ma
import maya.mel as mel
import os, math

######################################################################################################################################
#Created by Simon Paul Mills (www.simonpaulmills.com) 
#Please do not modify this information, it is used to identify rig components in the scene.

author = ' SimonMills' #creator of tool and rig
webSite = 'www.trickbox.ca' #vendor website
webHelp = 'https://simonpaulmills.com/blogs/tutorials/how-to-rig-a-car-in-maya-using-the-uac-rig' #help page


toolFile = __file__
toolFile = toolFile.replace( '\\', '/')

######################################################################################################################################
#LOCATIONS
######################################################################################################################################
product = os.path.basename( toolFile ).split( '.py' )[0]
iconDir = toolFile.split( product + '.py' )[0] + 'icons/'

#file modifiers
truckDir = 'truck/'
sfx_noChassis = '_NoChassis'
sfx_lite = '_Lite'
ext_ma = '.ma'

#the default load,import & reference maya files are pulled from here:
if '/tool/' in toolFile:
	rigFile = toolFile.split( '/tool/' )[0] + '/' + product
	truckRigFile = toolFile.split( '/tool/' )[0] + '/' + truckDir + product 
else:
	rigFile = toolFile.split( '/tbTools/' )[0] + '/__ASSET__/Rigs/' + product + '/' + product
	truckRigFile = toolFile.split( '/tbTools/' )[0] + '/__ASSET__/Rigs/' + product + '/' + product
######################################################################################################################################
#HELP
######################################################################################################################################
dict_help = {
	'label' : {
		'setActiveRig' : 'Set Active Rig - ( Select any control )',
		'connectSkin' :       'SKIN selected mesh to rig ( full deformation )    ',
		'connectParent' :     'PARENT selected mesh to rig ( no deform )        ',
		'connectConstraint' : 'CONSTRAIN selected mesh to rig ( no deform ) ',
		'connectRemove' : 'REMOVE selected mesh(s) connection to rig.',
		'curvePath' : 'Add curve or edgeLoop to rig path system.',
		'addPath' : 'ADD SELECTED\n  curvePath',
		'removeActivePath' : 'REMOVE ACTIVE\n   curvePath',
		'removeAllPaths' : 'REMOVE ALL\ncurvePaths' },
	'warning' : {
		'nothingSelected' : 'nothing is selected.',
		'invalidSelection' : 'select group(s) or mesh, not both types at the same time.',
		'selectedCannotBeSkinned' : 'Selected objects cannot be skinned to the rig. Using the constraint method instead.',
		'connectingOther' : 'Connecting non-standard objects to the rig are limited to the body only.',
		'noRig' : 'No rig found in scene.',
		'multiRig' : 'More than 1 rig found in scene. Select any control or the top group of the rig you want to set active and press the top "Active Rig" button.',
		'selectControl' : 'Select the topGroup or any control of the rig you want active and try again.',
		'noCurve' : 'No curves selected. Select your curve(s) and try again.',
		'noMesh' : 'No mesh selected. Select your mesh(s) or a group of mesh(s) and hit the button for the part you wish to connect to.',
		'noMeshFoundInGroup' : 'No mesh found directly in group - ',
		'referencedParent' : 'is referenced. Cannot parent referenced objects to the rig. Maya referencing is hierarchy dependant.',
		'referencedAutoParentIgnore' : 'AutoParent will be ignored for referenced objects. Maya referencing is hierarchy dependant.',
		'noMeshRemove' : 'No mesh selected. Select your mesh(s) or a group of mesh(s) and hit the Red [ X ] button to remove any connection to the rig.',
		'noGrpRemove' : 'Selected groups contain no mesh. Select your mesh(s) or a group of mesh(s) and hit the Red [ X ] button to remove any connection to the rig.',
		'noRoot' : 'No root_ctrl selected. Select the root_ctrl of the rig you want to set active and press the top "Active Rig" button.',
		'addPathInvalidName' : ' cannot be added. The name already exists.', 
		'emptyParentGrp' : ' could not be parented to multiple rig nodes so it was ignored.',
		'load' : 'Could not locate file: ',
		'skipConnection' : 'Connection skipped for ',
		'removeActivePath' : ' is a preset path, this cannot be removed.',
		'removeAllPathConfirm' : 'Are you sure you want to remove all custom curve paths?',
		'removeAllPathCancel' : 'Remove All curve paths canceled.',
		'noActivePath' : 'No path is currently active. Set a curvePath from the root control curvePath attribute.',	
		'rootCtrlMismatch' : 'The root_ctrl detection is not matching correctly.',	
		'autoParent' : 'Auto Parent option has no effect when using the parent method, the option is irrelevant.',
		'autoParentOther' : 'Auto Parent option has no effect on non mesh/group objects, the option is irrelevant.', 
		'splitMesh' : 'You must split your mesh up when using parent or constraint connection methods. Use the skin method if you wish to keep the mesh as 1 piece.' },
	'success' : {
		'curveUpdate' : 'curve point positions updated.',
		'skin' : 'is now connected to rig by a SKIN method.',
		'constraint' : 'is now connected to rig by a CONSTRAINT method.',
		'parent' : 'is now connected to rig via PARENTING.',	
		'remove' : 'is now free from any connection to the rig.',
		'load' : 'Loaded: ',
		'reference' : 'Referenced: ',
		'import' : 'Imported: ',		
		'preservePosition' : 'PreservePosition is now ',
		'addPathFromCurve' : ' has been regenerated and added to path system. Your original source curve is preserved and can be deleted without breaking anything.',
		'addPathFromEdgeLoop' : ' curve generated from edgeLoop and added to path system.',
		'removeActivePath' : ' has been removed from the path system.',
		'removeAllPaths' : 'All user paths have been removed from the path system.' },		
	'popup' : {
		'setActiveRig' : 'help info regarding the setActiveRig row.',
		'connection' : 'help info regarding the connection row.',
		'curvePath' : 'help info regarding the curvePath row.' } }





#shortHand
x = 'X'
y = 'Y'
z = 'Z'
axis = [ x, y, z]
t = 'translate'
r = 'rotate'
s = 'scale'
v = 'visibility'
transforms = [ t, r, s ]

sceneUnitDict = { 'cm' : 1.0, 'mm' : 10.0, 'm' : 0.01, 'km': 9.999969839999708e-6, 'in' : 0.393701, 'ft' : 0.0328083, 'yd' : 0.0109361, 'mi' : 6.213693181818e-6 }
sceneUnitMultiplier = sceneUnitDict.get( ma.currentUnit( l=1, q=1 ) )


######################################################################################################################################
#GENERAL FUNCTIONS
######################################################################################################################################

def getMayaVersion():
	return int( mel.eval( '$versionGLOBAL = getApplicationVersionAsFloat' ) )

def isReferenced( n ):
	return ma.referenceQuery( n, inr = True )

def rename( n, newName ):
	n = ma.rename( n, newName )
	shape = getShape( n )
	if shape != None:
		ma.rename( shape, n + 'Shape' )
	return newName


def getNamespace( n ):
	baseName = n.split( ':' )[-1]
	nameSpc = n[0: len( n ) - len( baseName ) ]
	return nameSpc


def getBaseName( n ):
	baseName = n.split( ':' )[-1]
	nameSpc = n[0: len( n ) - len( baseName ) ]
	#in case of simlar naming in sub groups
	baseName = baseName.split( '|' )[-1]
	return baseName


def getParent( n ):
	parent = ma.listRelatives( n, f=0, p=1, pa=1 )
	return n if parent == [] or parent == None else parent[-1]


def getTopParent( n ):
	topParent, child = None, n
	while topParent == None:
		parent = ma.listRelatives( child, f=0, p=1, pa=1 )
		if parent == [] or parent == None:
			topParent = child
		else:
			child = parent[-1]
	else:
		return topParent


def getChildren( n ): 
	children = ma.listRelatives( n, type='transform', c=1, pa=1 )
	return [] if children == None else children


def getAllChildren( n ):
	children = ma.listRelatives( n, type='transform', ad=1, pa=1 )
	return [] if children == None else children


def getConnection( item ):
	return list( set( getConnectionIn( item ) + getConnectionOut( item ) ) )


def getConnectionIn( n, plugs = 0 ):
	inConnection =  ma.listConnections( n, d=0, s=1, scn=1, p=plugs )
	return [] if inConnection == None else list( set( inConnection ) )


def getConnectionOut( n, plugs = 0 ):
	outConnection =  ma.listConnections( n, d=1, s=0, scn=1, p=plugs )
	return [] if outConnection == None else list( set( outConnection ) )


def getConnectionByType( n, nType ):
	connectionList = []
	for connection in getConnection( n ):
		if ma.nodeType( connection ) == nType:
			connectionList.append( connection )
	return connectionList


def getTransform( n ):#component/shape to object transform
	if '.' in n: #component
		return getParent( getParent( n ) )

	elif 'Shape' in ma.nodeType( n ):
		return getParent( n )

	elif n in ma.ls( s=1 ): #shape
		return getParent( n )
	
	else:
		return n


def getShape( n ):
	shapeList =  ma.listRelatives( n, f=0, s=1, pa=1 )
	if shapeList == None:
		shapeList =  ma.listRelatives( getTransform( n ), f=0, s=1, pa=1 )
	if shapeList == [] or shapeList == None:
		return n
	else:
		return shapeList[0]


def hasSymetricalMeshParts( n ):
	bBox = ma.xform( n, bb=True, q=True )
	#10% of bBox[3]
	if bBox[0] + bBox[3] < ( bBox[3] * 0.1 ):
	    return True
	else:
	    return False


def getSkin( n ):# returns the skinNode attached to n
	n = getTransform( n )
	historyList = []
	for history in ma.listHistory( n ):
		if ma.nodeType( history ) == 'skinCluster':
			return history
	return None


def setTransform( n, pos = None, rot = None, scale = None ):
	valueList = [ pos, rot, scale ]
	for tform in transforms:
		value = valueList[ transforms.index( tform ) ]
		if value != None:
			for ax in axis:
				ma.setAttr( n + '.' + tform + ax , value[ axis.index( ax ) ] )


def unlockTransforms( n, forceShow = False ):
	try:
		for tf in transforms:
			for ax in axis:
				ma.setAttr( n + '.' + tf + ax, e=1, l=False )
				if forceShow == True:
					ma.setAttr( n + '.' + tf + ax, k=True )
		
	except:
		#reference
		pass

def resetAttributes( nList ):
	for n in nList:
		for tf in [ t, r, s ]:
			for ax in axis:
				value = 1.0 if tf == s else 0.0
				ma.setAttr( n + '.' + tf + ax, value )

def freezeTransforms( n ):
	try:
		ma.makeIdentity( n, a=1, t=1, r=1, s=1 )
	except:
		#referenced
		pass


def parentWorld( n ):
	if getParent( n ) != n:
		ma.parent( n, w=1 )


def getShellDict( mesh ): #returns shells as indexed dict - { 1: [list of faces], .. }
	shellCount =  ma.polyEvaluate( mesh, s=1 )
	faceAll = ma.ls( ma.polyListComponentConversion( mesh, tf=1 ), fl=1 )
	shellDict = { 1 : faceAll }
	faceID = 0
	faceList = []
	if shellCount > 1:
		for i in range( 0, shellCount ):
			shellDict[ i + 1 ] =  ma.ls( ma.polySelect( mesh, ns=1, ets= faceID, q=1, ass=1 ), fl=1 )
			faceID += len( shellDict.get( i + 1 ) )
	return shellDict


def buildCurveComponentList( curve, indexList = None ): #indexList returns only curve points of given indices
	curveComponentList = []
	for i in range( 0, getCurveComponents( curve ) ):
		if indexList == None or i in indexList:
			curveComponentList.append( curve + '.cv[' + str( i ) + ']' )
	return curveComponentList


def getCurveComponents( curve ):
	spans = ma.getAttr( curve + '.spans' )
	degree = ma.getAttr( curve + '.degree' )
	return spans + degree if ma.getAttr( curve + '.form' ) != 2 else spans


def getObjectCenter( n ):
	if ma.nodeType( n ) == 'joint':
		return ma.xform( n, q=1, t=1, ws=1 )
	else:
		return ma.objectCenter( n, gl=True )
		# # default objectCenter command returns a center that includes children, we don't want that.
		# children = getChildren( n )
		# if children != []:
		# 	parentWorld( children )
		# 	center = ma.objectCenter( n, gl=True )
		# 	ma.parent( children, n )
		# 	return center
		# else:
		# 	return ma.objectCenter( n, gl=True )


def distanceBetween( pointA, pointB ):
	#works with 3d or 2d points
	import math
	x = pointA[0] - pointB[0]
	y = pointA[1] - pointB[1]
	if len( pointA ) == 3:
		z = pointA[2] - pointB[2]
		return  math.sqrt( math.pow( x, 2 ) + math.pow( y, 2 ) + math.pow( z, 2 ) )
	else:
		return math.sqrt( math.pow( x, 2 ) + math.pow( y, 2 ) )


def averageVector( vectorList ):# example: [ [ 2, 1, 1 ], [ 2, 1, 2 ], [ 2, 1, 3 ] ] to [ 2, 1, 2 ] 
	avg = []
	if type( vectorList[0] ) == list:
		avg = [ 0.0, 0.0, 0.0 ]
		for i in range( 0, len( vectorList ) ):
			for ii in range( 0, len( vectorList[i] ) ):
				avg[ii] += vectorList[i][ii]
		avg = [ avg[0] / len( vectorList ), avg[1] / len( vectorList ), avg[2] / len( vectorList ) ]
	else:
		for i in range( 0, 3 ):
			avg.append( sum( vectorList[i::3] ) / ( len( vectorList ) / float( 3 ) ) )
	return avg					


def closestVector( targetVector, sourceVectorList ):
	#returns index of closest vector in sourceVectorList to targetVector
	closestDistance, closestVectorIndex = None, None
	for i in range( 0, len( sourceVectorList ) ):
		distance = distanceBetween( targetVector, sourceVectorList[i] )
		if closestDistance == None:
			closestDistance = distance
			closestVectorIndex = i

		if distance < closestDistance:
			closestDistance = distance
			closestVectorIndex = i
	
	return closestVectorIndex


def cmdPrint( info ):
	from maya.OpenMaya import MGlobal; MGlobal.displayInfo( '%s' % ( info ) )


def cmdWarn( info ):
	from maya.OpenMaya import MGlobal; MGlobal.displayWarning( '%s' % ( info ) )


def cmdMel( melCommand ):
	mel.eval( melCommand )


def cmdMelVar( melCommand ):
	return mel.eval( '$var = ' + melCommand )


def getAbrev( string ):
	#pulls only the upperCase letters from given string
	abrev = ''
	for char in string:
		if char.isupper():
			abrev += char
	return abrev


def isolate():
	panel = ma.getPanel( wf=1 )
	if ma.isolateSelect( panel, q=1, state=1 ):
		ma.isolateSelect( panel, state=0 )
		cmdPrint( 'isolate off' )
	else:
		ma.isolateSelect( panel, state=1 )
		ma.isolateSelect( panel, addSelected=1 )
		cmdPrint( 'isolate on' )




class progressBar():
	def __init__( self, maxValue ):
		self.status = 'processing'
		self.interruptable = True
		self.maxValue = maxValue
		self.start()

	def start( self ):
		self.globProgressBar = cmdMelVar( '$gMainProgressBar' )
		ma.progressBar( self.globProgressBar, e=1, beginProgress=1, isInterruptable=self.interruptable, status=self.status, maxValue=self.maxValue, minValue = 0 )

	def step( self, value = 1 ):
		if not ma.progressBar( self.globProgressBar, q=1, isCancelled=1 ): 
			ma.progressBar( self.globProgressBar, e=1, step = value, status = self.status + '...' )

	def stop( self ):
		ma.progressBar( self.globProgressBar, e=1, endProgress=1 )






######################################################################################################################################
#RIG CONNECT
######################################################################################################################################
class rigConnect():
	def __init__( self ):
		self.nameSpc = ''
		self.abrev = getAbrev( product )
		self.attr_connectCache = 'TB_cache_'
		self.attr_tagID, self.attr_tagPOS = 'TB_tag_ID', 'TB_tag_POS'
		self.attr_controlType = 'controlType'
		self.attr_showProxy = 'showProxy'
		self.attr_showChassis = 'showChassis'
		self.attr_showSteeringWheel = 'showSteeringWheel'
		self.attr_dynamics = 'dynamic'
		self.attr_version = 'version'

		#rigObjects
		self.activeRig = None
		self.rootCtrl = None
		self.bodyCtrl = None
		self.driveCtrl = None
		self.rigGrp = None
		self.locatorGrp = None
		self.curvePathGrp = None
		self.curvePtGrp = None
		self.geometryGrp = None

		#possible POS tag values
		self.list_tagPOS = [ 'lf', 'rf', 'lb', 'rb', 'lm1', 'rm1', 'lm2', 'rm2', 'lm3', 'rm3' ]
		
		self.dict_tagPOS = {
			'lf' : 'leftFront',
			'rf' : 'rightFront',
			'lb' : 'leftRear',
			'rb' : 'rightRear',
			'lm1' : 'leftMid1',
			'rm1' : 'rightMid1',
			'lm2' : 'leftMid2',
			'rm2' : 'rightMid2',
			'lm3' : 'leftMid3',
			'rm3' : 'rightMid3' }

		#possible ID tag values
		self.tagID_topNode = 'topNode' #self.activeRig
		self.tagID_rootJt = 'rootJt'
		self.tagID_rootCtrl = 'rootCtrl'
		self.tagID_wheelCtrl = 'wheelCtrl'
		self.tagID_tunerCtrl = 'tunerCtrl'
		self.tagID_bodyCtrl = 'bodyCtrl'
		self.tagID_driveCtrl = 'driveCtrl'
		self.tagID_dynamicTargetCtrl = 'dynamicTargetCtrl'
		self.tagID_steeringWheelCtrl = 'steeringWheelCtrl'
		self.tagID_body = 'body'
		self.tagID_steeringWheel = 'steeringWheel'
		self.tagID_caliper = 'caliper'
		self.tagID_wheel = 'wheel'
		self.tagID_tire = 'tire'
		self.tagID_locatorGrp = 'locatorGrp'
		self.tagID_curvePathGrp = 'curvePathGrp'
		self.tagID_curvePtGrp = 'curvePtGrp'
		self.tagID_geometryGrp = 'geometryGrp'
		self.tagID_renderGrp = 'renderGrp'
		self.tagID_rigGrp = 'rigGrp'
		self.tagID_wrapPlaneGrp = 'wrapPlaneGrp'
		
		self.tagID_boot = 'boot'
		self.tagID_bonnet = 'bonnet'
		self.tagID_f_door = 'f_door'
		self.tagID_b_door = 'b_door'
		self.tagID_wheelWrap = 'wheelWrap'


		#used in UI
		self.list_tagID = [ self.tagID_body, self.tagID_steeringWheel, self.tagID_caliper, self.tagID_wheel, self.tagID_tire ]
		self.list_tagID2 = [ self.tagID_bonnet, self.tagID_f_door, self.tagID_b_door, self.tagID_boot ]

	def setActiveRigObjects( self ):
		#makes all needed connections easily accessible
		self.rootCtrl = self.ensureExists( self.getCACHE( self.tagID_rootCtrl ) )
		self.bodyCtrl = self.ensureExists( self.getCACHE( self.tagID_bodyCtrl ) )
		self.driveCtrl = self.ensureExists( self.getCACHE( self.tagID_driveCtrl ) )
		self.rootJt = self.ensureExists( self.getCACHE( self.tagID_rootJt ) )
		self.rigGrp = self.ensureExists( self.getCACHE( self.tagID_rigGrp ) )
		self.locatorGrp = self.ensureExists( self.getCACHE( self.tagID_locatorGrp ) )
		self.curvePathGrp = self.ensureExists( self.getCACHE( self.tagID_curvePathGrp ) )
		self.curvePtGrp = self.ensureExists( self.getCACHE( self.tagID_curvePtGrp ) )
		self.geometryGrp = self.ensureExists( self.getCACHE( self.tagID_geometryGrp ) )
		self.renderGrp = self.ensureExists( self.getCACHE( self.tagID_renderGrp ) )
		self.wrapPlaneGrp = self.ensureExists( self.getCACHE( self.tagID_wrapPlaneGrp ) )



	def setActivePathPlugs( self ): #motion
		self.cPlugList = []
		cPlugList = self.getCACHE( self.tagID_cPlug ) 
		if cPlugList != None:
			cPlugList = eval( cPlugList )
			for cPlug in cPlugList:
				self.cPlugList.append( self.ensureExists( cPlug ) )


	def ensureExists( self, n ): #to pass, n must exist and be present within self.activeRig or connected to the rootCtrl in some way
		if n != None:
			n = self.abrev + '_' + n
			if ma.objExists( self.nameSpc + n ):
				if self.nameSpc + n in getAllChildren( self.activeRig ):
					return self.nameSpc + n
				
				if self.rootCtrl in getConnectionIn( self.nameSpc + n ):
					return self.nameSpc + n

			if ma.objExists( n ):
				if n in getAllChildren( self.activeRig ):
					return n
				
				if self.rootCtrl in getConnectionIn( n ):
					return n
		return None


	def setNameSpace( self ):
		self.nameSpc = getNamespace( self.activeRig )


	def createConnectionStorage( self ):
		#writes lists for each tagID
		self.influence_body = []
		self.influence_steeringWheel = []
		self.influence_caliper = []
		self.influence_wheel = []
		self.influence_tire= []
		self.linkGrps_body = []
		self.linkGrps_steeringWheel = []
		self.linkGrps_caliper = []
		self.linkGrps_wheel = []
		self.linkGrps_tire= []

		self.influence_bonnet = []
		self.linkGrps_bonnet = []
		self.influence_boot = []
		self.linkGrps_boot = []
		self.influence_f_door = []
		self.linkGrps_f_door = []	
		self.influence_b_door = []
		self.linkGrps_b_door = []	

	def checkActiveRig( self ):
		#checks if the active rig is still valid
		if self.activeRig != None:
			if ma.objExists( self.activeRig ):
				if self.getID( self.activeRig  ) == self.tagID_topNode:
					return True
		return False


	def setActiveRig( self, inputControl = None ): #inputControl can be rootCtrl or TopNode
		self.createConnectionStorage()

		self.list_sceneRigs = []
		if inputControl == None:
			#search scene for rigs
			for n in ma.ls( assemblies = True ):
				if self.getID( n ) == self.tagID_topNode:
					self.list_sceneRigs.append( n )
			
			if len( self.list_sceneRigs ) == 0:
				#none found, do a deeper search.
				for n in ma.ls( type = 'transform' ):
					if self.getID( n ) == self.tagID_topNode:
						self.list_sceneRigs.append( n )
			
			if len( self.list_sceneRigs ) == 0:
				return None

			#1 rig in scene so connect to it.
			elif len( self.list_sceneRigs ) == 1:
				self.activeRig = self.list_sceneRigs[0]
				self.setNameSpace()
				self.setActiveRigObjects()
				self.setActivePathPlugs()
				self.reAddPathsToReferencedRig()
				return True
			
			elif len( self.list_sceneRigs ) > 1:
				return False
			
			else:
				#no rig in scene
				return None

		else:
			#is inputControl the topCtrl?

			#finds the topGrp of the given rig and sets it as self.activeRig
			topNode = getTopParent( inputControl )
			
			if ma.objExists( topNode + '.' + self.attr_tagID ):
				if self.getID( topNode ) == self.tagID_topNode:
					self.activeRig = topNode
					self.setNameSpace()
					self.setActiveRigObjects()
					self.setActivePathPlugs()
					self.reAddPathsToReferencedRig()
					return True
			else:
				cmdWarn( dict_help.get( 'warning' ).get( 'noRoot' ) )
				return None


	def getSelection( self ):
		#filters selection
		meshList, curveList, rootCtrl, edgeLoop, grpList, topNode, subGrpList = [], [], None, [], [], None, []
		userSelection = ma.ls( sl=1 )
		if userSelection != []:
			
			if '.e[' in userSelection[-1]:
				edgeLoop = userSelection

			for n in userSelection:
				if self.getID( n ) == self.tagID_topNode:
					topNode = n
				else:
					n = getTransform( n )
					shape = getShape( n )


					if shape == n:
						grpList.append( n )
						#get and child groups
						for child in getChildren( n ):
							childTransform = getTransform( child )
							childShape = getShape( child )
							if childShape == childTransform:
								subGrpList.append( child )

					elif ma.nodeType( shape ) == 'mesh':
						meshList.append( n )

					elif ma.nodeType( shape ) == 'nurbsCurve':
						if self.getID( n ) == self.tagID_rootCtrl:
							rootCtrl = n
							# if self.rootCtrl != rootCtrl:
							# 	cmdWarn( dict_help.get( 'warning' ).get( 'rootCtrlMismatch' ) )
						else:
							curveList.append( n )
		return topNode, rootCtrl, meshList, curveList, edgeLoop, grpList, subGrpList


	def getID( self, n ):
		#extract the tagID of given object
		return ma.getAttr( getTransform( n ) + '.' + self.attr_tagID ) if ma.attributeQuery( self.attr_tagID, n = getTransform( n ), ex = 1 ) else None


	def getPOS( self, n ):
		return ma.getAttr( getTransform( n ) + '.' + self.attr_tagPOS ) if ma.attributeQuery( self.attr_tagPOS, n = getTransform( n ), ex = 1 ) else None


	def getCACHE( self, ID, TYPE = '' ):
		attr = self.attr_connectCache + ID + TYPE.capitalize()
		return ma.getAttr( self.activeRig + '.' + attr ) if ma.attributeQuery( attr, n = self.activeRig , ex = 1 ) else None



	def setInfluenceVar( self, ID, value ):
		if ID == self.tagID_body:
			self.influence_body = value

		elif ID == self.tagID_steeringWheel:
			self.influence_steeringWheel = value
		
		elif ID == self.tagID_caliper:
			self.influence_caliper = value
		
		elif ID == self.tagID_wheel:
			self.influence_wheel = value
		
		elif ID == self.tagID_tire:
			self.influence_tire= value
		
		elif ID == self.tagID_boot:
			self.influence_boot= value

		elif ID == self.tagID_bonnet:
			self.influence_bonnet= value

		elif ID == self.tagID_f_door:
			self.influence_f_door= value
		
		elif ID == self.tagID_b_door:
			self.influence_b_door= value

		else:
			print( 'ERROR' )



	def setLinkGrpVar( self, ID, value ):
		if ID == self.tagID_body:
			self.linkGrps_body = value

		elif ID == self.tagID_steeringWheel:
			self.linkGrps_steeringWheel = value
		
		elif ID == self.tagID_caliper:
			self.linkGrps_caliper = value
		
		elif ID == self.tagID_wheel:
			self.linkGrps_wheel = value
		
		elif ID == self.tagID_tire:
			self.linkGrps_tire= value
		
		elif ID == self.tagID_boot:
			self.linkGrps_boot= value

		elif ID == self.tagID_bonnet:
			self.linkGrps_bonnet= value

		elif ID == self.tagID_f_door:
			self.linkGrps_f_door= value
		
		elif ID == self.tagID_b_door:
			self.linkGrps_b_door= value

		else:
			print( 'ERROR' )



	def getInfluence( self, ID, tagPos = None ):
		#returns a list of all skeletal influences for given ID
		influence = []#eval( 'self.influence_' + ID )
		if influence == []:
			#check cache
			skinCache = self.getCACHE( ID, 'skin' )
			if skinCache != None:
				skinCache = eval( skinCache )
				for jt in skinCache :
					jt = self.ensureExists( jt )
					if jt != None:
						if tagPos == None:
							influence.append( jt )
						else:
							if tagPos in self.getPOS( jt ) or tagPos == 'useAllChildren':
								if ID == self.tagID_tire:
									#add the children of tire
									for child in getChildren( jt ):
										influence.append( child )
								else:
									influence.append( jt )
			# self.setInfluenceVar( ID, influence )
		return influence





	def getSkinSource( self, ID ):
		#returns a skinWt source mesh of given ID		
		rigMesh = ma.listRelatives( self.activeRig, type='mesh', ad=1, pa=1 )
		for meshObj in rigMesh:
			if self.getID( getTransform( meshObj ) ) == ID:
				return meshObj


	def getLinkGrps( self, ID ):
		#returns the linkGrp node for given ID
		linkGrps = eval( 'self.linkGrps_' + ID )
		if linkGrps == []:
			linkGrpCache = self.getCACHE( ID, 'parent' )
			if linkGrpCache != None:
				linkGrpCache = eval( linkGrpCache )
				for linkGrp in linkGrpCache :
					linkGrp = self.ensureExists( linkGrp )
					if linkGrp != None:
						linkGrps.append( linkGrp )
			self.setLinkGrpVar( ID, linkGrps )
		
		linkGrpVectors = []
		if len( linkGrps ) > 1:
			for linkGrp in linkGrps:
				linkGrpVectors.append( getObjectCenter( linkGrp ) )

		return linkGrps, linkGrpVectors


	def getGroupedMesh( self, grp ):
		meshList = []
		for child in getAllChildren( grp ):
			shape = getShape( child )
			if ma.nodeType( shape ) == 'mesh':
				meshList.append( child )
		return meshList


	def getClosestLinkGrp( self, n, linkGrps, linkGrpVectors ):	
		closestIndex = closestVector( getObjectCenter( n ), linkGrpVectors )
		return linkGrps[ closestIndex ]


	def attachMesh( self, ID, method, parentNode = None, autoParentGeo = False, removeUnusedInfluences = False ):
		topNode, rootCtrl, meshList, curveList, edgeLoop, grpList, subGrpList = self.getSelection()
		

		linkGrps, linkGrpVectors = self.getLinkGrps( ID )
		# print( ID )
		# print( linkGrps )
		# print( linkGrpVectors )
		

		try:
			linkGrps, linkGrpVectors = self.getLinkGrps( ID )
		except:
			self.updateActiveRigLayout( False )
			self.attachMesh( ID, method, parentNode, autoParentGeo, removeUnusedInfluences )
			return False
		#EMPTY
		if grpList == [] and meshList == [] and curveList == [] and edgeLoop == [] and rootCtrl == None and topNode == None:
			selection = ma.ls( sl=1 )
			if selection == []:
				cmdWarn( dict_help.get( 'warning' ).get( 'nothingSelected' ) )
			else:
				#some other object is being connected to rig.
				if method == self.label_skin:
					cmdWarn( dict_help.get( 'warning' ).get( 'selectedCannotBeSkinned' ) )
					method = self.label_constraint

				if ID in [ self.tagID_body, self.tagID_steeringWheel, self.tagID_boot, self.tagID_bonnet ]:
					linkGrp = linkGrps[-1]
				
				else:
					for n in selection:
						linkGrp = self.getClosestLinkGrp( n, linkGrps, linkGrpVectors )
						
						if method == self.label_parent:
							if autoParentGeo == False:
								cmdWarn( n + dict_help.get( 'warning' ).get( 'autoParent' ) )

							if not isReferenced( n ):
								if getParent( n ) != linkGrp:
									ma.parent( [ n ], linkGrp )
									cmdPrint( n + ' ' + dict_help.get( 'success' ).get( 'parent' ) )
							else:
								cmdWarn( grp + ' ' + dict_help.get( 'warning' ).get( 'referencedParent' ) )
					
						if method == self.label_constraint:
							if autoParentGeo == True:
								cmdWarn( n + dict_help.get( 'warning' ).get( 'autoParentOther' ) )
							ma.parentConstraint( linkGrp, n, mo=1 )
							ma.scaleConstraint( linkGrp, n, mo=1 )
							cmdPrint( n + ' ' + dict_help.get( 'success' ).get( 'constraint' ) )



		#GROUP ONLY
		elif grpList != [] and meshList == [] and curveList == [] and edgeLoop == [] and rootCtrl == None and topNode == None:
			if self.checkActiveRig() == True:
				#REMOVE ANY PREVIOUS CONNECTION
				self.disconnectMesh( False )

			#cannot skin a group so skin contents
			if method == self.label_skin:
				for grp in grpList:
					meshList = self.getGroupedMesh( grp )
					

					if meshList != []:
						for mesh in meshList:
							#unlock + freeze mesh
							unlockTransforms( mesh )
							freezeTransforms( mesh )
						
						#unlock + freeze mesh
						try:
							unlockTransforms( grp )
							freezeTransforms( grp )
						except:
							cmdWarn( 'unable to freeze transforms on ' + grp + '. A child non-mesh node with locked or connected attributes may cause this.' )


						ma.select( meshList )
						self.attachMesh( ID, method, grp, autoParentGeo )
					else:
						cmdWarn( dict_help.get( 'warning' ).get( 'noMeshFoundInGroup' ) + ' ' +  grp )

			else:
				for grp in grpList:
					meshList = self.getGroupedMesh( grp )

					if ID in [ self.tagID_body, self.tagID_steeringWheel, self.tagID_boot, self.tagID_bonnet ]:
						linkGrp = linkGrps[-1]
					else:
						linkGrp = self.getClosestLinkGrp( grp, linkGrps, linkGrpVectors )
					

					if meshList != []:

						#unlock/freeze grp
						unlockTransforms( grp )
						freezeTransforms( grp )

						if method == self.label_parent:
							if not isReferenced( grp ):
								if autoParentGeo == False:
									cmdWarn( grp + dict_help.get( 'warning' ).get( 'autoParent' ) )

								if getParent( grp ) != linkGrp:
									ma.parent( [ grp ], linkGrp )
									cmdPrint( grp + ' ' + dict_help.get( 'success' ).get( 'parent' ) )
							else:
								cmdWarn( grp + ' ' + dict_help.get( 'warning' ).get( 'referencedParent' ) )

						if method == self.label_constraint:
							ma.parentConstraint( linkGrp, grp, mo=1 )
							ma.scaleConstraint( linkGrp, grp, mo=1 )
							if autoParentGeo == True:
								if getParent( grp ) != self.renderGrp:
									if not isReferenced( grp ):
										ma.parent( grp, self.renderGrp )
									else:
										cmdWarn( grp + ' ' + dict_help.get( 'warning' ).get( 'referencedAutoParentIgnore' ) )
							cmdPrint( grp + ' ' + dict_help.get( 'success' ).get( 'constraint' ) )
					else:
						if method == self.label_parent:
							if autoParentGeo == False:
								cmdWarn( grp + dict_help.get( 'warning' ).get( 'autoParent' ) )

							if not isReferenced( grp ):
								if getParent( grp ) != linkGrp:
									ma.parent( [ grp ], linkGrp )
									cmdPrint( grp + ' ' + dict_help.get( 'success' ).get( 'parent' ) )
							else:
								cmdWarn( grp + ' ' + dict_help.get( 'warning' ).get( 'referencedParent' ) )
					
						if method == self.label_constraint:
							if autoParentGeo == True:
								cmdWarn( grp + dict_help.get( 'warning' ).get( 'autoParentOther' ) )
							ma.parentConstraint( linkGrp, grp, mo=1 )
							ma.scaleConstraint( linkGrp, grp, mo=1 )
							cmdPrint( grp + ' ' + dict_help.get( 'success' ).get( 'constraint' ) )

			#restore selection
			if grpList == []:
				ma.select( grpList )
			return True


		#MESH ONLY
		elif meshList != [] and grpList == [] and curveList == [] and edgeLoop == [] and rootCtrl == None and topNode == None:
			if self.checkActiveRig() == True:
				#REMOVE ANY PREVIOUS CONNECTION
				self.disconnectMesh( False )

				#SKIN
				if method == self.label_skin:	
					#start progressBar
					pBar = progressBar( len( meshList ) )

					for n in meshList:
						maxInfluence = 4.0
						pBar.status = 'processing ' + n
						#unlock + freeze mesh
						unlockTransforms( n )
						freezeTransforms( n )

						if not isReferenced( n ):
							ma.bakePartialHistory( n )


						#multi jt skin with skin source ###################################
						if ID in [ self.tagID_tire ]: 
							#has skin source
							skinSource = self.getSkinSource( ID )
							
							if hasSymetricalMeshParts( n ):
								influence = self.getInfluence( ID, 'useAllChildren' )
							
							else:
								linkGrp = self.getClosestLinkGrp( n, linkGrps, linkGrpVectors )
								tagPos = self.getPOS( linkGrp )
								influence = self.getInfluence( ID, tagPos )
							
						
						elif ID in [ self.tagID_wheel ]:
							#has skin source
							skinSource = self.getSkinSource( ID )
							
							if hasSymetricalMeshParts( n ):
								influence = self.getInfluence( ID )
							
							else:
								linkGrp = self.getClosestLinkGrp( n, linkGrps, linkGrpVectors )
								tagPos = self.getPOS( linkGrp )
								influence = self.getInfluence( ID, tagPos )


						#multi jt skin, no skin source ###################################
						elif ID in [ self.tagID_caliper, self.tagID_b_door, self.tagID_f_door ]: 
							skinSource = None
							
							if hasSymetricalMeshParts( n ):
								maxInfluence = 1.0
								influence = self.getInfluence( ID )

							else:
								linkGrp = self.getClosestLinkGrp( n, linkGrps, linkGrpVectors )
								tagPos = self.getPOS( linkGrp )
								influence = self.getInfluence( ID, tagPos )


						#single jt skin ###################################
						elif ID in [ self.tagID_body, self.tagID_steeringWheel, self.tagID_bonnet, self.tagID_boot ]: 
							maxInfluence = 1.0
							influence = self.getInfluence( ID )
							skinSource = None

						
						else:
							cmdWarn( 'tag not found for ' + n )
							return False


						# print( 'ID: ' + str( ID ) )
						# print( 'linkGrps: ' + str( linkGrps ) )
						# print( 'linkGrpVectors: ' + str( linkGrpVectors ) )
						# print( 'influence: ' + str( influence ) )
						# print( 'skinSource: ' + str( skinSource ) )

						#set skin
						ma.skinCluster( influence, n, tsb=1, ih=0, dr=4.0, mi=maxInfluence, omi=1, nw=1 )
						
						#copy weights
						if skinSource != None:
							ma.copySkinWeights( skinSource, n, nm=1, sa='closestPoint', ia='oneToOne' )
		

						#parent to renderGrp
						if autoParentGeo == True:
							if not isReferenced( n ):
								if parentNode != None:
									if getParent( parentNode ) != self.renderGrp:
										ma.parent( parentNode, self.renderGrp )
								else:
									if getParent( n ) != self.renderGrp:
										ma.parent( n, self.renderGrp )
							else:
								cmdWarn( n + ' ' + dict_help.get( 'warning' ).get( 'referencedAutoParentIgnore' ) )
						
						#print
						pBar.step( 1 )
						cmdPrint( n + ' ' + dict_help.get( 'success' ).get( 'skin' ) )
					
					#end progressBar
					pBar.stop()
					#restore selection
					ma.select( meshList )
					#remove unused influences - not needed now
					if removeUnusedInfluences == True:
						cmdMel( 'scOpt_saveAndClearOptionVars(1); scOpt_setOptionVars( { "unusedSkinInfsOption"} ); cleanUpScene( 1 ); scOpt_saveAndClearOptionVars(0)' )
					return True
				
				#PARENT/CONSTRAINT
				else:
					for n in meshList:
						if ID in [ self.tagID_body, self.tagID_steeringWheel, self.tagID_boot, self.tagID_bonnet ]:
							linkGrp = linkGrps[-1]
						else:
							linkGrp = self.getClosestLinkGrp( n, linkGrps, linkGrpVectors )

						unlockTransforms( n )
						freezeTransforms( n )

						if method == self.label_parent:
							if autoParentGeo == False:
								cmdWarn( n + dict_help.get( 'warning' ).get( 'autoParent' ) )
							if not isReferenced( n ):
								if getParent( n ) != linkGrp:
									ma.parent( [ n ], linkGrp )
									cmdPrint( n + ' ' + dict_help.get( 'success' ).get( 'parent' ) )
							else:
								cmdWarn( n + ' ' + dict_help.get( 'warning' ).get( 'referencedParent' ) )

						if method == self.label_constraint:
							ma.parentConstraint( linkGrp, n, mo=1 )
							ma.scaleConstraint( linkGrp, n, mo=1 )
							if autoParentGeo == True:
								if not isReferenced( n ):
									if getParent( n ) != self.renderGrp:
										ma.parent( n, self.renderGrp )
								else:
									cmdWarn( n + ' ' + dict_help.get( 'warning' ).get( 'referencedAutoParentIgnore' ) )
							cmdPrint( n + ' ' + dict_help.get( 'success' ).get( 'constraint' ) )

				ma.select( meshList )
			return True

		else:
			cmdWarn( dict_help.get( 'warning' ).get( 'invalidSelection' ) )
			return False



	


	def disconnectMesh( self, printState = True, parentNode = None ):
		topNode, rootCtrl, meshList, curveList, edgeLoop, grpList, subGrpList = self.getSelection()
		rigMesh =  ma.listRelatives( self.activeRig, type='mesh', ad=1, pa=1 )

		#EMPTY/Non Standard object
		if grpList == [] and meshList == [] and curveList == [] and edgeLoop == [] and rootCtrl == None and topNode == None:
			selection = ma.ls( sl=1 )
			if selection == []:
				cmdWarn( dict_help.get( 'warning' ).get( 'nothingSelected' ) )
			else:
				for n in selection:
					#is it constrained?
					for child in getChildren( n ):
						if ma.nodeType( child ) == 'parentConstraint' or ma.nodeType( child ) == 'scaleConstraint':
							ma.delete( child )
							if printState == True:
								cmdPrint( child + ' removed' )
					#is it parented ?
					parentWorld( n )


		#GROUP ONLY
		elif grpList != [] and meshList == [] and curveList == [] and edgeLoop == [] and rootCtrl == None and topNode == None:
			for grp in grpList:
				#is it constrained?
				for child in getChildren( grp ):
					if ma.nodeType( child ) == 'parentConstraint' or ma.nodeType( child ) == 'scaleConstraint':
						ma.delete( child )
						if printState == True:
							cmdPrint( child + ' removed' )

				if parentNode != None:
					#is it constrained?
					for child in getChildren( parentNode ):
						if ma.nodeType( child ) == 'parentConstraint' or ma.nodeType( child ) == 'scaleConstraint':
							ma.delete( child )
							if printState == True:
								cmdPrint( child + ' removed' )

					#is it parented to the rig?
					if getParent( parentNode ) == self.renderGrp:
						parentWorld( parentNode )

				else:
					#is it parented to the rig?
					if getShape( grp ) in rigMesh:
						parentWorld( n )
				
				#check children
				meshList = self.getGroupedMesh( grp )
				if meshList != []:
					ma.select( meshList )
					self.disconnectMesh( printState, parentNode )
					
			#restore selection
			ma.select( grpList )
			return True


		#MESH ONLY
		elif meshList != [] and grpList == [] and curveList == [] and edgeLoop == [] and rootCtrl == None and topNode == None:
			for n in meshList:
				#unlock
				unlockTransforms( n )

				#is it skinned?
				skinNode = getSkin( n )
				if skinNode != None:
					#remove skin
					ma.delete( skinNode )
					if printState == True:
						cmdPrint( n + ' ' + dict_help.get( 'success' ).get( 'remove' ) )
				
				#is it constrained?
				for child in getChildren( n ):
					if ma.nodeType( child ) == 'parentConstraint' or ma.nodeType( child ) == 'scaleConstraint':
						ma.delete( child )
						if printState == True:
							cmdPrint( child + ' removed' )

				if parentNode != None:
					#is it constrained?
					for child in getChildren( parentNode ):
						if ma.nodeType( child ) == 'parentConstraint' or ma.nodeType( child ) == 'scaleConstraint':
							ma.delete( child )
							if printState == True:
								cmdPrint( child + ' removed' )

					#is it parented to the rig?
					if getParent( parentNode ) == self.renderGrp:
						parentWorld( parentNode )

				else:
					#is it parented to the rig?
					if getShape( n ) in rigMesh:
						parentWorld( n )

		else:
			cmdWarn( dict_help.get( 'warning' ).get( 'invalidSelection' ) )










######################################################################################################################################
#MOTION PATH
######################################################################################################################################
class motionPath( rigConnect ):
	def __init__( self ):
		rigConnect.__init__( self )
		self.curvePathPfx = 'path_'
		self.conditionSfx = 'CDN'
		self.attr_autoSteer = 'autoSteer'
		self.attr_curvePath = 'curvePath'
		self.attr_globalScale = 'globalScale'
		self.attr_curveScale = 'curveScale'
		self.attr_curveMirror = 'curveMirror'
		self.attr_pathSpin = 'pathSpin'
		self.attr_globalScaleINV = 'globalScaleINV'
		self.attr_steerMotion = 'motionSteer'
		self.attr_frontMotion = 'motionFront'
		self.attr_rearMotion = 'motionRear'
		self.attr_frontTwist = 'frontTwist'
		self.attr_motion = 'motion'
		self.tagID_cPlug = 'cPlug'
		self.defaultSlots = 6 #number of default curvePaths
		self.scaleAttrList = [ self.attr_globalScale, self.attr_curveScale, self.attr_curveMirror ]
		self.defaultScalePose = [ 1.0, 1.0, 0 ]

	def getPathCache( self, index ):
		#retrieves the path components of a given index
		pathInfo = self.getCACHE( str( index ) )
		if pathInfo != None:
			connectables = eval( pathInfo )
			return connectables
		return None, None


	def setPathCache( self, index, connectables ):
		#stores the names of all path components of given index on the activeRig
		attr = self.attr_connectCache + str( index)
		if not ma.attributeQuery( attr, n = self.activeRig, ex = 1 ):
			ma.addAttr( self.activeRig, ln = attr, dt = 'string' )
		ma.setAttr( self.activeRig + '.' + attr, str( connectables ), type = 'string' )
		

	def getAllCurvePaths( self ):
		return self.getDefaultCurvePaths() + self.getUserCurvePaths()


	def getDefaultCurvePaths( self ):
		return ma.addAttr( self.rootCtrl + '.' + self.attr_curvePath, q=1, en=1 ).split( ':' )[ 0 : self.defaultSlots + 1]
	

	def getUserCurvePaths( self ):
		allCurvePaths = ma.addAttr( self.rootCtrl + '.' + self.attr_curvePath, q=1, en=1 ).split( ':' )
		if len( allCurvePaths ) > self.defaultSlots + 1:
			return allCurvePaths[ self.defaultSlots + 1: ]
		else:
			return []


	def getActiveCurvePath( self ): #returns index, pathName
		pathIndex = ma.getAttr( self.rootCtrl + '.' + self.attr_curvePath )
		return pathIndex, self.getAllCurvePaths()[ pathIndex ]


	def createCurveGrp( self, curveName ):
		curveGrp = ma.rename( ma.group( em=1 ), curveName + '_grp' )
		return curveGrp


	def createCurvePt( self, curveName ):
		curvePt = ma.rename( ma.spaceLocator(), curveName + '_pt' )
		return curvePt


	def addAttribute( self, n, attrName ):
		if not ma.attributeQuery( attrName, n = n, ex = 1 ):
			ma.addAttr( n, ln = attrName )
			ma.setAttr( n + '.' + attrName, e=1, k=1, cb=0 )


	def edgeLoopToCurve( self, edgeLoop ): 
		ma.select( edgeLoop )
		#maya default polyToCurve is not very good with corners
		return ma.rename( ma.polyToCurve(  form=2, degree=3, ch=0 )[0], edgeLoop[-1].split( '.e[' )[0] + 'Path' )
		# vectorList = []
		# cmdMel( "PolySelectConvert 3;" )
		# for vtx in ma.ls( sl=1, fl=1 ):
		# 	vectorList.append( ma.xform( vtx, q=1, t=1, ws=1 ) )
		# return ma.rename( self.buildCurve( vectorList ), vtx.split( ':' )[-1].split( '.vtx' )[0] + 'Path' )
	

	def getScalePose( self ):
		#gets all scale attribute values
		scalePose = []
		for attr in self.scaleAttrList:
			scalePose.append( ma.getAttr( self.rootCtrl + '.' + attr ) )
		return scalePose


	def setScalePose( self, scalePose ):
		for attr in self.scaleAttrList:
			value = scalePose[ self.scaleAttrList.index( attr ) ]
			ma.setAttr( self.rootCtrl + '.' + attr, value )
	

	def addToPathDropDown( self, cPath ):
		allCurvePaths = self.getAllCurvePaths()

		if cPath not in allCurvePaths:
			allCurvePaths.append( cPath )
		else:
			return None
		
		enumName = ''
		for cPath in allCurvePaths:
			enumName += cPath + ':'
		
		ma.addAttr( self.rootCtrl + '.' + self.attr_curvePath, e=1, en=enumName )
		return len( allCurvePaths ) - 1
		

	def removeFromPathDropDown( self, index ):
		allCurvePaths = self.getAllCurvePaths()
		cPath = allCurvePaths[ index ]
		allCurvePaths.remove( cPath )

		enumName = ''
		for cPath in allCurvePaths:
			enumName += cPath + ':'
		
		ma.addAttr( self.rootCtrl + '.' + self.attr_curvePath, e=1, en=enumName )
		ma.setAttr( self.rootCtrl + '.' + self.attr_curvePath, 0 ) #turn curvePath off
		return len( allCurvePaths ) - 1
		


	def removeCurvePath( self, pathIndex = None ):
		allCurvePaths = self.getAllCurvePaths()
		if pathIndex == None:
			pathIndex, cPath = self.getActiveCurvePath()
		
		curvePathCount = len( allCurvePaths ) -1
		if pathIndex > self.defaultSlots:

			connectables = self.getPathCache( pathIndex )
			if connectables != None:
				for n in connectables:
					if ma.objExists( n ):
						ma.delete( n )

				if int( pathIndex ) < int( curvePathCount ):
					slotsToShiftUp = curvePathCount - pathIndex
					for i in range( 0, slotsToShiftUp ):
						oldIndex, newIndex = pathIndex + 1 + i, pathIndex + i
						connectables = self.getPathCache( oldIndex )
						self.disconnectPath( oldIndex, connectables )
						self.connectPath( newIndex, connectables )

				self.removeFromPathDropDown( pathIndex )
				cmdPrint( allCurvePaths[ pathIndex ] + dict_help.get( 'success' ).get( 'removeActivePath' ) )
				#wipe cache
				self.setPathCache( pathIndex, None )
				return True

			return False
		else:
			if pathIndex == 0:
				cmdPrint( dict_help.get( 'warning' ).get( 'noActivePath' ) )
			else:

				cmdPrint( allCurvePaths[ pathIndex ] + dict_help.get( 'warning' ).get( 'removeActivePath' ) )




	def removeAllUserCurvePaths( self ):
		allCurvePaths = self.getAllCurvePaths()
		for i in range( len( allCurvePaths ) - 1, self.defaultSlots, -1 ):
			self.removeCurvePath( i )
		setTransform( self.rootCtrl, [0,0,0] )
		cmdPrint( dict_help.get( 'label' ).get( 'removeAllPaths' ) )

		#CLEAN OUT ALL BROKEN PATHS/GROUPS
		curvePathDataCount = len( getChildren( self.curvePathGrp ) )
		if curvePathDataCount > self.defaultSlots:
			for i in range( self.defaultSlots + 1, curvePathDataCount + 1):
				connectables = self.getPathCache( i )
				if connectables != None:
					for n in connectables:
						if ma.objExists( n ):
							ma.delete( n )
				self.setPathCache( i, None )




	def addDefaultCurvePath( self, cPath, vectorList, pathIndex, closeCurve = False ):
		connectables = self.addPath( cPath, vectorList, pathIndex, closeCurve )
		self.connectPath( pathIndex, connectables )



	def reAddPathsToReferencedRig( self ):
		#when a user references in a rig, added paths to not stay in the list. This refreshes the list if a curve is found without an attribute
		#check if curvePath dir contains user paths:
		curveCount = len( getChildren( self.curvePathGrp ) ) 
		if curveCount > self.defaultSlots:#6
			if len( getChildren( self.curvePtGrp ) ) > self.defaultSlots: #6
				if self.getUserCurvePaths() == []:
					for i in range( self.defaultSlots + 1, curveCount + 1 ):
						curveName =  self.getPathCache( i )[-3].split( self.curvePathGrp.split( 'CurvePath' )[0] + self.curvePathPfx )[-1]
						pathIndex = self.addToPathDropDown( curveName )
						cmdPrint( 'relinked referenced path: ' + curveName )



	def addUserCurvePath( self, preservePosition = True, reverse = False ):
		topNode, rootCtrl, meshList, curveList, edgeLoop, grpList, subGrpList = self.getSelection()

		#accepts selected curves or a mesh edge loop
		if edgeLoop != []:
			cmdPrint( dict_help.get( 'warning' ).get( 'noCurve' ) )
			curveList = [ self.edgeLoopToCurve( edgeLoop ) ]
		
		if curveList != []:
			for cPath in curveList:
				
				#in case it is a dupe of an existing curve in rig
				parentWorld( cPath )
				unlockTransforms( cPath, True )

				
				if reverse == True:
					ma.reverseCurve( cPath )

				self.forceCurveUpdate( cPath )

				#add the attribute
				pathIndex = self.addToPathDropDown( cPath.split( ':' )[-1] )
				
				if pathIndex != None:
					#is the curve a continous loop? - not needed in user paths
					# closedCurve = True if ma.getAttr( getShape( cPath ) + '.form' ) != 0 else False

					#store current scale
					gScale, cScale, cMirror  = self.getScalePose()
					scale = gScale * cScale 
					#inverseScale
					scaleINV = scale / math.pow( scale, 2.0 )

					#get offset from origin
					offset = ma.xform( cPath + '.cv[0]', q=1, t=1, ws=1 )
					
					#duplicate curve and hide it.
					dupe = ma.duplicate( cPath )[0]
					ma.setAttr( dupe + '.' + v, 0 )

					#move curve pivot to 1st pt
					freezeTransforms( cPath )
					ma.xform( cPath, piv = offset, ws=1 )

					#set scale + position
					setTransform( cPath, [ -offset[0] * 1.0, -offset[1] * 1.0, -offset[2] * 1.0 ] )

					#if mirror mode is on - setPivot to 1st pt
					if cMirror != 0:
						freezeTransforms( cPath )
						setTransform( cPath, None, None, [ -1.0, 1.0, 1.0 ] )
					
					# #reset pivot
					ma.xform( cPath, piv = [ 0, 0, 0 ], ws=1 )
					freezeTransforms( cPath )

					#add path
					connectables = self.addPath( cPath, cPath, pathIndex, False )

					#rename original
					ma.rename( dupe, cPath )
					
					if preservePosition == True:
						#move root ctrl to the curve pt 1 location
						setTransform( self.rootCtrl, [ 0, 0, 0 ], [ 0, 0, 0 ] )#[ offset[0], offset[1], offset[2] ] )
					
					#setCache
					self.setPathCache( pathIndex, connectables )
					
					#connect to rig
					self.connectPath( pathIndex, connectables )

					if preservePosition == True:
						#move root ctrl to the curve pt 1 location
						setTransform( self.rootCtrl, offset )#[ offset[0], offset[1], offset[2] ] )
					
					#set the active path
					ma.setAttr( self.rootCtrl + '.' + self.attr_curvePath, pathIndex )
					
					# return connectables[-3]


				else:
					cmdPrint( cPath + dict_help.get( 'warning' ).get( 'addPathInvalidName' ) )
				
			ma.select( self.rootCtrl)
			if edgeLoop != []:
				cmdPrint( cPath + dict_help.get( 'success' ).get( 'addPathFromEdgeLoop' ) )
			else:
				cmdPrint( dict_help.get( 'success' ).get( 'addPathFromCurve' ) )
		

	def cleanup( self, nList ):
		nList_clean = []
		for n in nList:
			#set nonKeyable
			for tf in transforms:
				for ax in axis:
					if ma.attributeQuery(  tf + ax, n = n, ex = 1 ):
						ma.setAttr( n + '.' + tf + ax, k=0 )

			#add product abrev prefix and namespace if present
			n = ma.rename( n, self.nameSpc + self.abrev + '_' + n )
			nList_clean.append( n )

		return nList_clean


	def buildCurve( self, vectorList ): 
		#builds a curve from given vector points
		degreeValue = 2
		knotCount = len( vectorList ) + degreeValue -1
		knotList = []
		for i in range( 0, knotCount ):
			if i == 0 or i == 1:
				knotList.append( 0 )
			elif i > 1 and i < knotCount - 2:
				knotList.append( i - 1 )
			else:
				knotList.append( knotCount - 3 )
		newCurve = ma.curve( n = 'newCurve', d = degreeValue, p = vectorList, k = knotList )
		return newCurve


	def convertDoubleLinear( self, curvePathNode ):
		#removes doubleLinear nodes and connects them using "allCoordinates" to translation -used for curvepaths only at the moment
		dblLinearList, outList = getConnectionByType( curvePathNode, 'addDoubleLinear' ), []
		for dl in dblLinearList:
			outList += getConnectionOut( dl )
		outList = list( set( outList ) )
		ma.delete( dblLinearList )
		for o in outList:
			for ax in axis:
				ma.connectAttr( curvePathNode + '.' + ax.lower() + 'Coordinate', o + '.' + t + ax )


	def forceCurveUpdate( self, curve = None ):
		if curve == None:
			selected = ma.ls( sl=1 )
			if selected != []:
				curve = selected[0]
			else:
				cmdWarn( dict_help.get( 'warning' ).get( 'nothingSelected' ) )
				return False
		#temporarily moves points slightly to force maya to update curve shape.
		cmdMel( 'SelectCurveCVsAll;' )
		for cv in ma.ls( sl=1,fl=1):
			ma.move( 0.001, 0.001, 0.001, cv, r=1 )
			ma.move( -0.001, -0.001, -0.001, cv, r=1 )
		
		#update viewport by moving curve slightly and returning it - maya 2022 has an display issue
		ma.move( 0.001, 0.001, 0.001, curve, r=1 )
		ma.move( -0.001, -0.001, -0.001, curve, r=1 )

		ma.select( curve )
		cmdPrint( dict_help.get( 'success' ).get( 'curveUpdate' ) )
		return True


	def addPathAnimation( self, curve, curvePt, vectorControl, attributeName = False ): 
		attributeList = [ 'motion', self.attr_frontTwist, 'upTwist', 'sideTwist' ]
		ma.xform( vectorControl, t=getObjectCenter( curve ), ws=1 )
		
		if attributeName == False:
			self.addAttribute( vectorControl, attributeList[0] )
		
		for attr in attributeList:
			if attr != attributeList[0]:
				self.addAttribute( vectorControl, attr )
		
		path = ma.pathAnimation( curvePt, c=curve, n=curvePt + '_curvePath', fm=1, f=1, fa='z', ua='y', wut='object', wuo=vectorControl, iu=0, inverseFront=0, b=0 )
		ma.cutKey( path )
		driven = path + '.' + 'uValue' # renamed spin to uValue
		
		if attributeName != False:
			attr = attributeName
			self.addAttribute( vectorControl, attr )
		else:
			attr = attributeList[0]

		ma.setDrivenKeyframe( driven, cd=vectorControl + '.' + attr, dv= 0.0, v=0, itt = 'linear', ott = 'linear' )
		ma.setDrivenKeyframe( driven, cd=vectorControl + '.' + attr, dv=1.0, v=sceneUnitMultiplier, itt = 'linear', ott = 'linear' )
		ma.setInfinity( driven, pri='cycle', poi='cycle' )
		
		for attr in attributeList:
			if attr != attributeList[0]:
				ma.connectAttr( vectorControl + '.' + attr, path + '.' + attr, f=1 )

		self.convertDoubleLinear( path )
		
		return vectorControl, curve, curvePt


	def addPath( self, cPath, vectorList, pathIndex, closeCurve = False ):
		#build curves & grps
		if type( vectorList ) == str or type( vectorList ) == unicode:
			mainPath = rename( cPath, self.curvePathPfx + cPath.split( ':' )[-1] )
			freezeTransforms( mainPath )
			noSpinPath = rename( ma.duplicate( mainPath )[0], self.curvePathPfx + cPath + '_noSpinPath' )
		else:
			mainPath = rename( self.buildCurve( vectorList ), self.curvePathPfx + cPath )
			noSpinPath = rename( self.buildCurve( vectorList ), self.curvePathPfx + cPath + '_noSpinPath' )
		curveGrp = self.createCurveGrp( self.curvePathPfx + cPath )
		ptGrp = self.createCurveGrp( self.curvePathPfx + cPath + 'Pt' )

		#close certain curves
		if closeCurve == True:
			ma.closeCurve( mainPath, ch=0, ps=1, rpo=1, bb=0.5, bki=0, p=0.1 )
			ma.closeCurve( noSpinPath, ch=0, ps=1, rpo=1, bb=0.5, bki=0, p=0.1 )


		#link each noSpinPath cv directly to mainPath cvs
		mainListCV = buildCurveComponentList( mainPath )
		noSpinListCV = buildCurveComponentList( noSpinPath )
		for ii in range( 0, len( mainListCV ) ):
			ma.connectAttr( getShape( mainListCV[ii] ) + '.controlPoints[' + str( ii ) + ']', getShape( noSpinListCV[ii] ) + '.controlPoints[' + str( ii ) + ']', f=1 )

		
		#move vector curve above main curve and hide it
		ma.xform( noSpinPath, t=[ 0.0, 50.0, 0.0 ], ws=1 )
		ma.setAttr( noSpinPath + '.' + v, 0 )
		
		#noSpinPath follows mainPath
		ma.parentConstraint( mainPath, noSpinPath, mo=1 )

		#parent
		ma.parent( [ mainPath, noSpinPath ], curveGrp ),
		ma.parent( curveGrp, self.curvePathGrp )

		#reset
		resetAttributes( [ mainPath, noSpinPath, curveGrp, ptGrp ] )

		#motionPath connection pts
		mainPathUpVecPt = self.createCurvePt( mainPath + '_upVector' )
		noSpinPathUpVecPt = self.createCurvePt( noSpinPath + '_upVector' )
	
		#auto steering
		steerPt = self.createCurvePt( 'steer_' + mainPath )
		frontPt = self.createCurvePt( 'front_' + mainPath )
		rearPt = self.createCurvePt( 'rear_' + mainPath )

		#create main motion path setups
		self.addPathAnimation( mainPath, steerPt, mainPathUpVecPt, self.attr_steerMotion )
		self.addPathAnimation( mainPath, frontPt, mainPathUpVecPt, self.attr_frontMotion )
		self.addPathAnimation( mainPath, rearPt, mainPathUpVecPt, self.attr_rearMotion )
		self.addPathAnimation( noSpinPath, mainPathUpVecPt, noSpinPathUpVecPt, False )
		
		#curveLength info
		arclenNode = ma.rename( ma.arclen( mainPath, ch= True ), mainPath + '_' + 'curveInfo' )

		#autoSteerAimSetup
		autoSteerUpVecPt = self.createCurvePt( mainPath + '_' + self.attr_autoSteer + 'UpVector' )
		autoSteerAimPt = self.createCurvePt( mainPath + '_' + self.attr_autoSteer + 'Aim' )
		autoPathAlignAimPt = self.createCurvePt( mainPath + '_' + self.attr_autoSteer + 'AlignAim' )
		ma.parent( [ autoSteerUpVecPt, autoSteerAimPt, autoPathAlignAimPt ], rearPt )
		resetAttributes( [ autoSteerUpVecPt, autoSteerAimPt, autoPathAlignAimPt ] )
		ma.setAttr( autoSteerUpVecPt + '.' + t + y, 50.0 )
		ma.aimConstraint( steerPt, autoSteerAimPt, aim=[ 0, 0, 1 ], worldUpObject = autoSteerUpVecPt, wut='object', mo=0, skip = 'none' )
		ma.aimConstraint( frontPt, autoPathAlignAimPt, aim=[ 0, 0, 1 ], worldUpObject = autoSteerUpVecPt, wut='object', mo=0, skip = 'none' )
		ma.parent( [ steerPt, frontPt, rearPt ] + [ mainPathUpVecPt, noSpinPathUpVecPt ], ptGrp )
		ma.parent( [ ptGrp ], self.curvePtGrp )

		#visibilityToggle		
		vis_CDN = ma.rename( ma.shadingNode( 'condition', au = 1 ), mainPath + '_' + v + '_' + self.conditionSfx )
		ma.setAttr( vis_CDN + '.operation', 0 ) #equal
		ma.setAttr( vis_CDN + '.colorIfTrueR', 1.0 )
		ma.setAttr( vis_CDN + '.colorIfFalseR', 0.0 )
		ma.connectAttr( vis_CDN + '.outColorR', curveGrp + '.' + v, f=1 )
		ma.connectAttr( vis_CDN + '.outColorR', ptGrp + '.' + v, f=1 )
		
		#setColor
		ma.setAttr( getTransform( mainPath ) + '.overrideEnabled', 1 )
		ma.setAttr( getTransform( mainPath ) + '.overrideColor', 3 )
		
		#update
		self.forceCurveUpdate( mainPath )
		self.forceCurveUpdate( noSpinPath )

		connectables = self.cleanup( [ mainPathUpVecPt, noSpinPathUpVecPt, steerPt, frontPt, rearPt, arclenNode,  autoSteerAimPt, autoPathAlignAimPt, curveGrp, ptGrp, vis_CDN, mainPath, noSpinPath, autoSteerUpVecPt ] )
		
		#cleanup all added objects/nodes
		return connectables


	def connectPath( self, pathIndex, connectables ):
		mainPathUpVecPt, noSpinPathUpVecPt, steerPt, frontPt, rearPt, arclenNode,  autoSteerAimPt, autoPathAlignAimPt, curveGrp, ptGrp, vis_CDN, mainPath, noSpinPath, autoSteerUpVecPt = connectables

		#visibility
		ma.setAttr( vis_CDN + '.secondTerm', pathIndex )
		ma.connectAttr( self.rootCtrl + '.' + self.attr_curvePath, vis_CDN + '.firstTerm', f=1 )

		#mirrorCurve
		ma.connectAttr(  self.cPlugList[0] + '.outColorR', mainPath + '.' + s + x, f=1 )
		ma.connectAttr(  self.cPlugList[0] + '.outColorR', noSpinPath + '.' + s + x, f=1 )
		# ma.connectAttr(  self.cPlugList[0] + '.outColorR', curveGrp + '.' + s + x, f=1 )

		#front/rear/steer pts
		ma.connectAttr( self.cPlugList[1] + '.outputX', mainPathUpVecPt + '.' + self.attr_rearMotion, f=1 )
		ma.connectAttr( self.cPlugList[1] + '.outputX', noSpinPathUpVecPt + '.' + self.attr_motion, f=1 )
		ma.connectAttr( self.cPlugList[2]+ '.outputX', mainPathUpVecPt + '.' + self.attr_steerMotion, f=1 )
		ma.connectAttr( self.cPlugList[2]+ '.outputY', mainPathUpVecPt + '.' + self.attr_frontMotion, f=1 )

		#arclen
		ma.connectAttr( arclenNode + '.arcLength', self.cPlugList[3] + '.input[ ' + str( pathIndex ) + ']', f=1 )

		#choiceConnection
		ma.connectAttr( autoSteerAimPt + '.' + r + y, self.cPlugList[4] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( autoPathAlignAimPt + '.' + r + x, self.cPlugList[5] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( autoPathAlignAimPt + '.' + r + y, self.cPlugList[6] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( autoPathAlignAimPt + '.' + r + z, self.cPlugList[7] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( mainPathUpVecPt + '.' + self.attr_rearMotion, self.cPlugList[8] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( rearPt + '.' + t + x, self.cPlugList[9] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( rearPt + '.' + t + y, self.cPlugList[10] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( rearPt + '.' + t + z, self.cPlugList[11] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( rearPt + '.' + r + x, self.cPlugList[12] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( rearPt + '.' + r + y, self.cPlugList[13] + '.input[ ' + str( pathIndex ) + ']', f=1 )
		ma.connectAttr( rearPt + '.' + r + z, self.cPlugList[14] + '.input[ ' + str( pathIndex ) + ']', f=1 )

		#pathSpin
		ma.connectAttr( self.driveCtrl + '.' + self.attr_pathSpin, mainPathUpVecPt + '.' + self.attr_frontTwist, f=1 )




	def disconnectPath( self, pathIndex, connectables ):
		mainPathUpVecPt, noSpinPathUpVecPt, steerPt, frontPt, rearPt, arclenNode,  autoSteerAimPt, autoPathAlignAimPt, curveGrp, ptGrp, vis_CDN, mainPath, noSpinPath, autoSteerUpVecPt = connectables
		
		#visibility
		ma.setAttr( vis_CDN + '.secondTerm', pathIndex )
		ma.disconnectAttr( self.rootCtrl + '.' + self.attr_curvePath, vis_CDN + '.firstTerm' )

		#mirrorCurve
		ma.disconnectAttr(  self.cPlugList[0] + '.outColorR', curveGrp + '.' + s + x )

		#front/rear/steer pts
		ma.disconnectAttr( self.cPlugList[1] + '.outputX', mainPathUpVecPt + '.' + self.attr_rearMotion )
		ma.disconnectAttr( self.cPlugList[1] + '.outputX', noSpinPathUpVecPt + '.' + self.attr_motion )
		ma.disconnectAttr( self.cPlugList[2]+ '.outputX', mainPathUpVecPt + '.' + self.attr_steerMotion )
		ma.disconnectAttr( self.cPlugList[2]+ '.outputY', mainPathUpVecPt + '.' + self.attr_frontMotion )

		#arclen
		ma.disconnectAttr( arclenNode + '.arcLength', self.cPlugList[3] + '.input[ ' + str( pathIndex ) + ']' )

		#choiceConnection
		ma.disconnectAttr( autoSteerAimPt + '.' + r + y, self.cPlugList[4] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( autoPathAlignAimPt + '.' + r + x, self.cPlugList[5] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( autoPathAlignAimPt + '.' + r + y, self.cPlugList[6] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( autoPathAlignAimPt + '.' + r + z, self.cPlugList[7] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( mainPathUpVecPt + '.' + self.attr_rearMotion, self.cPlugList[8] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( rearPt + '.' + t + x, self.cPlugList[9] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( rearPt + '.' + t + y, self.cPlugList[10] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( rearPt + '.' + t + z, self.cPlugList[11] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( rearPt + '.' + r + x, self.cPlugList[12] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( rearPt + '.' + r + y, self.cPlugList[13] + '.input[ ' + str( pathIndex ) + ']' )
		ma.disconnectAttr( rearPt + '.' + r + z, self.cPlugList[14] + '.input[ ' + str( pathIndex ) + ']' )
		
		#pathSpin
		ma.disconnectAttr( self.driveCtrl + '.' + self.attr_pathSpin, mainPathUpVecPt + '.' + self.attr_frontTwist )










######################################################################################################################################
#TERRAIN
######################################################################################################################################
class terrain( motionPath ):
	def __init__( self ):
		motionPath.__init__( self )
		self.muscleSfx, self.wrapSfx = '_host', '_wrap'
		self.attrTerrainOffset = 'terrainOffset'


	def getHost( self, n ): #returns the host muscle object attached to n (It is also parented to it.)
		for history in ma.listHistory( n ):
			if ma.nodeType( history ) == 'cMuscleObject':
				return history
		return None


	def getWraps( self, n ):#returns any attached muscle nodes that are connected to n 
		activeWraps = []
		host = self.getHost( n )
		if host == None:
			cmdWarn( 'No host node found for ' + n )
		else:
			for connection in getConnectionOut( host ):
				if ma.nodeType( connection ) == 'cMuscleSystem':
					activeWraps.append( connection )
		
		return activeWraps
	

	def getWrapMesh( self, n ): #returns any attached mesh that are connected to n 
		activeWrapMesh = []
		activeWraps = self.getWraps( n )
		if activeWraps == []:
			cmdWarn( 'No wrap nodes found connected to ' + n )
		else:
			for activeWrap in activeWraps:
				for connection in getConnectionOut( activeWrap ):
					if ma.nodeType( connection ) == 'transform':
						if connection != n:
							shape = getShape( connection )
							if type( shape ) == list:
								shape = shape[0]
							if ma.nodeType( shape ) == 'mesh':
								activeWrapMesh.append( connection )
		return activeWrapMesh


	def removeTerrain( self, n ):
		#remove current vehicles wraps and geometry constraints
		host = self.getHost( n )
		activeWraps = self.getWraps( n )

		if activeWraps != []:
			ma.delete( activeWraps )
			cmdPrint( 'Removed all vehicles from ' + n )

		if host != []:
			ma.delete( host )
			cmdPrint( 'Removed terrain wrap host' )

		else:
			cmdWarn( 'Selected object is not connected to a vehicle as a terrain.' )



	def addTerrain( self, terrainMesh ):
		self.wrapPlaneGrp = self.ensureExists( self.getCACHE( self.tagID_wrapPlaneGrp ) )

		if self.wrapPlaneGrp == None:
			cmdWarn( 'No wrap planes found. Ensure your vehicle is rigged using version 2.8 or above.' )

		else:
			terrainShape = getShape( terrainMesh )
			newWrapList, activeVehicleWrapMesh = [], []
			
			#get active vehicle wrap mesh
			wrapCache = eval( self.getCACHE( self.tagID_wheel, 'wrap' ) ) 
			for wrap in wrapCache:
				activeVehicleWrapMesh.append( self.ensureExists( wrap ) )

			#is the terrain already connected to other vehicle wraps?
			currentlyConnectedWrapMesh = self.getWrapMesh( terrainMesh )

			if currentlyConnectedWrapMesh != []:
				#is active vehicle already connected?
				for activeWrap in activeVehicleWrapMesh:
					if activeWrap in currentlyConnectedWrapMesh:
						cmdWarn( 'Vehicle already connected.' )
						return True
					else:
						nList = activeVehicleWrapMesh + currentlyConnectedWrapMesh
						#remove all connections
						self.removeTerrain( terrainMesh )
			else:
				nList = activeVehicleWrapMesh
				

			for n in nList:
				if n != nList[-1]:
					#create using a temp plane
					tempPlane = ma.polyPlane( sw=1, sh=1, ch=0 )[-1]
					ma.select( tempPlane )
				else:
					#create using the terrainMesh
					ma.select( terrainMesh )
				
				muscle = mel.eval( 'cMuscle_makeMuscle( 0 )' )[0]
				muscle = ma.rename( muscle, terrainMesh + self.muscleSfx )
				ma.setAttr( muscle + '.fat', 0.0 )
				ma.select( n )
				
				#clear any potential issue
				ma.delete( n, ch=1 )

				wrap = mel.eval( 'cMuscle_makeMuscleSystem( 1 )' )
				wrap = ma.rename( wrap, n + self.wrapSfx )
				newWrapList.append( wrap )
				
				#terrain offset
				if not ma.isConnected( self.driveCtrl + '.' + self.attrTerrainOffset,  muscle + '.fat' ):
					ma.connectAttr( self.driveCtrl + '.' + self.attrTerrainOffset,  muscle + '.fat' )
			
				ma.setAttr( wrap + '.shrinkWrap', 1 )
				ma.setAttr( wrap + '.enableSliding', 1 )

				if n != nList[-1]:
					ma.select( tempPlane, add=1 )
				else:
					ma.select( terrainMesh, add=1 )

				mel.eval( 'cMuscle_connectToSystem()' )

				vertCount = ma.polyEvaluate( n, v=1 )
				
				#set weights
				for i in range( 0, vertCount ):
					mel.eval( 'cMuscleWeight -muscle "' + muscle + '" -v 1.0 -normalize false -wt "sliding" -system "' + wrap + '" ' + n + '.vtx[' + str( i ) + ']' )
				
				if n != nList[-1]:
					#replace tempPlane connections with terrainMesh
					ma.connectAttr( terrainMesh + '.worldMatrix[0]',  muscle + '.worldMatrixStart', f=1 )
					ma.connectAttr( terrainShape + '.worldMesh[0]',  muscle + '.meshIn', f=1 )		
					#remove tempPlane
					ma.delete( tempPlane )

			for wrap in newWrapList:
				try:
					if not ma.isConnected( muscle + '.muscleData',  wrap + '.muscleData[0]' ):
						ma.connectAttr( muscle + '.muscleData',  wrap + '.muscleData[0]', f=1 )
				except:
					pass
					# cmdWarn( 'failed to connect: ' + muscle + '.muscleData' +  ' to ' + wrap + '.muscleData[0]' )
				
				if wrap != newWrapList[-1]:
					try:
						if not ma.isConnected( newWrapList[ 1 ] + '.offset', wrap + '.offset' ):
							ma.connectAttr( newWrapList[ 1 ] + '.offset', wrap + '.offset', f=1 )
					except:
						pass
						# cmdWarn( 'failed to connect: ' + newWrapList[ 1 ] + '.offset' + ' to ' +  wrap + '.offset', )
			
			ma.select( terrainMesh )
			cmdPrint( 'Vehicle connected to ' + terrainMesh )







######################################################################################################################################
#UI
######################################################################################################################################
class ui( terrain ):
	def __init__( self, version = '' ):
		terrain.__init__( self )

		#location
		self.location_UI = ( 350, 350 )
		self.location_popupOffset = ( 150, 8 )
		
		#setUI
		self.setUI_topbar, self.setUI_autoSize, self.setUI_sizable = 1, 1, 0
		
		#namingUI
		self.version = version
		self.name_tool = product
		self.name_popupHelp = 'popupHelp'
		self.title_main = self.name_tool + ' ' + str( self.version ) + ' - ' + webSite
		self.title_popupHelp = self.name_tool + ' - help'

		#size
		self.size_UI = [ 400, 80 ]
		self.size_button = [ 150, 25 ]
		self.size_icon = 25
		self.size_helpPopup = [ 390, 20 ] 
		self.size_userInput = [ 160, 30 ]
		
		#color
		self.color_dark = [ 0.15, 0.15, 0.15 ]
		self.color_disable = [ 0.25, 0.25, 0.25 ]
		self.color_grey = [ 0.8, 0.8, 0.8 ]
		self.color_highlight = [ 0.706, 0.855, 1.0 ]
		self.color_red = [ 0.499, 0.314, 0.314 ]
		self.color_redDark = [ 0.399, 0.214, 0.214 ]
		self.color_violet = [ 0.36, 0.345, 0.439 ]
		self.color_brown = [ 0.5, 0.4, 0.4 ]
		self.color_orange = [ 0.499, 0.330, 0.216 ]
		self.color_purple = [ 0.427, 0.345, 0.439 ]
		self.color_purpleDark = [ 0.327, 0.245, 0.339 ]
		self.color_blue = [ 0.245, 0.3, 0.339 ]
		self.color_green = [ 0.302, 0.459, 0.376 ]
		self.color_forest = [ 0.2, 0.3, 0.2 ]
		self.color_gold = [ 0.8, 0.7, 0.2 ]	

		#icon
		self.icon_uacr =  iconDir + 'icon_UltimateAdjustableCarRig.png'
		self.icon_remove = iconDir + 'icon_remove.png'
		self.icon_removeOff = iconDir + 'icon_removeOff.png'
		self.icon_trickBox = iconDir + 'icon_trickbox.png'
		# self.icon_help = 'menuIconHelp.png'
		self.icon_connect_body = iconDir + 'icon_connect_body.png'
		self.icon_connect_bonnet = iconDir + 'icon_connect_bonnet.png'
		self.icon_connect_boot = iconDir + 'icon_connect_boot.png'
		self.icon_connect_caliper = iconDir + 'icon_connect_caliper.png'
		self.icon_connect_doorBack = iconDir + 'icon_connect_doorBack.png'
		self.icon_connect_doorFront = iconDir + 'icon_connect_doorFront.png'
		self.icon_connect_steeringWheel = iconDir + 'icon_connect_steeringWheel.png'
		self.icon_connect_tire = iconDir + 'icon_connect_tire.png'
		self.icon_connect_wheel = iconDir + 'icon_connect_wheel.png'


		#active
		self.active_vehicle = None
		self.enableFunctions = True

		#labels
		self.label_connectSkin = dict_help.get( 'label' ).get( 'connectSkin' )
		self.label_connectParent = dict_help.get( 'label' ).get( 'connectParent' )
		self.label_connectConstraint = dict_help.get( 'label' ).get( 'connectConstraint' )
		self.label_connectRemove = dict_help.get( 'label' ).get( 'connectRemove' )
		self.label_curvePath = dict_help.get( 'label' ).get( 'curvePath' )
		self.label_setActiveRig = dict_help.get( 'label' ).get( 'setActiveRig' )
		self.label_addPath = dict_help.get( 'label' ).get( 'addPath' )
		self.label_removeActivePath = dict_help.get( 'label' ).get( 'removeActivePath' )
		self.label_removeAllPaths = dict_help.get( 'label' ).get( 'removeAllPaths' )
		self.label_liteVersion = 'LT'
		self.label_chassisVersion = 'INCLUDE CHASSIS MODEL'
		self.label_keepPosition = 'KEEP POSITION'
		self.label_reverseCurve = 'REVERSE'
		self.label_proxyView = 'PROXY'
		self.label_chassisView = 'CHASSIS'
		self.label_steeringView = 'STEERING WHEEL'
		self.label_setup = 'SETUP'
		self.label_dynamic = 'DYNAMIC'
		self.label_resetPose = 'RESET'
		self.label_parentGeo = 'AUTO PARENT'
		self.label_unusedInfluence  = 'CLEAN UP'
		self.label_camTop = 'TOP'
		self.label_camFront = 'FRONT'
		self.label_camSide = 'SIDE'
		self.label_camPersp = 'PERSP'
		self.label_isolate = 'ISOLATE'
		self.button_liteVersion = 'liteVersion'
		self.button_chassisVersion = 'chassisVersion'
		self.button_wheelCount = 'wheelCount'
		self.button_wheelSpan = 'wheelSpan'
		self.button_resetPose = 'resetPose'
		self.button_setup = 'setup'
		self.button_dynamics = 'dynamics'
		self.button_proxyView = 'proxyView'
		self.button_chassisView = 'chassisView'
		self.button_steeringView = 'steeringView'
		self.button_activeRig = 'button_activeRig'
		self.button_parentGeo = 'button_parentGeo'
		self.button_connectionType = 'button_connectionType'
		self.button_connectionRemove = 'button_connectionRemove'
		self.button_keepPosition = 'button_keepPosition'
		self.button_reverseCurve = 'button_reverseCurve'
		self.button_unusedInfluence  = 'button_unusedInfluence'
		self.text_connectionType = 'text_connectionType'
		self.list_disable_buttons = []
		self.list_tagID_buttons = []
		self.label_activeRig = ''
		self.label_skin = 'SK'
		self.label_constraint = 'CN'
		self.label_parent = 'P'
		self.label_remove = 'X'
		self.list_connectToggle = [ self.label_skin, self.label_constraint, self.label_parent ] #self.label_remove 
		self.dict_connect = {
			self.label_skin : { 'color' : self.color_dark, 'label' : self.label_connectSkin },
			self.label_constraint : { 'color' : self.color_blue, 'label' : self.label_connectConstraint },
			self.label_parent : { 'color' : self.color_forest, 'label' : self.label_connectParent },
			self.label_remove : { 'color' : self.color_red, 'label' : self.label_connectRemove } }
		
		#wheelCount
		self.label_2 = '2'
		self.label_4 = '4'
		self.label_6 = '6'
		self.label_8 = '8'
		self.label_10 = '10'
		self.list_wheelCountToggle = [ self.label_4, self.label_6, self.label_8, self.label_10 ] # self.label_2
		self.dict_wheelCount = {
			self.label_2 : { 'color' : self.color_disable },
			self.label_4 : { 'color' : self.color_dark },
			self.label_6 : { 'color' : self.color_disable },
			self.label_8 : { 'color' : self.color_disable },
			self.label_10 : { 'color' : self.color_disable } }
		
		#wheelSpan
		self.label_0 = '0'
		self.label_20 = '20'
		self.label_48 = '48'
		self.label_72 = '72'
		self.list_wheelSpanToggle = [ self.label_0, self.label_20, self.label_48, self.label_72 ]
		self.dict_wheelSpan = {
			self.label_0 : { 'color' : self.color_disable },
			self.label_20 : { 'color' : self.color_dark },
			self.label_48 : { 'color' : self.color_disable },
			self.label_72 : { 'color' : self.color_disable } }


	def build( self ):
		#build main UI
		if ma.window( self.name_tool, q=1, ex=1 ):
			ma.deleteUI( self.name_tool )
		ma.window( self.name_tool, t=self.title_main, dtg='', ip=0, rtf=0, tb=self.setUI_topbar, s=self.setUI_sizable, ret=0 )
	
		#layout UI
		self.layout()
		
		#show main UI
		ma.showWindow( self.name_tool )
		ma.window( self.name_tool, e=1, tlc=self.location_UI, wh=self.size_UI, mnb=0, mxb=0, rtf=self.setUI_autoSize )

		#try to connect to rig
		self.updateActiveRigLayout( False )
		#set default connectionType
		self.connectionTypeToggle( self.label_skin, True )
		self.wheelCountToggle( self.label_4, True )
		self.wheelSpanToggle( self.label_0, True )
		#create/wipe storage lists
		self.createConnectionStorage()
		#setDefaultToggles
		# self.setToggleButton( self.button_liteVersion, self.label_liteVersion , None, False )
		self.setToggleButton( self.button_keepPosition, self.label_keepPosition , None, True )
		self.setToggleButton( self.button_chassisVersion, self.label_chassisVersion , None, True )
		self.setToggleButton( self.button_parentGeo, self.label_parentGeo , None, True )
		if self.rootCtrl != None:
			self.setToggleButton( self.button_proxyView, self.label_proxyView , None, ma.getAttr( self.rootCtrl + '.' + self.attr_showProxy )  )
			self.setToggleButton( self.button_chassisView, self.label_chassisView , None, ma.getAttr( self.rootCtrl + '.' + self.attr_showChassis ) )
			# self.setToggleButton( self.button_steeringView, self.label_steeringView , None, ma.getAttr( self.rootCtrl + '.' + self.attr_showSteeringWheel) )
			self.setToggleButton( self.button_dynamics, self.label_dynamic , None, ma.getAttr( self.bodyCtrl + '.' + self.attr_dynamics) )
			self.setToggleButton( self.button_setup, self.label_setup , None, ma.getAttr( self.rootCtrl + '.' + self.attr_controlType ) )

	def layout( self ):
		#ACTIVE RIG ###########################################################
		ma.frameLayout( lv=0, mw = 6, mh = 6 )
		ma.rowColumnLayout( nc=3 )
		#help button
		ma.nodeIconButton( l='', i=self.icon_trickBox, w=self.size_icon + 5, h=self.size_icon + 5, bgc=self.color_grey, c=lambda x=None : self.commandWebHelp() )
		ma.text( l='   Active Rig:  ', h=self.size_icon )
		#activeRig button
		ma.nodeIconButton( self.button_activeRig, l=self.label_activeRig, w=self.size_UI[0] / 1.325, h=self.size_button[1], fn='boldLabelFont', st='textOnly', bgc=self.color_dark, c=lambda x=True : self.updateActiveRigLayout( x ) )
		ma.setParent( '..' )

		ma.frameLayout( lv=0, mw = 6, mh = 6 )
		ma.rowColumnLayout( nc=7 )
		ma.text( l='   CHOOSE A RIG:', align='left', fn ='boldLabelFont', rs=0, h=20 )
		ma.text( l='        ', h=self.size_icon )
		
		ma.text( l='Wheel Count: ' )
		ma.nodeIconButton( self.button_wheelCount, l='', st='textOnly', mw=self.size_icon * 0.1, mh=self.size_icon * 0.1, w=self.size_icon * 1.1, h=self.size_icon, c=lambda x=None : self.wheelCountToggle() )
		ma.text( l='    ', h=self.size_icon )

		ma.text( l='Tire Deformation Divisions: ' )
		ma.nodeIconButton( self.button_wheelSpan, l='', st='textOnly', mw=self.size_icon * 0.1, mh=self.size_icon * 0.1, w=self.size_icon * 1.1, h=self.size_icon, c=lambda x=None : self.wheelSpanToggle() )
		ma.setParent( '..' )
		ma.rowColumnLayout( nc=5 )
		
		#LITE toggle
		# ma.nodeIconButton( self.button_liteVersion, l=self.label_liteVersion, w=self.size_icon, h=self.size_icon, st='textOnly', bgc=self.color_dark, c=lambda x=self.button_liteVersion, y= self.label_liteVersion : self.setToggleButton( x, y ) )
		# ma.text( l=' ' )

		#CHASSIS toggle
		ma.nodeIconButton( self.button_chassisVersion, l=self.label_chassisVersion, w=self.size_button[0] * 1.0, h=self.size_icon, st='textOnly', bgc=self.color_dark, c=lambda x=self.button_chassisVersion, y= self.label_chassisVersion : self.setToggleButton( x, y ) )
		ma.text( l='   ' )
		#LOADERS
		ma.nodeIconButton( l='REFERENCE', st='textOnly', w=self.size_button[0] / 2.0, h=self.size_button[1] * 1.0, bgc=self.color_gold, fn='boldLabelFont', c=lambda x='reference' : self.loadScene( x ) )
		# ma.text( l=' ' )
		ma.nodeIconButton( l='LOAD', st='textOnly', w=self.size_button[0] / 2.0, h=self.size_button[1] * 1.0, bgc=self.color_gold, fn='boldLabelFont', c=lambda x='load' : self.loadScene( x ) )
		# ma.text( l=' ' )
		ma.nodeIconButton( l='IMPORT', st='textOnly', w=self.size_button[0] / 2.0, h=self.size_button[1] * 1.0, bgc=self.color_gold, fn='boldLabelFont', c=lambda x='import' : self.loadScene( x ) )
		# ma.text( l='  ' )

		#POSE RESET -Future update?
		# self.list_disable_buttons.append( ma.nodeIconButton( self.button_resetPose, l=self.label_resetPose,  st='textOnly', w=self.size_button[0] / 3.25, h=self.size_button[1], bgc=self.color_grey, en=self.enableFunctions, c=lambda x= None : self.commandResetPose() ) )




		ma.setParent( '..' )
		ma.setParent( '..' )


		

		ma.frameLayout( lv=0, mw = 6, mh = 6 )
		ma.rowColumnLayout( nc=9 )
		ma.text( l='   VIEW:    ', align='left', fn ='boldLabelFont', rs=0, h=20 )
		
		#DYNAMICS
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_dynamics, l=self.label_dynamic,  st='textOnly', w=self.size_button[0] / 2.00, h=self.size_button[1], bgc=self.color_disable, en=self.enableFunctions, c=lambda x=self.button_dynamics, y= self.label_dynamic, z=self.attr_dynamics : self.setToggleButton( x, y, z ) ) )
		ma.text( l='  ' )
		
		#SHOW CHASSIS
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_chassisView, l=self.label_chassisView,  st='textOnly', w=self.size_button[0] / 2.7, h=self.size_button[1], bgc=self.color_disable, en=self.enableFunctions, c=lambda x=self.button_chassisView, y= self.label_chassisView, z=self.attr_showChassis: self.setToggleButton( x, y, z ) ) )
		ma.text( l='  ' )
		
		#PROXY/RENDER MODE
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_proxyView, l=self.label_proxyView,  st='textOnly', w=self.size_button[0] / 3.0, h=self.size_button[1], bgc=self.color_disable, en=self.enableFunctions, c=lambda x=self.button_proxyView, y= self.label_proxyView, z=self.attr_showProxy: self.setToggleButton( x, y, z ) ) )
		ma.text( l='           ' )

		ma.text( l='MODE:    ', fn ='boldLabelFont', rs=0, h=20 )
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_setup, l=self.label_setup,  st='textOnly', fn='boldLabelFont', w=self.size_button[0] / 3.0, h=self.size_button[1], bgc=self.color_disable, en=self.enableFunctions, c=lambda x=self.button_setup, y= self.label_setup, z=self.attr_controlType : self.setToggleButton( x, y, z ) ) )
		ma.setParent( '..' )

		#EDIT MODE
		ma.rowColumnLayout( nc=10 )
		# ma.text( l=' ', h=self.size_icon )
		#STEERING WHEEL
		# self.list_disable_buttons.append( ma.nodeIconButton( self.button_steeringView, l=self.label_steeringView,  st='textOnly', w=self.size_button[0] / 1.5, h=self.size_button[1], bgc=self.color_disable, en=self.enableFunctions, c=lambda x=self.button_steeringView, y= self.label_steeringView, z=self.attr_showSteeringWheel: self.setToggleButton( x, y, z ) ) )
		ma.text( l='   CAM:      ', fn ='boldLabelFont', rs=0, h=20 )
		ma.nodeIconButton( l=self.label_camTop, w=self.size_button[0] / 3.0, h=self.size_button[1], st='textOnly', bgc=self.color_grey, en=self.enableFunctions, c=lambda x=self.label_camTop : self.setActiveCamera( x ) )
		ma.text( l=' ' )
		ma.nodeIconButton( l=self.label_camFront, w=self.size_button[0] / 3.0, h=self.size_button[1], st='textOnly', bgc=self.color_grey, en=self.enableFunctions, c=lambda x=self.label_camFront : self.setActiveCamera( x ) )
		ma.text( l=' ' )
		ma.nodeIconButton( l=self.label_camSide, w=self.size_button[0] / 3.0, h=self.size_button[1], st='textOnly', bgc=self.color_grey, en=self.enableFunctions, c=lambda x=self.label_camSide : self.setActiveCamera( x ) )
		ma.text( l=' ' )
		ma.nodeIconButton( l=self.label_camPersp, w=self.size_button[0] / 3.0, h=self.size_button[1], st='textOnly', bgc=self.color_grey, en=self.enableFunctions, c=lambda x=self.label_camPersp : self.setActiveCamera( x ) )
		ma.text( l='       ' )
		ma.nodeIconButton( l=self.label_isolate, w=self.size_button[0] / 1.6, h=self.size_button[1], st='textOnly', fn='boldLabelFont', bgc=self.color_grey, en=self.enableFunctions, c=lambda : isolate() )
		
		ma.setParent( '..' )
		ma.setParent( '..' )
		ma.setParent( '..' )


		#CONNECTION ############################################################
		ma.frameLayout( lv=0, mw = 6, mh = 6 )
		ma.text( l='   VEHICLE CONNECT:', align='left', fn ='boldLabelFont', rs=0, h=20 )

		ma.rowColumnLayout( nc=5 )
		#connectionType toggle button
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_connectionType, l='', st='textOnly', mw=self.size_icon * 0.1, mh=self.size_icon * 0.1, w=self.size_icon, h=self.size_icon, en=self.enableFunctions, c=lambda x=None : self.connectionTypeToggle() ) )
		ma.text( l='    ', h=self.size_icon )
		ma.text( self.text_connectionType, l='', h = self.size_button[1] )
		ma.text( l=' ', h=self.size_icon )
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_parentGeo, l=self.label_parentGeo,  st='textOnly', w=self.size_button[0] / 1.3, h=self.size_button[1], bgc=self.color_disable, en=self.enableFunctions, c=lambda x=self.button_parentGeo, y= self.label_parentGeo : self.setToggleButton( x, y ) ) )
		ma.setParent( '..' )
		
		#connection buttons
		ma.rowColumnLayout( nc=( len( self.list_tagID ) * 2 ) + 1 )
		for tagID in self.list_tagID:
			label = tagID.upper() if tagID != 'steeringWheel' else  'STEERING\nWHEEL'
			if tagID != self.list_tagID[0]:
				ma.text( l=' ' )
			# button = ma.nodeIconButton( l=label, w=self.size_UI[0] / ( len( self.list_tagID ) * 1.2 ), h=self.size_button[1] * 1.3, fn='boldLabelFont', st='textOnly', bgc=self.color_dark, en=self.enableFunctions, c=lambda x=tagID: self.commandConnect( x ) )
			icon = iconDir + 'icon_connect_' + tagID + '.png'
			button = ma.nodeIconButton( l=label, w=self.size_UI[0] / ( len( self.list_tagID ) * 1.2 ), h=self.size_button[1] * 1.3, fn='boldLabelFont', st='iconOnly', bgc=self.color_dark, i = icon, en=self.enableFunctions, c=lambda x=tagID: self.commandConnect( x ) )

			self.list_disable_buttons.append( button )
			self.list_tagID_buttons.append( button )
		#connectionRemove button
		ma.text( l='   ' )
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_connectionRemove, l='[ ' + self.label_remove + ' ]', w=self.size_button[1] * 1.4, h=self.size_button[1], i=self.icon_remove, fn='boldLabelFont', bgc=self.color_red, en=self.enableFunctions, c=lambda x=None: self.disconnectMesh() ) )
		ma.setParent( '..' )
		

		#additional connection buttons (doors, bonnet etc)
		ma.rowColumnLayout( nc=( len( self.list_tagID2 ) * 2 ) )
		for tagID in self.list_tagID2:
			label = tagID.upper()
			if tagID == 'doorBack':
				label = 'DOOR\nBACK'
			if tagID == 'doorFront':
				label = 'DOOR\nFRONT'		
			
			# button = ma.nodeIconButton( l=label, w=self.size_UI[0] / ( len( self.list_tagID ) * 1.2 ), h=self.size_button[1] * 1.3, fn='boldLabelFont', st='textOnly', bgc=self.color_dark, en=self.enableFunctions, c=lambda x=tagID: self.commandConnect( x ) )
			icon = iconDir + 'icon_connect_' + tagID + '.png'
			button = ma.nodeIconButton( l=label, w=self.size_UI[0] / ( len( self.list_tagID ) * 1.2 ), h=self.size_button[1] * 1.3, fn='boldLabelFont', st='iconOnly', bgc=self.color_dark, i = icon, en=self.enableFunctions, c=lambda x=tagID: self.commandConnect( x ) )
			ma.text( l=' ' )

			self.list_disable_buttons.append( button )
			self.list_tagID_buttons.append( button )
		ma.setParent( '..' )



		ma.setParent( '..' )
		ma.setParent( '..' )
		ma.setParent( '..' )


		# self.list_tagID2
		# self.icon_connect_body = iconDir + 'icon_connect_body.png'
		# self.icon_connect_bonnet = iconDir + 'icon_connect_bonnet.png'
		# self.icon_connect_boot = iconDir + 'icon_connect_boot.png'
		# self.icon_connect_caliper = iconDir + 'icon_connect_caliper.png'
		# self.icon_connect_doorBack = iconDir + 'icon_connect_doorBack.png'
		# self.icon_connect_doorFront = iconDir + 'icon_connect_doorFront.png'
		# self.icon_connect_steeringWheel = iconDir + 'icon_connect_steeringWheel.png'
		# self.icon_connect_tire = iconDir + 'icon_connect_tire.png'
		# self.icon_connect_wheel = iconDir + 'icon_connect_wheel.png'










		#CURVE PATH ############################################################


		ma.frameLayout( lv=0, mw = 6, mh = 6 )
		ma.text( l='   CURVE PATH:', align='left', fn ='boldLabelFont', rs=0, h=20 )
		ma.rowColumnLayout( nc=6 )
		ma.text( l='   ' )
		ma.text( l=self.label_curvePath, h = self.size_icon )
		#keepCurvePosition button
		ma.text( l='     ' )
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_keepPosition, l=self.label_keepPosition, w=self.size_icon * 3.5, h=self.size_icon, bgc=self.color_disable, en=self.enableFunctions, st='textOnly', c=lambda x=self.button_keepPosition, y= self.label_keepPosition : self.setToggleButton( x, y ) ) )
		ma.text( l='  ' )
		self.list_disable_buttons.append( ma.nodeIconButton( self.button_reverseCurve, l=self.label_reverseCurve, w=self.size_icon * 2.5, h=self.size_icon, bgc=self.color_disable, en=self.enableFunctions, st='textOnly', c=lambda x=self.button_reverseCurve, y= self.label_reverseCurve : self.setToggleButton( x, y ) ) )
		ma.setParent( '..' )
		
		#REMOVE ALL CURVE PATH
		ma.rowColumnLayout( nc=5)
		self.list_disable_buttons.append( ma.nodeIconButton( l=self.label_removeAllPaths, w=self.size_UI[0] / 4.0, h=self.size_button[1] * 2.0, fn='boldLabelFont', st='textOnly', bgc=self.color_redDark, en=self.enableFunctions, c=lambda x='removeAll': self.commandPath( x ) ) )
		ma.text( l='      ' )
		#REMOVE CURVE PATH
		self.list_disable_buttons.append( ma.nodeIconButton( l=self.label_removeActivePath, w=self.size_UI[0] / 3.0, h=self.size_button[1] * 2.0, fn='boldLabelFont', st='textOnly', bgc=self.color_red, en=self.enableFunctions, c=lambda x='removeActive': self.commandPath( x ) ) )
		ma.text( l=' ' )
		#ADD CURVE PATH
		self.list_disable_buttons.append( ma.nodeIconButton( l=self.label_addPath, w=self.size_UI[0] / 3.0, h=self.size_button[1] * 2.0, fn='boldLabelFont', st='textOnly', bgc=self.color_green, en=self.enableFunctions, c=lambda x='add': self.commandPath( x ) ) )
		ma.setParent( '..' )
		ma.setParent( '..' )

		#TERRAIN CONNECT#####################################################

		self.label_addTerrain = 'ADD SELECTED TERRAIN'
		self.label_removeTerrain = 'REMOVE TERRAIN'
		self.label_curvePath = 'Select a single terrain mesh for the vehicle wheels to adhere to.'

		ma.frameLayout( lv=0, mw = 6, mh = 6 )
		ma.text( l='   TERRAIN:', align='left', fn ='boldLabelFont', rs=0, h=20 )
		ma.rowColumnLayout( nc=2 )
		ma.text( l='   ' )
		ma.text( l=self.label_curvePath, h = self.size_icon )
		#keepCurvePosition button
		# ma.text( l='   ' )
		# self.list_disable_buttons.append( ma.nodeIconButton( self.button_keepPosition, l=self.label_keepPosition, w=self.size_icon * 3.5, h=self.size_icon, bgc=self.color_disable, en=self.enableFunctions, st='textOnly', c=lambda x=self.button_keepPosition, y= self.label_keepPosition : self.setToggleButton( x, y ) ) )
		# ma.text( l=' ' )
		# self.list_disable_buttons.append( ma.nodeIconButton( self.button_reverseCurve, l=self.label_reverseCurve, w=self.size_icon * 2.0, h=self.size_icon, bgc=self.color_disable, en=self.enableFunctions, st='textOnly', c=lambda x=self.button_reverseCurve, y= self.label_reverseCurve : self.setToggleButton( x, y ) ) )
		ma.setParent( '..' )
		

		#REMOVE ALL CURVE PATH
		ma.rowColumnLayout( nc=3)
		# self.list_disable_buttons.append( ma.nodeIconButton( l=self.label_addTerrain, w=self.size_UI[0] / 4.0, h=self.size_button[1] * 2.0, fn='boldLabelFont', st='textOnly', bgc=self.color_redDark, en=self.enableFunctions, c=lambda x='removeAll': self.commandPath( x ) ) )
		# ma.text( l='      ' )
		#REMOVE CURVE PATH
		self.list_disable_buttons.append( ma.nodeIconButton( l=self.label_removeTerrain, w=self.size_UI[0] / 2.1, h=self.size_button[1] * 1.5, fn='boldLabelFont', st='textOnly', bgc=self.color_redDark, en=self.enableFunctions, c=lambda x='remove': self.commandTerrain( x ) ) )
		ma.text( l=' ' )
		#ADD CURVE PATH
		self.list_disable_buttons.append( ma.nodeIconButton( l=self.label_addTerrain, w=self.size_UI[0] / 2.1, h=self.size_button[1] * 1.5, fn='boldLabelFont', st='textOnly', bgc=self.color_green, en=self.enableFunctions, c=lambda x='add': self.commandTerrain( x ) ) )
		ma.setParent( '..' )





	def close( self ):
		#close main UI
		if ma.window( self.name_tool, q=1, ex=1 ):
			ma.deleteUI( self.name_tool )


	def updateActiveRigLayout( self, fromSelection = True ):
		rootCtrl, topNode, trueSelection = None, None, []
		
		if fromSelection == True:
			trueSelection = ma.ls( sl=1 )
			topNode, rootCtrl, meshList, curveList, edgeLoop, grpList, subGrpList = self.getSelection()
		
		if topNode != None:
			activeRig = self.setActiveRig( topNode )
		
		elif rootCtrl != None:
			activeRig = self.setActiveRig( rootCtrl )

		else: #allow update from any control of initial selection
			
			if len( trueSelection ) == 1 and ma.nodeType( getShape( trueSelection[0] ) ) == 'nurbsCurve' :
					activeRig = self.setActiveRig( trueSelection[0] )
			else:
				if len( trueSelection ) == 0:
					activeRig = self.setActiveRig( None )
				else:
					activeRig = None
					cmdWarn( dict_help.get( 'warning' ).get( 'selectControl' ) )

		if activeRig == True:
			self.enableFunctions = True
			self.label_activeRig = self.activeRig

		else:
			self.enableFunctions = False
			self.label_activeRig = self.label_setActiveRig
			#disable UI if none or multiple rigs found scene
			if activeRig == None:
				cmdWarn( dict_help.get( 'warning' ).get( 'noRig' ) )
		
			if activeRig == False:
				cmdWarn( dict_help.get( 'warning' ).get( 'multiRig' ) )

		for button in self.list_disable_buttons:
			ma.nodeIconButton( button, e=1, en=self.enableFunctions )

		if self.enableFunctions == True:
			ma.nodeIconButton( self.button_connectionRemove, e=1, i=self.icon_remove )
		else:
			ma.nodeIconButton( self.button_connectionRemove, e=1, i=self.icon_removeOff )

		ma.nodeIconButton( self.button_activeRig, e=1, l=self.label_activeRig )


	def getConnectionType( self ):
		return ma.nodeIconButton( self.button_connectionType, q=1, l=1 )


	def connectionTypeToggle( self, setType = None, initialize = False ):
		if setType == None:
			currentIndex = self.list_connectToggle.index( self.getConnectionType() )
			newIndex = 0 if currentIndex >= len( self.list_connectToggle ) - 1 else currentIndex + 1
			setType = self.list_connectToggle[ newIndex ]
		connectDict = self.dict_connect.get( setType )
		ma.nodeIconButton( self.button_connectionType, e=1, bgc=connectDict.get( 'color' ), l= setType )
		ma.text( self.text_connectionType, e=1, l=connectDict.get( 'label' ) )
		for button in self.list_tagID_buttons:
			ma.nodeIconButton( button, e=1, bgc=connectDict.get( 'color' ) )
		#disable tire in parent/constraint modes
		if initialize == False:
			if setType != self.label_skin:
				ma.nodeIconButton( self.list_tagID_buttons[4], e=1, en=False )
			else:
				ma.nodeIconButton( self.list_tagID_buttons[4], e=1, en=True )

			if setType == self.label_parent:
				ma.nodeIconButton( self.button_parentGeo, e=1, en=False )
			else:
				ma.nodeIconButton( self.button_parentGeo, e=1, en=True )


	def getWheelCount( self ):
		return ma.nodeIconButton( self.button_wheelCount, q=1, l=1 )


	def wheelCountToggle( self, setType = None, initialize = False ):
		if setType == None:
			currentIndex = self.list_wheelCountToggle.index( self.getWheelCount() )
			newIndex = 0 if currentIndex >= len( self.list_wheelCountToggle ) - 1 else currentIndex + 1
			setType = self.list_wheelCountToggle[ newIndex ]
		wheelCountDict = self.dict_wheelCount.get( setType )
		ma.nodeIconButton( self.button_wheelCount, e=1, bgc=wheelCountDict.get( 'color' ), l= setType )
		
		if setType == self.label_4:
			#enable chassis if wheels are 4
			ma.nodeIconButton( self.button_chassisVersion, e=1, en=True )
		else:
			#disable chassis if more wheels than 4
			ma.nodeIconButton( self.button_chassisVersion, e=1, en=False )


	def getWheelSpan( self ):
		return ma.nodeIconButton( self.button_wheelSpan, q=1, l=1 )


	def wheelSpanToggle( self, setType = None, initialize = False ):
		if setType == None:
			currentIndex = self.list_wheelSpanToggle.index( self.getWheelSpan() )
			newIndex = 0 if currentIndex >= len( self.list_wheelSpanToggle ) - 1 else currentIndex + 1
			setType = self.list_wheelSpanToggle[ newIndex ]
		wheelSpanDict = self.dict_wheelSpan.get( setType )
		ma.nodeIconButton( self.button_wheelSpan, e=1, bgc=wheelSpanDict.get( 'color' ), l= setType )


	def getToggleButtonState( self, buttonName, label ):
		return True if ma.nodeIconButton( buttonName, q=1, ann=1 ) == label + ' - On' else False


	def setToggleButton( self, buttonName, label, attributeLink = None, setValue = None,  ):
		if self.getToggleButtonState( buttonName, label ) == True or setValue == False:
			ma.nodeIconButton( buttonName, e=1, bgc= self.color_disable, ann= label + ' - Off' )
			cmdPrint( label + ' off.' )
			if attributeLink != None:
				if ma.objExists( self.rootCtrl + '.' + attributeLink ):
					ma.setAttr( self.rootCtrl + '.' + attributeLink, 0 )
				if ma.objExists( self.bodyCtrl + '.' + attributeLink ):
					ma.setAttr( self.bodyCtrl + '.' + attributeLink, 0 )
		
		elif self.getToggleButtonState( buttonName, label ) == False or setValue == True:
			ma.nodeIconButton( buttonName, e=1, bgc= self.color_highlight, ann= label + ' - On' )
			cmdPrint( label + ' on.' )
			if attributeLink != None:
				if ma.objExists( self.rootCtrl + '.' + attributeLink ):
					ma.setAttr( self.rootCtrl + '.' + attributeLink, 1 )
				if ma.objExists( self.bodyCtrl + '.' + attributeLink ):
					ma.setAttr( self.bodyCtrl + '.' + attributeLink, 1 )


	def loadScene( self, method ):
		wheelCount = int( self.getWheelCount() ) 
		wheelSpan = int( self.getWheelSpan() )
		liteVersion = sfx_lite if wheelSpan == 0 else ''
		useChassis = sfx_noChassis if self.getToggleButtonState( self.button_chassisVersion, self.label_chassisVersion ) == False else ''
		
		#construct path
		if wheelCount == 4:
			if wheelSpan == 0:
				loadDir = rigFile + liteVersion + useChassis + ext_ma
			
			elif wheelSpan == 20:
				loadDir = rigFile + useChassis + ext_ma
			
			else:
				loadDir = rigFile + '_' + str( wheelSpan ) + 't' + useChassis + ext_ma

		else:
			if wheelSpan == 0:
				loadDir = truckRigFile + '_' + str( wheelCount ) + 'w' + liteVersion + sfx_noChassis + ext_ma

			elif wheelSpan == 20:
				loadDir = truckRigFile + '_' + str( wheelCount ) + 'w' + sfx_noChassis + ext_ma

			else:
				loadDir = truckRigFile + '_' + str( wheelCount ) + 'w' + '_' + str( wheelSpan ) + 't' + sfx_noChassis + ext_ma


		#uac lite only
		if not os.path.exists( loadDir ):
			cmdWarn( loadDir + ' does not exist, loading default instead.' )
			loadDir = rigFile + sfx_lite + sfx_noChassis  + ext_ma


		if os.path.exists( loadDir ):
			#namspc is built from the product abreviation and how ever nany cars are in the scene + 1
			ns = self.abrev + str( len( self.list_sceneRigs ) + 1 )
			
			if method == 'reference':
				ma.file( loadDir, r=1, op='v=0', lrd='all', uns=True, ns=ns )
				cmdPrint( dict_help.get( 'success' ).get( 'reference' ) + os.path.basename( loadDir ) )

			if method == 'import':
				ma.file( loadDir, i=1, ra=0, pr=1, type='mayaAscii', ns=ns )
				cmdPrint( dict_help.get( 'success' ).get( 'import' ) + os.path.basename( loadDir ) )
			
			if method == 'load':
				ma.file( loadDir, o=1, f=1, type='mayaAscii' )
				cmdPrint( dict_help.get( 'success' ).get( 'load' ) + os.path.basename( loadDir ) )
				
			self.updateActiveRigLayout( False )

		else:
			cmdPrint( dict_help.get( 'warning' ).get( 'load' ) + loadDir )



	def setActiveCamera( self, cam ):
		cam = cam.lower()
		ma.lookThru( getShape( cam ), ma.getPanel( wf=1 ) )
		#frame active rig
		selection = ma.ls( sl=1 )
		ma.select( self.activeRig )
		ma.viewFit()
		if selection != []:
			ma.select( selection )
		else:
			ma.select( cl=1 )
		cmdPrint( cam + ' set as active view' )


	def commandConnect( self, tagID ):
		#connect mesh piece(s) to desired rig component.
		method = self.getConnectionType()
		autoParentGeo = self.getToggleButtonState( self.button_parentGeo, self.label_parentGeo )
		removeUnusedInfluences = False #self.getToggleButtonState( self.button_unusedInfluence, self.label_unusedInfluence )
		self.attachMesh( tagID, method, None, autoParentGeo, removeUnusedInfluences )


	def commandPath( self, method = 'add' ):
		if method == 'add':
			#connect selected curve or edgeloop to rig
			self.addUserCurvePath( self.getToggleButtonState( self.button_keepPosition, self.label_keepPosition ), self.getToggleButtonState( self.button_reverseCurve, self.label_reverseCurve ) ) 
			#curve = self.addUserCurvePath( self.getToggleButtonState( self.button_keepPosition, self.label_keepPosition ), self.getToggleButtonState( self.button_reverseCurve, self.label_reverseCurve ) ) 
			# if curve != None:
			# 	#update viewport by moving curve slightly and returning it - maya 2022 has an display issue
			# 	ma.move( 0.001, 0.001, 0.001, curve, r=1 )
			# 	ma.undo()
			# 	ma.move( -0.001, -0.001, -0.001, curve, r=1 )
			# 	print( curve )
			# 	ma.select( curve )


		if method == 'removeActive':
			#remove the active curvePath from the rig
			self.removeCurvePath() 

		if method == 'removeAll':
			msg = dict_help.get( 'warning' ).get( 'removeAllPathConfirm' )
			cmdWarn( msg )
			if ma.confirmDialog( t='Confirm', m=msg, b=[ 'Yes', 'No' ], db='Yes', cb='No', ds='No' ) == 'Yes':
				#searches and remove all user curves
				self.removeAllUserCurvePaths()
			else:
				cmdWarn( dict_help.get( 'warning' ).get( 'removeAllPathCancel' ) )


	def commandTerrain( self, method = 'add' ):
		selected = ma.ls( sl=1 )
		if selected != []:
			if method == 'add':
				#connects the first selected mesh object to rig
				for n in selected:
					if ma.nodeType( getShape( n ) ) == 'mesh':
						self.addTerrain( n )
						return True

			if method == 'remove':
				#removes all selected mesh objects from rig
				for n in selected:
					if ma.nodeType( getShape( n ) ) == 'mesh':
						self.removeTerrain( n )
		else:
			cmdWarn( dict_help.get( 'warning' ).get( 'nothingSelected' ) )



	def commandWebHelp( self ):
		#loads online documentation
		ma.showHelp( webHelp, absolute=True )


	def commandResetPose( self ):
		pass
		#future update?
		# ctrlList = self.getCtrls()
		






