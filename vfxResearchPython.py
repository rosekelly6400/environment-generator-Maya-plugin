import maya.cmds as cm
import pymel.core as cmds
import random

#globalVars
mapFile = 'b'
floorMapFile = 'f'
mapData = None
floorMapData = None
topogArray = []
presentColors = []
#array of dialogue boxes for object files
objFileDials = [None] * 100
colorObjAssociations = [None] * 100
objCoords = [None] * 100

testViewObjs = [None] * 100 
testViewSquares =  [None] * 100 
floorPlane = None
sizeFactor = 1
#array of object scale, rotation, movement randomness slider values
xVals = [None] * 3 * 100
yVals = [None] * 3 * 100
zVals = [None] * 3 * 100
rotRandVals = [None] * 100
envScaleValue = 1
envScaleSlider = None

rotVals = [0,0,0] * 100
moveVals = [0,0,0] * 100
scaleVals = [0,0,0] * 100
rotRandNumber = 0 * 100

# Make a new default window
windowID = 'myWindowID'
if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

window = cmds.window(windowID, title="Map Interpreter", iconName='Short Name', width=1, height=1 )
scrollLayout = cmds.scrollLayout(
	horizontalScrollBarThickness=16,
	verticalScrollBarThickness=16)

#Create buttons
cmds.columnLayout( adjustableColumn=True, columnAlign='center', rowSpacing=20)
cmds.rowColumnLayout( numberOfColumns=3 )

cmds.separator( style='none' )
cmds.text("Select png file to be translated to 3D:")
cmds.separator( style='none' )

ict = cmds.textFieldButtonGrp( fileName='', label='Map File:', buttonLabel='...', buttonCommand='searchForFiles()' )
flf = cmds.textFieldButtonGrp( fileName='', label='Floor Layer File:', buttonLabel='...', buttonCommand='searchForFloorFiles()')
cmds.floatSliderGrp(label="Floor Map Height Range", field=True, min=0, max=50, value=5)

cmds.separator( style='none' )

cmds.button( label='Interpret Map', command='interpretPng()' )
cmds.button( label='Interpret Floor Map', command='interpretFloorMap()' )
cmds.setParent( '..' )
cmds.showWindow( window )

#Object Map FileOpening Function
def searchForFiles():    
    singleFilter = "All Files (*.*)"
    filepath = cmds.fileDialog2(fileFilter=singleFilter, dialogStyle=2, fileMode=1, returnFilter=True)
    global mapFile
    mapFile = str(filepath[0])
    cmds.textFieldButtonGrp(ict, e=True, fileName=filepath[0])
    
#Floor Texture FileOpening Function
def searchForFloorFiles():    
    singleFilter = "All Files (*.*)"
    filepath = cmds.fileDialog2(fileFilter=singleFilter, dialogStyle=2, fileMode=1, returnFilter=True)
    global floorMapFile
    floorMapFile = str(filepath[0])
    cmds.textFieldButtonGrp(flf, e=True, fileName=filepath[0])
    
    
#FileOpening Function for objects and colors
# sets color to be associated with certain object as specified by object file dialogue of given index
def searchForObjFiles(index, r, g, b):
    global testViewObjs 
    global testViewSquares   
    global rotVals
    global moveVals
    global scaleVals
    global envScaleValue
    singleFilter = "All Files (*.*)"
    filepath = cmds.fileDialog2(fileFilter=singleFilter, dialogStyle=2, fileMode=1, returnFilter=True)
    global colorObjAssociations
    colObjPair = (r, g, b, filepath[0], False, None)
    colorObjAssociations[index] = colObjPair
    cmds.textFieldButtonGrp(objFileDials[index], e=True, fileName=filepath[0])
    
    before = set(cm.ls(assemblies=True))
    cm.file( filepath[0], i=True)
    after = set(cm.ls(assemblies=True))
    testViewObjs[index] = after.difference(before)
    
    before = set(cm.ls(assemblies=True))
    cm.polyCube() 
    after = set(cm.ls(assemblies=True))
    testViewSquares[index] = after.difference(before)
    
    
    cm.move(-envScaleValue*(index+1), 0, 0 , testViewObjs[index], ws=True, a=True)
    cm.scale(1, 1, 1, testViewObjs[index])
    
    cm.move(-envScaleValue*(index+1), -0.05 , 0 , testViewSquares[index], ws=True, a=True)
    cm.scale(envScaleValue, 0.1, envScaleValue, testViewSquares[index])



