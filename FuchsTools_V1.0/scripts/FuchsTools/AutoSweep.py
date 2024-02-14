import maya.cmds as fuchsCmds
def AutoSweep():
    def selWarningCall():
        fuchsCmds.warning("Select a curve object or the edges of a mesh")
        fuchsCmds.inViewMessage( amg='Select an <hl>edge</hl> or a <hl>curve</hl> to build the sweep.', pos='midCenter', fade=True )
    selection=fuchsCmds.ls(selection=True)
    if len(selection)>0:
        if fuchsCmds.nodeType(fuchsCmds.listRelatives(selection,shapes=True))=="nurbsCurve":
            fuchsCmds.CreateSweepMesh
            fuchsCmds.sweepMeshFromCurve(oneNodePerCurve=1)
        elif fuchsCmds.nodeType(selection)=="transform" and fuchsCmds.nodeType(fuchsCmds.listRelatives(selection,shapes=True))=="mesh":
            selWarningCall()
        else:
            fuchsCmds.polyToCurve(selection,form=2,degree=3,conformToSmoothMeshPreview=1,name="sweepCurve1")
            fuchsCmds.CreateSweepMesh
            fuchsCmds.sweepMeshFromCurve(oneNodePerCurve=1)
    else:
        selWarningCall()