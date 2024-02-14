import maya.cmds as fuchsCmds

def setColorSpace(colorSpace):
    selection=fuchsCmds.ls(sl=1)
    for fileNode in selection:
        if fuchsCmds.nodeType(fileNode)=="file":
            fuchsCmds.setAttr(fileNode+".colorSpace", colorSpace, type="string")
            fuchsCmds.setAttr(fileNode+".ignoreColorSpaceFileRules", 1)
            print("Node "+fileNode+" set to "+colorSpace+".")
        else:
            print(fileNode+" is not a fileNode.")
