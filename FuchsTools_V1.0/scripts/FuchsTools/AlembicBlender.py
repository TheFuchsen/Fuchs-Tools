import maya.cmds as fuchsCmds



def alembicBlender():

    def AlembicBlenderDisplay(success):
        if success:
            fuchsCmds.inViewMessage( amg='Built <hl>Alembic BlendShapes</hl>.', pos='midCenter', fade=True )
        else:
            fuchsCmds.inViewMessage( amg='<hl>"No blandShapes were built."</hl>', pos='midCenter', fade=True )

    def blendshapeCreator():
        success=False
        for sObj in sourceList:
            sName=sObj.split("|")[-1].split(":")[-1]
            sPCount=fuchsCmds.polyEvaluate(sObj,v=1)
            tinder=False
            for tObj in targetList:
                tName=tObj.split("|")[-1].split(":")[-1]
                tPCount=fuchsCmds.polyEvaluate(tObj,v=1)
                if tName == sName:
                    if tPCount == sPCount:
                        try:
                            fuchsCmds.setAttr(sObj+".visibility", 0)
                        except:
                            fuchsCmds.warning(sObj+" visibility is locked and cannot be modified." )
                        fuchsCmds.refresh()
                        blendShapeName=tName+"_blendShape"
                        tempBlendshape=fuchsCmds.blendShape(sObj,tObj,name=blendShapeName)
                        blendShapesList.append(tempBlendshape[0])
                        nameAppend.append(sName)
                        fuchsCmds.setAttr(tempBlendshape[0]+"."+tName,0.25)
                        fuchsCmds.refresh()
                        fuchsCmds.setAttr(tempBlendshape[0]+"."+tName,0.5)
                        fuchsCmds.refresh()
                        fuchsCmds.setAttr(tempBlendshape[0]+"."+tName,0.75)
                        fuchsCmds.refresh()
                        fuchsCmds.setAttr(tempBlendshape[0]+"."+tName,1)
                        fuchsCmds.setAttr(tempBlendshape[0]+".origin",0)
                        tinder=True
                        break
                    else:
                        fuchsCmds.warning("Polycount between "+sObj+" and "+tObj+" do not match. Aborting")
                        return
                    fuchsCmds.refresh()
            if tinder == False:
                fuchsCmds.warning("No object matches "+sObj+".")
            
        if blendShapesList:
            print("Successfull blendShapes:", blendShapesList)
            fuchsCmds.select(blendShapesList)
            fuchsCmds.sets(blendShapesList,name="AlembicBlendShapes1")
            success=True
        else:
            fuchsCmds.warning("No blandShapes were built.")
        return success
    
    selected=fuchsCmds.ls(selection=True)
    sourceGroup=None
    sourceList=[]
    targetList=[]
    blendShapesList=[]
    nameAppend=[]
    success=False

    if len(selected) == 2:
        for grp in selected:
            if grp.lower() == "source":
                print("Filtering source")
                sourceList=fuchsCmds.listRelatives(grp, children=True,fullPath=True)
                print(sourceList)
            elif grp.lower() ==  "target":
                print("Filtering target")
                targetList=fuchsCmds.listRelatives(grp, children=True,fullPath=True)
                print(targetList)
            else:
                fuchsCmds.warning("At least one of your elements was not detected")
                return
    else:
        fuchsCmds.warning("Select Source and Target group")
        fuchsCmds.inViewMessage( amg='Select <hl>Source</hl> and <hl>Target</hl> group.', pos='midCenter', fade=True )
        return
    fuchsCmds.select(None)
    success = blendshapeCreator()
    fuchsCmds.refresh()
    AlembicBlenderDisplay(success)