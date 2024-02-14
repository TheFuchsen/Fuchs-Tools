#Fuchs Shader Helper v0.1

import maya.cmds as mc

def materialSetManager(Shader):
    mtlList=[]

    if Shader==None:
        mtlList=mc.ls(sl=1)
    else:
        mtlList.append(Shader)
        print(mtlList)
    if mtlList:
        for mtlNode in mtlList:
            if mc.nodeType(mtlNode) == "RedshiftStandardMaterial":
                try:
                    mc.sets(mtlNode,add="MaterialSet")
                except:
                    mc.sets(mtlNode,name="MaterialSet")
            elif mc.nodeType(mtlNode) == "RedshiftHair":
                try:
                    mc.sets(mtlNode,add="HairMaterialSet")
                except:
                    mc.sets(mtlNode,name="HairMaterialSet")
            else:
                mc.warning("Selected node is not a Redshift type material.")
    else:
        mc.warning("Nothing was given.")

def rsHairHelper():

    rsHairMtl=[]
    igsDesc=[]
    selected=mc.ls(sl=1)
    if selected:
        for node in selected:
            if mc.nodeType(node) == "RedshiftHair":
                rsHairMtl.append(node)
            elif mc.nodeType(mc.listRelatives(node,shapes=True,children=True,fullPath=True))=="xgmSplineDescription":
                igsDesc.append(node)
            else:
                mc.warning(node+" was not identifyed.")

    if igsDesc:
        mtlNode=None
        relatives=mc.listRelatives(igsDesc[0],shapes=True,children=True,fullPath=True)      
        hostSG=(mc.listConnections(relatives[0], type='shadingEngine'))
        if rsHairMtl:
            mtlNode=rsHairMtl[0]
            hostSG=mc.listConnections(mtlNode,type="shadingEngine")
            for node in igsDesc:
                print(node)
                print(hostSG)
                mc.sets(node, edit=True, forceElement=hostSG[0])
        else:
            if len(igsDesc)>1:
                mc.warning("Select only 1 IGS description for slave material creation.")
                return
            mtlNode=mc.shadingNode("RedshiftHair", asShader=True, name="RedshiftHair_MTL")
            materialSetManager(mtlNode)
            mc.connectAttr(mtlNode+".outColor", hostSG[0]+".rsSurfaceShader",f=1)

            materialSetManager(mtlNode)
        print("Updated "+hostSG[0]+".")
            
    else:
        mc.warning("Select at least 1 Xgen IGS description.")

def rsSlaveMaterial():
    
    rsStandardMaterial=[]
    meshObj=[]
    SGNode=False
    selected=mc.ls(sl=1)
    if selected:
        for node in selected:
            if mc.nodeType(node) == "RedshiftStandardMaterial":
                rsStandardMaterial.append(node)
            elif mc.nodeType(mc.listRelatives(node,shapes=True,children=True,fullPath=True))=="mesh":
                meshObj.append(node)
            elif mc.nodeType(node) == "shadingEngine":
                meshObj.append(node)
                SGNode=True
            else:
                mc.warning(node+" was not identifyed.")

    if meshObj:
        mtlNode=None
        if SGNode:
            hostSG=meshObj
        else:
            relatives=mc.listRelatives(meshObj[0],shapes=True,children=True,fullPath=True)      
            hostSG=(mc.listConnections(relatives[0], type='shadingEngine'))
        if rsStandardMaterial:
            mtlNode=rsStandardMaterial[0]
            hostSG=mc.listConnections(mtlNode,type="shadingEngine")
            for node in meshObj:
                print(node)
                print(hostSG)
                mc.sets(node, edit=True, forceElement=hostSG[0])
        else:
            if len(meshObj)>1:
                mc.warning("Select only 1 mesh object for slave material creation.")
                return
            mtlNode=mc.shadingNode("RedshiftStandardMaterial", asShader=True, name="RedshiftStandardMaterial_RSMTL")
            materialSetManager(mtlNode)
            mc.connectAttr(mtlNode+".outColor", hostSG[0]+".rsSurfaceShader",f=1)

            materialSetManager(mtlNode)
        print("Updated "+hostSG[0]+".")
            
    else:
        mc.warning("Select at least 1 mesh object description.")