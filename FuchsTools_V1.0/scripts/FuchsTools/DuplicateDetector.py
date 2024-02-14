import maya.cmds as fuchsCmds

def duplicateDetector():
    selected=fuchsCmds.ls(sl=1, absoluteName=True)
    print(selected)
    objectList={}
    foundDuplicate=[]
    stripNameDuplicated=[]
    for obj in selected:
        stripName=obj.split("|")[-1].split(":")[-1]
        if stripName not in objectList:
            objectList[stripName]=[]
            objectList[stripName].append(obj)
        else:
            foundDuplicate.append(obj)
            if stripName not in stripNameDuplicated:
                stripNameDuplicated.append(stripName)
            if objectList[stripName][0] not in foundDuplicate:
                foundDuplicate.append(objectList[stripName][0])
    if foundDuplicate:
        fuchsCmds.warning("Duplicate found! ", stripNameDuplicated)
        print(objectList)
        fuchsCmds.inViewMessage( amg="Duplicate found! "+str(stripNameDuplicated)+".", pos='midCenter', fade=True )
        fuchsCmds.select(foundDuplicate)
    else:
        fuchsCmds.inViewMessage( amg="No duplicates were found.", pos='midCenter', fade=True )
