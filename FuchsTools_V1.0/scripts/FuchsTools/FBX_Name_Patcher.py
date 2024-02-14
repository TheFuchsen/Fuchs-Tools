import maya.cmds as fuchsCmds

def FBXNamePatch():

    asciiArray=["FBXASC032",
"FBXASC046",
"FBXASC044",
"FBXASC033",
"FBXASC034",
"FBXASC035",
"FBXASC036",
"FBXASC037",
"FBXASC038",
"FBXASC047",
"FBXASC040",
"FBXASC041",
"FBXASC061",
"FBXASC063",
"FBXASC194",
"FBXASC161",
"FBXASC039",
"FBXASC194",
"FBXASC191",
"FBXASC045",
"FBXASC064"]
    
    selected=fuchsCmds.ls(selection=True)
    if selected:
        for obj in selected:
            originalName=str(obj)
            patchedName=None
            tiwitiwis=False
            for i in asciiArray:
                if i in obj:
                    if not patchedName:
                        patchedName=originalName
                    patchedName=patchedName.replace(i,"_")
                    tiwitiwis=True
            if tiwitiwis:
                fuchsCmds.rename(obj,patchedName)
                print("Patching ",originalName," as ", patchedName)
            if not tiwitiwis:
                print("No conflicting names detected in ",obj)
    else:
        fuchsCmds.warning("No object selected")