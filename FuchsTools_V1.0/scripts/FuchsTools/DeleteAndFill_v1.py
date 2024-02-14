import maya.cmds as fuchsCmds

def deleteAndFill():
    selection = fuchsCmds.ls(selection=True)
    selectedObjects = []
    for component in selection:
        if component.split(".")[0] not in selectedObjects:
            selectedObjects.append(component.split(".")[0])
    if selection:
        if len(selectedObjects)>1:
            fuchsCmds.warning("Only 1 object at a time.")
        elif fuchsCmds.nodeType(selection[0]) == "mesh" and len(selection)>1:
            fuchsCmds.Delete()
            fuchsCmds.select(selectedObjects)
            fuchsCmds.FillHole()
            fuchsCmds.select(selectedObjects)
            print ("Deleted and Filled.")
        else:
            fuchsCmds.warning("Select at least 2 or more faces.")
    else:
        fuchsCmds.warning("Select at least 2 or more faces.")
deleteAndFill()