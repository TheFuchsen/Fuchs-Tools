import maya.cmds as fuchsCmds

def RenderVisibility(toggle):
    selected=fuchsCmds.ls(selection=True)
    for node in selected:
        relativeList=fuchsCmds.listRelatives(node,shapes=True,fullPath=True)
        if (toggle=="off" and fuchsCmds.nodeType(relativeList[0])=="mesh") or (toggle=="off" and fuchsCmds.nodeType(relativeList[0])=="xgmSplineDescription"):
            fuchsCmds.setAttr(node+".primaryVisibility",0)
            fuchsCmds.setAttr(node+".rsEnableVisibilityOverrides", 1)
            fuchsCmds.setAttr(node+".rsPrimaryRayVisible", 0)
            print("Disabled render visibility for "+node+".")
        elif toggle=="on" and fuchsCmds.nodeType(relativeList[0])=="mesh":
            fuchsCmds.setAttr(node+".primaryVisibility",1)
            fuchsCmds.setAttr(node+".rsEnableVisibilityOverrides", 1)
            fuchsCmds.setAttr(node+".rsPrimaryRayVisible", 1)
            print("Enabled render visibility for "+node+".")
        elif toggle=="on" and fuchsCmds.nodeType(relativeList[0])=="xgmSplineDescription":
            fuchsCmds.setAttr(node+".primaryVisibility",1)
            fuchsCmds.setAttr(node+".rsEnableVisibilityOverrides", 1)
            fuchsCmds.setAttr(node+".rsPrimaryRayVisible", 1)
            print("Enabled render visibility for "+node+".")
        else:
            print(node+" is not a geometry object. Skipping")
