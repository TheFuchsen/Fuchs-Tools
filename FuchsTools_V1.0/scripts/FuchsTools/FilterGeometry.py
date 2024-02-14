import maya.cmds as fuchsCmds

def filterGeoSelection():
    selected=fuchsCmds.ls(sl=1)
    geoList=[]
    notGeo=[]
    if selected:
        for obj in selected:
            primos=fuchsCmds.listRelatives(obj,children=True,fullPath=True)
            if fuchsCmds.nodeType(primos[0])=="mesh":
                geoList.append(obj)
            else:
                notGeo.append(obj)
        if geoList:
            fuchsCmds.select(geoList)
            print("Removed from selection:",notGeo)
            fuchsCmds.inViewMessage( amg='Filtered <hl>geometry</hl> from selection.', pos='midCenter', fade=True )
            print("Filtered geo:",geoList)
        else:
            fuchsCmds.inViewMessage( amg='No <hl>mesh</hl> objects were selected', pos='midCenter', fade=True )
            fuchsCmds.warning("No mesh objects were selected.")
    else:
        fuchsCmds.inViewMessage( amg='Select objects you want to filter.', pos='midCenter', fade=True )
        fuchsCmds.warning("Nothing was selected.")