import maya.cmds as fuchsCmds
def selHardEdges():
    selection=fuchsCmds.ls(selection=True)
    if selection:
        fuchsCmds.polySelectConstraint(m=3,t=0x8000, sm=1)
        fuchsCmds.polySelectConstraint(m=0,t=0x8000, sm=0)
    else:
        fuchsCmds.warning("Nothing is selected.")