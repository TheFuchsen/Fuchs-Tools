# Make Me Random! v1
# Translate randomizer for Maya!

# Select your objects move the sliders!

# Instalation:

# import MakeMeRandom_v2 as fuchsMMR
# fuchsMMR.summonMakeMeRandom()

# @TheFuchsen
# https://github.com/TheFuchsen/Fuchs-Tools/

# Changelog for MMS V3:
# - Revamped! MakeMeSpin is now MakeMeRandom!
# - Added sliders for real time feedback. 
# - Added NakeMeMove: Positional Randomizer.
# - Object aware (This took both my sleep and hair away).

import maya.cmds as fuchsCmds
import random

originalRotations = {}
randomizedRotations = {}
originalTranslations = {}
randomizedTranslations = {}
originalScales = {}
randomizedScales = {}
mmrCleanupList=[]
objectsForMMR = []

def mmrHouseCleaning(*args):
    fuchsCmds.deleteUI("mmmWindow", window=True)
    originalRotations.clear()
    originalTranslations.clear()
    originalScales.clear()
    randomizedRotations.clear()
    randomizedTranslations.clear()
    randomizedScales.clear()
    objectsForMMR.clear()
    mmrCleanupList.clear()

def makeMeSpin(*args):
    if not objectsForMMR:
        fuchsCmds.warning("Select at least 1 object")
        return

    for obj in objectsForMMR:
        xRot, yRot, zRot = fuchsCmds.getAttr(obj + ".rotate")[0]

        # Store original rotation values for each object if not already stored
        if obj not in originalRotations:
            originalRotations[obj] = (xRot, yRot, zRot)

        xRot = random.uniform(-1, 1)
        yRot = random.uniform(-1, 1)
        zRot = random.uniform(-1, 1)

        # Store randomized rotation values for each object
        randomizedRotations[obj] = (xRot, yRot, zRot)

    # Update the rotations immediately after randomization
    updateRotation()

def makeMeMove(*args):


    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            xTrans, yTrans, zTrans = fuchsCmds.getAttr(obj + ".translate")[0]

            # Store original translation values for each object if not already stored
            if obj not in originalTranslations:
                originalTranslations[obj] = (xTrans, yTrans, zTrans)

            xTrans = random.uniform(-1, 1)
            yTrans = random.uniform(-1, 1)
            zTrans = random.uniform(-1, 1)

            # Store randomized translation values for each object
            randomizedTranslations[obj] = (xTrans, yTrans, zTrans)

    # Update the translations immediately after randomization
    updateTranslation()

def makeMeMorph(*args):

    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            xScale, yScale, zScale = fuchsCmds.getAttr(obj + ".scale")[0]

            # Store original scale values for each object if not already stored
            if obj not in originalScales:
                originalScales[obj] = (xScale, yScale, zScale)

            xScale = random.uniform(-1, 1)
            yScale = random.uniform(-1, 1)
            zScale = random.uniform(-1, 1)

            # Store randomized translation values for each object
            randomizedScales[obj] = (xScale, yScale, zScale)

    # Update the translations immediately after randomization
    updateScale()

def updateRotation(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=True)
    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalRotations.get(obj, (0, 0, 0))
            randRotX, randRotY, randRotZ = randomizedRotations.get(obj, (0, 0, 0))

            RotFactorX = fuchsCmds.floatSliderGrp(xRotSlider, query=True, value=True)
            RotFactorY = fuchsCmds.floatSliderGrp(yRotSlider, query=True, value=True)
            RotFactorZ = fuchsCmds.floatSliderGrp(zRotSlider, query=True, value=True)

            newXRot = origX + (RotFactorX*randRotX)
            newYRot = origY + (RotFactorY*randRotY)
            newZRot = origZ + (RotFactorZ*randRotZ)

            fuchsCmds.setAttr(obj + ".rotateX", newXRot)
            fuchsCmds.setAttr(obj + ".rotateY", newYRot)
            fuchsCmds.setAttr(obj + ".rotateZ", newZRot)

