# P2D Merger v3 by TheFuchsen (Angel Canales)
# October 2023
# This script will help you merge multiple p2d nodes into a single one, no matter what it is controlling, no matter how many they are.
# It can control both merging and separation.
# Shipped with FuchsTools v1
# To be used ONLY with FuchsTools. Do not edit, nor share, nor redistribute.

import maya.cmds as fuchsCmds

def p2dMerger(action):
    def errorMsg(action):
        if action == "merge":
            fuchsCmds.warning("First select at least 2 \"place2dTexture\" nodes to merge.")
        elif action == "separate":
            fuchsCmds.warning("Select only 1 \"place2dTexture\" node to separate with more than 1 file connection.")
    def attrConnector(file_arg,target_arg):
        for outputAttr,inputAttr in attrDict.items():
            try:
                fuchsCmds.connectAttr(target_arg+outputAttr, file_arg+inputAttr, force=True)
            except:
                if logStatus:
                    print("Skipping ", outputAttr," for ", file_arg,".")
    print ("""
           
---------------------------
P2D Merger v3 by TheFuchsen
---------------------------
""")
    attrDict={     
    ".coverage":".coverage",
    ".mirrorU":".mirrorU",
    ".mirrorV":".mirrorV",
    ".noiseUV":".noiseUV",
    ".offset":".offset",
    ".repeatUV":".repeatUV",
    ".rotateFrame":".rotateFrame",
    ".rotateUV":".rotateUV",
    ".stagger":".stagger",
    ".translateFrame":".translateFrame",
    ".outUV":".uvCoord",
    ".outUvFilterSize":".uvFilterSize",
    ".vertexCameraOne":".vertexCameraOne",
    ".vertexUvOne":".vertexUvOne",
    ".vertexUvTwo":".vertexUvTwo",
    ".vertexUvThree":".vertexUvThree",
    ".wrapU":".wrapU",
    ".wrapV":".wrapV",
}
    selected = fuchsCmds.ls(selection=True)

    p2dNodes =[]
    fileNodes = []
    logStatus=False

    for node in selected:
        if fuchsCmds.nodeType(node) == "place2dTexture":
            p2dNodes.append(node)
    if p2dNodes:
        for node in p2dNodes:
            fileNodes.append(fuchsCmds.listConnections(node+".outUV", c=True, p=True))            
        if action == "merge":
            if len(p2dNodes) > 1:
                print ("Merging", len(p2dNodes), "place2dTexture nodes.")
                targetP2D = fuchsCmds.shadingNode("place2dTexture", asUtility=True, n="place2dTexture1")
                for masterlist in fileNodes:                   
                    for node in masterlist:
                        fileNode=node.split(".")[0]
                        if fileNode not in p2dNodes:
                            attrConnector(fileNode,targetP2D)
                for p2dNode in p2dNodes:
                    fuchsCmds.delete(p2dNode)
            else:
                errorMsg(action)
        elif action == "separate":
            if len(p2dNodes)<2:
                if len(fileNodes[0])>2:                    
                    for node in fileNodes[0]:
                        fileNode=node.split(".")[0]
                        if fileNode not in p2dNodes:
                            print("Separating ",fileNode,".")
                            targetP2D = fuchsCmds.shadingNode("place2dTexture", asUtility=True, n="place2dTexture1")
                            attrConnector(fileNode,targetP2D)
                    for p2dNode in p2dNodes:
                        fuchsCmds.delete(p2dNode)
                else:
                    errorMsg(action)
            else:
                errorMsg(action)
        else:
            if logStatus:
                fuchsCmds.warning("No action was given for P2DMerger.")
    else:
        errorMsg(action)