# from FuchsTools import targetWireframe as tarwir
# tarwir.targetWireframe("on")
# tarwir.targetWireframe("off")
# Angel Canales / @TheFuchsen oct 2023

import maya.cmds as mc

def targetWireframe(status):
    selected=mc.ls(selection=True,absoluteName=True)
    for node in selected:
        shapeNode=mc.listRelatives(node,shapes=True, fullPath=True)
        for subNode in shapeNode:
            if mc.nodeType(subNode) == "mesh":
                isIntermediate=mc.getAttr(subNode+".intermediateObject")
                if status == "on" and isIntermediate==False:
                    mc.setAttr(subNode+".overrideEnabled",1)
                    mc.setAttr(subNode+".overrideShading",0)
                    break
                if status == "off" and isIntermediate==False:
                    mc.setAttr(subNode+".overrideShading",1)
                    mc.setAttr(subNode+".overrideEnabled",0)
                    break