def updateTranslation(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=True)
    xRange = fuchsCmds.floatSliderGrp(xTransSlider, query=True, value=True)
    yRange = fuchsCmds.floatSliderGrp(yTransSlider, query=True, value=True)
    zRange = fuchsCmds.floatSliderGrp(zTransSlider, query=True, value=True)

    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalTranslations.get(obj, (0, 0, 0))
            randTransX, randTransY, randTransZ = randomizedTranslations.get(obj, (0, 0, 0))

            newXTrans = origX + (xRange*randTransX)
            newYTrans = origY + (yRange*randTransY)
            newZTrans = origZ + (zRange*randTransZ)

            fuchsCmds.setAttr(obj + ".translateX", newXTrans)
            fuchsCmds.setAttr(obj + ".translateY", newYTrans)
            fuchsCmds.setAttr(obj + ".translateZ", newZTrans)

def updateScale(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=True)
    xRange = fuchsCmds.floatSliderGrp(xScaleSlider, query=True, value=True)
    yRange = fuchsCmds.floatSliderGrp(yScaleSlider, query=True, value=True)
    zRange = fuchsCmds.floatSliderGrp(zScaleSlider, query=True, value=True)

    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalScales.get(obj, (0, 0, 0))
            randScaleX, randScaleY, randScaleZ = randomizedScales.get(obj, (0, 0, 0))

            newXScale = origX + (xRange*randScaleX)
            newYScale = origY + (yRange*randScaleY)
            newZScale = origZ + (zRange*randScaleZ)

            fuchsCmds.setAttr(obj + ".scaleX", newXScale)
            fuchsCmds.setAttr(obj + ".scaleY", newYScale)
            fuchsCmds.setAttr(obj + ".scaleZ", newZScale)

def cancelMMR(*args):
    
    for obj in objectsForMMR:
        if fuchsCmds.objExists(obj):
            mmrCleanupList.append(obj)
    if mmrCleanupList:
        for obj in mmrCleanupList:
            xTrans, yTrans, zTrans = originalTranslations[obj]
            xRot, yRot, zRot = originalRotations[obj]
            xScal, yScal, zScal = originalScales[obj]
            fuchsCmds.setAttr(obj + ".translateX", xTrans)
            fuchsCmds.setAttr(obj + ".translateY", yTrans)
            fuchsCmds.setAttr(obj + ".translateZ", zTrans)
            fuchsCmds.setAttr(obj + ".rotateX", xRot)
            fuchsCmds.setAttr(obj + ".rotateY", yRot)
            fuchsCmds.setAttr(obj + ".rotateZ", zRot)
            fuchsCmds.setAttr(obj + ".scaleX", xScal)
            fuchsCmds.setAttr(obj + ".scaleY", yScal)
            fuchsCmds.setAttr(obj + ".scaleZ", zScal)
    mmrHouseCleaning()

