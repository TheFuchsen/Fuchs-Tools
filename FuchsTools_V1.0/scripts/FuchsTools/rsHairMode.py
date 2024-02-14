import maya.cmds as fuchsCmds
                     
def rsToggleHairMode(mode):
    
    selected=fuchsCmds.ls(selection=True)
    hairDetect = False
    for obj in selected:
        if fuchsCmds.nodeType(fuchsCmds.listRelatives(obj,shapes=True,children=True)) == "xgmSplineDescription":
            hairDetect = True
            if mode == "Ribbon":
                try:
                    if fuchsCmds.getAttr(obj+".Mode") == 1:
                        fuchsCmds.setAttr(obj+".Mode",0)
                        print (obj + " set to Ribbon.")
                    else:
                        print (obj + " already set to Ribbon.")
                except:
                    fuchsCmds.warning("No strand mode found in obj. Please make sure your selected object is an IGS description.")
            if mode == "Thick":
                try:
                    if fuchsCmds.getAttr(obj+".Mode") == 0:
                        fuchsCmds.setAttr(obj+".Mode",1)
                        print (obj + " set to Thick.")
                    else:
                        print (obj + " already set to Thick.")
                except:
                    fuchsCmds.warning("No strands found. Please make sure your selected objects are an IGS description.")
    if not hairDetect:
        fuchsCmds.warning("No strands found. Please make sure your selected objects are an IGS description.")
        fuchsCmds.inViewMessage( amg='Select at least 1 <hl>IGS Description</hl>.', pos='midCenter', fade=True )
    else:
        fuchsCmds.inViewMessage( amg='Redshift IGS toggled to <hl>'+mode+'</hl>.', pos='midCenter', fade=True )