def changeEnvNum():
    global envScaleValue
    global envScaleSlider
    global testViewObjs
    global testViewSquares
    envScaleValue = cmds.floatSliderGrp(envScaleSlider, q=True, value=True)
    ind = 0
    for o in testViewObjs:
        if o != None:
            cm.move(envScaleValue*(ind+1), 0, 0 , o, ws=True, a=True)
            ind = ind + 1
    
    ind = 0
    for s in testViewSquares:
        if s != None:
            cm.move(envScaleValue*(ind+1), -0.05, 0 , s, ws=True, a=True)
            cm.scale(envScaleValue, 0.1, envScaleValue, s)
            ind = ind + 1
            
        
        
    
# sets x and y vals for objects from slider changes
def setObjXYZ(index):    
    global xVals
    global yVals
    global zVals
    global rotVals
    global moveVals
    global scaleVals
    global rotRandVals
    global testViewObjs
    global testViewSquares
    global envScaleValue
    
    scaleX = cmds.floatSliderGrp(xVals[3*index], q=True, value=True)
    rotateX = cmds.floatSliderGrp(xVals[3*index + 1], q=True, value=True)
    moveX = cmds.floatSliderGrp(xVals[3*index + 2], q=True, value=True)
    
    scaleY = cmds.floatSliderGrp(yVals[3*index], q=True, value=True)
    rotateY = cmds.floatSliderGrp(yVals[3*index + 1], q=True, value=True)
    moveY = cmds.floatSliderGrp(yVals[3*index + 2], q=True, value=True)
    
    scaleZ = cmds.floatSliderGrp(zVals[3*index], q=True, value=True)
    rotateZ = cmds.floatSliderGrp(zVals[3*index + 1], q=True, value=True)
    moveZ = cmds.floatSliderGrp(zVals[3*index + 2], q=True, value=True)
    
    scaleTriple = (scaleX, scaleY, scaleZ)
    rotateTriple = (rotateX, rotateY, rotateZ)
    moveTriple = (moveX, moveY, moveZ)
    
    rotVals[index] = rotateTriple
    moveVals[index] = moveTriple
    scaleVals[index] = scaleTriple
    
    if(testViewObjs[index-1] != None):
        cm.move(-envScaleValue*index + moveVals[index][0], 0+ moveVals[index][1], 0 + moveVals[index][2], testViewObjs[index-1], ws=True, a=True)
        cm.scale(scaleVals[index][0], scaleVals[index][1], scaleVals[index][2], testViewObjs[index-1], a=True)
        cm.rotate(0 + rotVals[index][0], 0 + rotVals[index][1], 0 + rotVals[index][2], testViewObjs[index-1],  a=True)