def updateXR(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalRotations.get(obj, (0, 0, 0))
            randRotX, randRotY, randRotZ = randomizedRotations.get(obj, (0, 0, 0))
            RotFactorX = fuchsCmds.floatSliderGrp(xRotSlider, query=True, value=True)
            newXRot = origX + (RotFactorX*randRotX)
            fuchsCmds.setAttr(obj + ".rotateX", newXRot)
def updateYR(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalRotations.get(obj, (0, 0, 0))
            randRotX, randRotY, randRotZ = randomizedRotations.get(obj, (0, 0, 0))
            RotFactorY = fuchsCmds.floatSliderGrp(yRotSlider, query=True, value=True)
            newYRot = origY + (RotFactorY*randRotY)
            fuchsCmds.setAttr(obj + ".rotateY", newYRot)
def updateZR(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalRotations.get(obj, (0, 0, 0))
            randRotX, randRotY, randRotZ = randomizedRotations.get(obj, (0, 0, 0))
            RotFactorZ = fuchsCmds.floatSliderGrp(zRotSlider, query=True, value=True)
            newZRot = origZ + (RotFactorZ*randRotZ)
            fuchsCmds.setAttr(obj + ".rotateZ", newZRot)

def updateXT(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    xRange = fuchsCmds.floatSliderGrp(xTransSlider, query=True, value=True)
    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalTranslations.get(obj, (0, 0, 0))
            randTransX, randTransY, randTransZ = randomizedTranslations.get(obj, (0, 0, 0))
            newXTrans = origX + (xRange*randTransX)
            fuchsCmds.setAttr(obj + ".translateX", newXTrans)
def updateYT(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    yRange = fuchsCmds.floatSliderGrp(yTransSlider, query=True, value=True)
    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:    
            origX, origY, origZ = originalTranslations.get(obj, (0, 0, 0))
            randTransY, randTransY, randTransZ = randomizedTranslations.get(obj, (0, 0, 0))
            newYTrans = origY + (yRange*randTransY)
            fuchsCmds.setAttr(obj + ".translateY", newYTrans)
def updateZT(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    zRange = fuchsCmds.floatSliderGrp(zTransSlider, query=True, value=True)
    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalTranslations.get(obj, (0, 0, 0))
            randTransZ, randTransY, randTransZ = randomizedTranslations.get(obj, (0, 0, 0))
            newZTrans = origZ + (zRange*randTransZ)
            fuchsCmds.setAttr(obj + ".translateZ", newZTrans)

def updateXS(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    xRange = fuchsCmds.floatSliderGrp(xScaleSlider, query=True, value=True)

    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalScales.get(obj, (0, 0, 0))
            randScaleX, randScaleY, randScaleZ = randomizedScales.get(obj, (0, 0, 0))

            newXScale = origX + (xRange*randScaleX)

            fuchsCmds.setAttr(obj + ".scaleX", newXScale)
def updateYS(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    yRange = fuchsCmds.floatSliderGrp(yScaleSlider, query=True, value=True)

    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalScales.get(obj, (0, 0, 0))
            randScaleX, randScaleY, randScaleZ = randomizedScales.get(obj, (0, 0, 0))
            newYScale = origY + (yRange*randScaleY)
            fuchsCmds.setAttr(obj + ".scaleY", newYScale)
def updateZS(*args):
    fuchsCmds.undoInfo(stateWithoutFlush=False)
    zRange = fuchsCmds.floatSliderGrp(zScaleSlider, query=True, value=True)

    for obj in objectsForMMR:
        if not fuchsCmds.objExists(obj):
            objectsForMMR.remove(obj)
            print(obj, " not found. Removing from list.")
        else:
            origX, origY, origZ = originalScales.get(obj, (0, 0, 0))
            randScaleX, randScaleY, randScaleZ = randomizedScales.get(obj, (0, 0, 0))
            newZScale = origZ + (zRange*randScaleZ)

            fuchsCmds.setAttr(obj + ".scaleZ", newZScale)

def summonMakeMeRandom():
    global objectsForMMR
    selection = fuchsCmds.ls(selection=True)
    for obj in selection:
        if fuchsCmds.nodeType(obj) == "transform":
            objectsForMMR.append(obj)

    if objectsForMMR:

        fuchsCmds.select(None)
        if fuchsCmds.window("mmmWindow", exists=True):
            fuchsCmds.deleteUI("mmmWindow", window=True)

        mmrWindow = fuchsCmds.window("mmmWindow", title="Make Me Random!", widthHeight=(300, 640), sizeable=False, titleBarMenu=False)
        fuchsCmds.columnLayout(adjustableColumn=True, backgroundColor=[0.2, 0.2, 0.2], rowSpacing=10)

        # Add sliders for X, Y, and Z axes with higher precision (3 decimal places)
        fuchsCmds.text(label="Make Me Slide!", align="center", wordWrap=True, height=20, backgroundColor=(0.1,0.1,0.1), font="boldLabelFont")

        # Add sliders for translation range (default range is 10)
        global xTransSlider, yTransSlider, zTransSlider
        xTransSlider = fuchsCmds.floatSliderGrp(label="X", field=True, minValue=0, maxValue=10,fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateTranslation, dragCommand=updateXT, precision=3)
        yTransSlider = fuchsCmds.floatSliderGrp(label="Y", field=True, minValue=0, maxValue=10,fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateTranslation, dragCommand=updateYT, precision=3)
        zTransSlider = fuchsCmds.floatSliderGrp(label="Z", field=True, minValue=0, maxValue=10,fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateTranslation, dragCommand=updateZT, precision=3)

        # Add sliders for X, Y, and Z axes with higher precision (3 decimal places)
        fuchsCmds.text(label="Make Me Spin!", align="center", wordWrap=True, backgroundColor=(0.1,0.1,0.1), font="boldLabelFont")
        global xRotSlider, yRotSlider, zRotSlider
        xRotSlider = fuchsCmds.floatSliderGrp(label="X", field=True, minValue=0, maxValue=360, fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateRotation, dragCommand=updateXR, precision=3)
        yRotSlider = fuchsCmds.floatSliderGrp(label="Y", field=True, minValue=0, maxValue=360, fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateRotation, dragCommand=updateYR, precision=3)
        zRotSlider = fuchsCmds.floatSliderGrp(label="Z", field=True, minValue=0, maxValue=360, fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateRotation, dragCommand=updateZR, precision=3)

        # Add sliders for X, Y, and Z axes with higher precision (3 decimal places)
        fuchsCmds.text(label="Make Me Morph!", align="center", wordWrap=True, backgroundColor=(0.1,0.1,0.1), font="boldLabelFont")
        global xScaleSlider, yScaleSlider, zScaleSlider
        xScaleSlider = fuchsCmds.floatSliderGrp(label="X", field=True, minValue=0, maxValue=10, fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateScale, dragCommand=updateXS, precision=3)
        yScaleSlider = fuchsCmds.floatSliderGrp(label="Y", field=True, minValue=0, maxValue=10, fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateScale, dragCommand=updateYS, precision=3)
        zScaleSlider = fuchsCmds.floatSliderGrp(label="Z", field=True, minValue=0, maxValue=10, fieldMaxValue=10000,value=0, width=250, columnWidth3=(30, 100, 150), changeCommand=updateScale, dragCommand=updateZS, precision=3)
        # Add the "Randomize" button
        fuchsCmds.button(label="Randomize Slide", width=150, height=40, command=makeMeMove)
        # Add the "Randomize" button
        fuchsCmds.button(label="Randomize Spin", width=150, height=40, command=makeMeSpin)
        # Add the "Randomize" button
        fuchsCmds.button(label="Randomize Morph", width=150, height=40, command=makeMeMorph)

        # Add "Apply" and "Cancel" buttons
        fuchsCmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150))
        fuchsCmds.button(label="Apply", width=150, height=40, command=mmrHouseCleaning)
        fuchsCmds.button(label="Cancel", width=150, height=40, command=cancelMMR)
        fuchsCmds.setParent('..')

        # Add text to display the list of objects affected by the random translation
        fuchsCmds.text(label="Affected Objects:", align="left")
        affected_objects_text = fuchsCmds.text(label="", align="left", wordWrap=True)

        # Update the text with the list of selected objects (show the first 10 objects and count of remaining)
        max_display_objects = 10
        affected_objects_text_label = ", ".join(objectsForMMR[:max_display_objects])
        if len(objectsForMMR) > max_display_objects:
            remaining_objects_count = len(objectsForMMR) - max_display_objects
            affected_objects_text_label += ", ... (+{})".format(remaining_objects_count)
        fuchsCmds.text(affected_objects_text, edit=True, label=affected_objects_text_label)

        fuchsCmds.showWindow(mmrWindow)
        makeMeSpin()
        makeMeMove()
        makeMeMorph()
    else:
        fuchsCmds.warning("Select at least 1 object")

summonMakeMeRandom()