# Redshift Tessellation settings for multiple objects.
# from FuchsTools import RedshiftTessellationSwitch as r3dsubD
# r3dsubD.createTesselationToggleWindow()
# Enjoy!
# Angel Canales / TheFuchsen
# Part of FuchsTools 2023


import maya.cmds as fuchsCmds

def applyTessellation(toggle, subCount, scrn_adapt, disp_enable, edge_length, smoothSubd):
    objectList = []
    selection = fuchsCmds.ls(selection=True, absoluteName=True)
    
    for obj in selection:
        if fuchsCmds.nodeType(obj) == "transform":
            objectList.append(obj)

    if subCount > 6:
        # Show warning dialog if sub_count exceeds 6
        result = fuchsCmds.confirmDialog(title="Warning", message="Subdivision count is set too high. It may slow down the process. Continue?", button=["Yes", "No"], defaultButton="Yes", cancelButton="No", dismissString="No")
        if result == "No":
            return

    if objectList:
        for obj in objectList:
            fuchsCmds.setAttr(obj + ".rsEnableSubdivision", toggle)
            fuchsCmds.setAttr(obj + ".rsScreenSpaceAdaptive", scrn_adapt)
            fuchsCmds.setAttr(obj + ".rsMinTessellationLength", edge_length)
            fuchsCmds.setAttr(obj + ".rsMaxTessellationSubdivs", subCount)
            fuchsCmds.setAttr(obj + ".rsEnableDisplacement", disp_enable)
            fuchsCmds.setAttr(obj + ".rsDoSmoothSubdivision", smoothSubd)
            

        resultText = "Enabled" if toggle else "Disabled"
        fuchsCmds.text("confirmation_text", edit=True, label=f"Tessellation settings {resultText} for selected objects.",align="center")
    else:
        fuchsCmds.text("confirmation_text", edit=True, label="Error: Select at least 1 object.", align="center")

def createTesselationToggleWindow():
    if fuchsCmds.window("tesselationToggleWin", exists=True):
        fuchsCmds.deleteUI("tesselationToggleWin", window=True)

    windowWidth = 300
    windowHeight = 200

    tesselationToggleWin = fuchsCmds.window("tesselationToggleWin", title="Tesselation Toggle", width=windowWidth, height=windowHeight, sizeable=False)

    # Set the background color of the entire window
    windowColor = [0.2, 0.2, 0.2]  # A shade of gray (R, G, B values)
    fuchsCmds.columnLayout(adjustableColumn=True, rowSpacing=10, backgroundColor=windowColor)

    fuchsCmds.text(label="Use this script to mass enable or disable tesselation for multiple objects.", align="center", wordWrap=True)

    # Subdivision Count Slider
    subdivisionSlider = fuchsCmds.intSliderGrp(label="Subdivision count:", field=True, value=2, minValue=0, maxValue=16, step=1, width=10)
    # Slider for Edge Length
    edgeLengthSlider = fuchsCmds.floatSliderGrp(label="Edge Length:", field=True, value=0, minValue=0, maxValue=32)
    fuchsCmds.setParent("..")  # Return to the main layout
    # Checkboxes for Displacement and Screen Adaptive
    checkboxesLayout = fuchsCmds.rowLayout(adjustableColumn=1,numberOfColumns=3, columnWidth=[(1, 140),(2, 140),(3, 140)], columnAttach=[(1, "both", 5), (2, "both", 5),(3, "both", 5)], columnAlign=[(1, "center"), (2, "center"),(3, "center")])
    displacementCheckbox = fuchsCmds.checkBox(label="Displacement", value=False, align="center")
    screenAdaptiveCheckbox = fuchsCmds.checkBox(label="Screen Adaptive", value=False, align="center")
    smoothSubdivisionCheckbox = fuchsCmds.checkBox(label="Smooth Subdivision", value=False, align="center")
    fuchsCmds.setParent("..")  # Return to the main layout


    # Buttons
    buttonsLayout = fuchsCmds.rowLayout(numberOfColumns=2, columnWidth=[(1, 210),(2, 210)], columnAttach=[(1, "both", 5), (2, "both", 5)], columnAlign=[(1, "center"), (2, "center")])
    fuchsCmds.button(label="Enable", command=lambda x: applyTessellation(1, fuchsCmds.intSliderGrp(subdivisionSlider, query=True, value=True), fuchsCmds.checkBox(screenAdaptiveCheckbox, query=True, value=True), fuchsCmds.checkBox(displacementCheckbox, query=True, value=True), fuchsCmds.floatSliderGrp(edgeLengthSlider, query=True, value=True),fuchsCmds.checkBox(smoothSubdivisionCheckbox, query=True, value=True)))
    fuchsCmds.button(label="Disable", command=lambda x: applyTessellation(0, fuchsCmds.intSliderGrp(subdivisionSlider, query=True, value=True), fuchsCmds.checkBox(screenAdaptiveCheckbox, query=True, value=True), fuchsCmds.checkBox(displacementCheckbox, query=True, value=True), fuchsCmds.floatSliderGrp(edgeLengthSlider, query=True, value=True),fuchsCmds.checkBox(smoothSubdivisionCheckbox, query=True, value=True)))
    fuchsCmds.setParent("..")  # Return to the main layout

    # Text for confirmation
    fuchsCmds.text("confirmation_text", label="", align="left", wordWrap=True)

    fuchsCmds.showWindow(tesselationToggleWin)

#createTesselationToggleWindow()