#Png Interpretation Function
def interpretPng():
    global presentColors 
    global objFileDials
    global envScaleSlider
    global mapData
    global mapFile
    global xVals
    global yVals
    global zVals
    global rotRandVals
    
    frsult = cmds.interpretMap(mapFile)
    mapData = frsult
    x = frsult[0]
    y = frsult[1]
    size = x*y
    #CHANGE AFTER RELOADING TO 3
    i = 3
    col = 0
    row = 0
    while (i + 3) < len(frsult):
        if col == x:
            col = 0
            row = row + 1
        found = False
        for c in presentColors:
            if (frsult[i] == c[0]) and (frsult[i+1] == c[1]) and (frsult[i+2] == c[2]):
                found = True
        if found == False:
            newColor = (frsult[i], frsult[i+1], frsult[i+2])
            presentColors.insert(0, newColor)
        
        col = col + 1
        i = i + 4 

    envScaleSlider = cmds.floatSliderGrp(label="Global Scale", field=True, min=0, max=10, value=1, changeCommand='changeEnvNum()')
    
    cmds.text("Select obj file to be associated with pixel location of below colors")
    cmds.rowColumnLayout( numberOfColumns=3 )
    k = 0
    for dC in presentColors:
        #1 COL LAYOUT
        #cmds.rowColumnLayout( numberOfColumns=1 )
        cmds.separator( style='none' )
        cmds.button(' ', enable=False, backgroundColor=(dC[0]/255, dC[1]/255, dC[2]/255))
        bcString = 'searchForObjFiles(' + str(k) + ', ' + str(dC[0]) + ', ' + str(dC[1]) + ', ' + str(dC[2]) + ')'
        
        cmds.separator( style='none' )
        cmds.separator( style='none' )
        objFileDials[k] = cmds.textFieldButtonGrp( fileName='', label='Object File:', buttonLabel='...', buttonCommand=bcString )
        cmds.separator( style='none' )
        k = k + 1
        #3 COL LAYOUT
        #cmds.rowColumnLayout( numberOfColumns=3 )
        fsgString = 'setObjXYZ(' + str(k) + ')'
        
        
        xVals[3*k] = cmds.floatSliderGrp(label="Scale X ", field=True, min=0, max=5, value=1, changeCommand=fsgString) 
        yVals[3*k] = cmds.floatSliderGrp(label="Scale Y ", field=True, min=0, max=5, value=1, changeCommand=fsgString)
        zVals[3*k] = cmds.floatSliderGrp(label="Scale Z ", field=True, min=0, max=5, value=1, changeCommand=fsgString)
        
        xVals[3*k + 1] = cmds.floatSliderGrp(label="Rotate X ", field=True, min=-180, max=180, value=0,  changeCommand=fsgString)
        yVals[3*k + 1] = cmds.floatSliderGrp(label="Rotate Y ", field=True, min=-180, max=180, value=0, changeCommand=fsgString)
        zVals[3*k + 1] = cmds.floatSliderGrp(label="Rotate Z ", field=True, min=-180, max=180, value=0, changeCommand=fsgString)
        
        xVals[3*k+2] = cmds.floatSliderGrp(label="Move X ", field=True, min=-0.5, max=0.5, value=0,  changeCommand=fsgString)
        yVals[3*k+2] = cmds.floatSliderGrp(label="Move Y ", field=True, min=-5, max=5, value=0, changeCommand=fsgString)
        zVals[3*k+2] = cmds.floatSliderGrp(label="Move Z ", field=True, min=-0.5, max=0.5, value=0, changeCommand=fsgString)
        
        cmds.separator( style='none' )
        rotRandVals[k] = cmds.floatSliderGrp(label=" Rotational Rand Range", field=True, min=1, max=180, value=0)
        cmds.separator( style='none' )
        
        
        cmds.separator( height=20, style='double' )
        cmds.separator( height=20, style='double' )
        cmds.separator( height=20, style='double' )
        setObjXYZ(k)
    cmds.separator( style='none' )
    cmds.button( label='Create 3D Environment', command='placeObjects()' )
    cmds.showWindow( window )
    #cmds.deleteUI(window, window=True)
    
#Object Placing Function
def placeObjects():
    global colorObjAssociations 
    global mapData
    global floorMapData
    global testViewObjs
    global testViewSquares
    global sizeFactor
    global floorPlane
    global topogArray
    
    global rotVals
    global moveVals
    global scaleVals
    global rotRandVals
    global envScaleValue
    
    for o in testViewObjs:
        cm.delete(o)
        
    for s in testViewSquares:
        cm.delete(s)
    
    x = mapData[0]
    y = mapData[1]
    size = x*y
    
    
    i = 3
    col = 0
    row = 0
    while (i + 3) < len(mapData):
        if col == x:
            col = 0
            row = row + 1
        found = False
        colorObjIndex = 0
        for c in colorObjAssociations:
            if c != None:
                if (mapData[i] == c[0]) and (mapData[i+1] == c[1]) and (mapData[i+2] == c[2]):
                    if(c[3]):
                        if c[4] == False:
                            before = set(cm.ls(assemblies=True))
                            cm.file(c[3], i=True)
                            after = set(cm.ls(assemblies=True))
                            selectedObj = after.difference(before)
                            newColObjPair = (c[0], c[1], c[2], c[3], True, selectedObj)
                            #print(colorObjAssociations)
                            colorObjAssociations[colorObjIndex] = newColObjPair
                            #print(colorObjAssociations)
                        else:
                            #print(c)
                            #print(c[5])
                            before = set(cm.ls(assemblies=True))
                            cm.duplicate(c[5])
                            after = set(cm.ls(assemblies=True))
                            selectedObj = after.difference(before)
                        
                        #bitmap floor value
                        #singlePointIndex = int((1/sizeFactor) * x * (1/sizeFactor) * y) - 1 - int((1/sizeFactor) * row) - int((1/sizeFactor) * col * x)
                        singlePointIndex = (int((1/sizeFactor) * (x-row -1) * x * int((1/sizeFactor))) + (1/sizeFactor) * col + 1)
                        spValue = 0
                        if topogArray != None and len(topogArray) > int(singlePointIndex):
                            #print(topogArray)
                            spValue = topogArray[int(singlePointIndex)]

                        cm.move(col*envScaleValue + moveVals[colorObjIndex+1][0] + 0.5, 0+ moveVals[colorObjIndex+1][1] + 6.0*spValue, row*envScaleValue + moveVals[colorObjIndex+1][2]+1, selectedObj, ws=True)
                        cm.scale(scaleVals[colorObjIndex+1][0], scaleVals[colorObjIndex+1][1], scaleVals[colorObjIndex+1][2], selectedObj)

                        cm.rotate(0 + rotVals[colorObjIndex+1][0], 0 + rotVals[colorObjIndex+1][1], 0 + rotVals[colorObjIndex+1][2], selectedObj)

                    found = True

            colorObjIndex = colorObjIndex + 1
        col = col + 1
        i = i + 4
    
