#Time Control v0.1

import maya.cmds as mc
import maya.mel

def plabackSpeed(interval):
    mc.playbackOptions(by=interval)
    mc.inViewMessage( amg='Time interval set to <hl>'+str(interval)+'<hl/> .', pos='midCenter', fade=True )
    print(end="Time interval set to "+str(interval)+".")
    

def frameSnap(BoolValue):
    aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
    mc.timeControl(aPlayBackSliderPython,e=True, snap=BoolValue)
    if BoolValue:
        mc.inViewMessage( amg='Enabled <hl>Frame Snap</hl> in time slider.', pos='midCenter', fade=True )
        print(end="Frame snap enabled.")
    else:
        mc.inViewMessage( amg='Disabled <hl>Frame Snap</hl> in time slider.', pos='midCenter', fade=True )
        print(end="Frame snap disabled.")