def createObj(x, y, z):
    cmds.polyCube( name = 'cube' )   
    cmds.move( x, y, z )
    
    
#Png Interpretation Function
def interpretFloorMap():
    global floorMapData
    global floorMapFile
    global floorPlane
    global sizeFactor
    global topogArray
    
    global mapData
    
    flrsult = cmds.interpretMap(floorMapFile)
    floorMapData = flrsult
    x = flrsult[0]
    y = flrsult[1]
    
    sizeFactor = x
    
    size = x*y
    #size of plane is dependant on obj png map, location also needs to change dependant on other map
    
    before = set(cm.ls(assemblies=True))
    cmds.polyPlane( sx=x, sy=y, w=x, h=y)
    after = set(cm.ls(assemblies=True))
    floorPlane = after.difference(before)
    
    mapX = floorMapData[0]
    
    sizeFactor = mapX / sizeFactor
    cm.move(mapX/2.0, 0, mapX/2.0, floorPlane, ws=True, a=True)
    cm.scale(sizeFactor, 0, sizeFactor, floorPlane)
    
    topoLvls = []
    frp = flrsult[3] / 255.0
    fgp = flrsult[3 + 1] / 255.0
    fbp = flrsult[3 + 2] / 255.0
    fvalue = max([frp, fgp, fbp])
    firstColor = fvalue
    topoLvls.insert(0, [firstColor, 3])
    
    firstFace = True
    
    #CHANGE AFTER RELOADING TO 3
    i = 3
    faceIndex = 0
    tileNum = (len(flrsult)-3) / 4
    col = 0
    row = 0
    while (i + 3) < len(flrsult):
        if col == x:
            col = 0
            row = row + 1
        rp = flrsult[i] / 255.0
        gp = flrsult[i + 1] / 255.0
        bp = flrsult[i + 2] / 255.0
        value = max([rp, gp, bp])
        faceIndexInverse = int(tileNum) - 1 - faceIndex
        topogArray.insert(0, value)
        if value == firstColor:
            currFace = 'pPlane1.f[' + str(faceIndexInverse) + ']'
            if firstFace == True:
                cmds.select(currFace)
                firstFace = False
            else:
                cmds.select(currFace, add = True)
        else:
            alreadyFound=False
            for t in topoLvls:
                if(t[0] == value):
                    alreadyFound=True
            if alreadyFound==False:
                topoLvls.insert(0, [value, i])
        
        col = col + 1
        i = i + 4
        faceIndex = faceIndex + 1
    cmds.move(0, (6*firstColor), 0, relative=True)
    
    
    for t in topoLvls:
        firstFace = True
        if t[0] != firstColor:
            i = 3
            faceIndex = 0
            tileNum = (len(flrsult)-3) / 4
            col = 0
            row = 0
            while (i + 3) < len(flrsult):
                if col == x:
                    col = 0
                    row = row + 1
                rp = flrsult[i] / 255.0
                gp = flrsult[i + 1] / 255.0
                bp = flrsult[i + 2] / 255.0
                value = max([rp, gp, bp])
                faceIndexInverse = int(tileNum) - 1 - faceIndex
                if value == t[0]:
                    currFace = 'pPlane1.f[' + str(faceIndexInverse) + ']'
                    if firstFace == True:
                        cmds.select(currFace)
                        firstFace = False
                    else:
                        cmds.select(currFace, add = True)
                col = col + 1
                i = i + 4
                faceIndex = faceIndex + 1
            cmds.move(0, 6*(t[0]), 0, relative=True)
    
    
