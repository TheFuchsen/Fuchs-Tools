# OneClick_PBR (Previously OneClickMaterial)
# October 2023
# This script can make an entire shading network with just one click!
# Shipped with FuchsTools v1
# To be used ONLY with FuchsTools. Do not edit, nor share, nor redistribute.
# By @TheFuchsen - Angel Canales
# OneClick_PBR("Redshift")
# OneClick_PBR("Arnold")
# OneClick_PBR("Vray")
# OneClick_PBR("Blinn")


import maya.cmds as fuchsCmds
import os

def OneClick_PBR(engine):

    activeEngine=engine
    

    materialDictionary = {
        "shaders":["RedshiftStandardMaterial","standardSurface","blinn","aiStandardSurface","VRayMtl","RedshiftMaterial"],
        "color":["color","basecolor","albedo","diffuse"],
        "roughness":["roughness","rgh"],
        "metallic":["metalness","metallic"],
        "ao":["ambientocclusion","ao","occlusion"],
        "emission":["emissive","emission"],
        "bump":["bump"],
        "normal":["normal","normalgl","ngl","n","nrm"],
        "normaldx":["normaldx","ndx"],
        "rmo":["rmo"],
        "displacement":["displacement","height","displaceheightfield"],
        "opacity":["alpha","mask","opacity","sprite","cutout"]
    }
    redshiftDict={
        "shader":".rsSurfaceShader",
        "material":"RedshiftStandardMaterial",
        "color":".base_color",
        "roughness":[".refl_roughness"],
        "metallic":".metalness",
        "ao":[".outColor",".overall_color"],
        "emission":".emission_color",
        "normal":[".outColor","RedshiftBumpMap",".input",".out",".bump_input"],
        "displacement":[".outColor","RedshiftDisplacement",".texMap",".out",".rsDisplacementShader"],
        "opacity":["Unused because this changes from case to case and redshift has like 4 different ways to make an alpha"],
        "naming":"_MTL_RSM"
    }
    redshiftVintageDict={
        "shader":".rsSurfaceShader",
        "material":"RedshiftMaterial",
        "color":".diffuse_color",
        "roughness":[".refl_roughness"],
        "metallic":".refl_metalness",
        "ao":[".outColor",".overall_color"],
        "emission":".emission_color",
        "normal":[".outColor","RedshiftBumpMap",".input",".out",".bump_input"],
        "displacement":[".outColor","RedshiftDisplacement",".texMap",".out",".rsDisplacementShader"],
        "opacity":["Unused because this changes from case to case and redshift has like 4 different ways to make an alpha"],
        "naming":"_MTL_RM"
    }
    vrayDict={     
        "shader":".surfaceShader",
        "material":"VRayMtl",
        "color":".diffuseColor",
        "roughness":[".reflectionGlossiness",".useRoughness"],
        "metallic":".metalness",
        "ao":[".outAlpha",".diffuseColorAmount"],
        "emission":".illumColor",
        "normal":[".outColor","VRayNormalMap",".map",".outColor",".bumpMap"],
        "displacement":["OCP does not support Vray displacement. Use manual Displacement sets."],
        "opacity":".opacityMap",
        "naming":"_MTL_VR"
    }
    standardDict={     
        "shader":".aiSurfaceShader",
        "material":"standardSurface",
        "color":".baseColor",
        "roughness":[".specularRoughness"],
        "metallic":".metalness",
        "ao":[".outAlpha",".base",".specular"],
        "emission":".emissionColor",
        "normal":[".outAlpha","bump2d",".bumpValue",".outNormal",".normalCamera"],
        "displacement":[".outAlpha","displacementShader",".displacement",".displacement",".displacementShader"],
        "opacity":["Unused because this changes from case to case"],
        "naming":"_MTL_AI"
    }
    blinnDict={
        "shader":".surfaceShader",
        "material":"blinn",
        "color":".color",
        "roughness":[".eccentricity"],
        "metallic":".reflectivity",
        "ao":[".diffuse",".specularColor"],
        "emission":".incandescence",
        "normal":[".outAlpha","bump2d",".bumpValue",".outNormal",".normalCamera"],
        "displacement":[".outAlpha","displacementShader",".displacement",".displacement",".displacementShader"],
        "opacity":".transparency"
    }
    engineDicts={
        "Redshift":redshiftDict,
        "RedshiftOld":redshiftVintageDict,
        "Vray":vrayDict,
        "Arnold":standardDict,
        "Blinn":blinnDict
    }

    mayaSelection=fuchsCmds.ls(selection=True)
    fileNodes=[]
    p2dNodes=[]
    geoNodes=[]
    uncategorizedFiles=[]
    pendingDeletion=[]
    hostMaterial=[]
    nodePairs={}
    isUdim=False
    mtlName = None
    logStatus=False
    duplicated=False
    normalExists=False
    normaldxExists=False
    auxiliar=False

    # Initial Display.

    print ("""
----------------------------------
One Click PBR V1 by TheFuchsen
----------------------------------
""")

    print("""Current engine is""", activeEngine+""".
          """)

    # Selection Sorter.

    for node in mayaSelection:
        if fuchsCmds.nodeType(node) == "file":
            fileNodes.append(node)
        elif fuchsCmds.nodeType(node) == "place2dTexture":
            p2dNodes.append(node)
        elif fuchsCmds.nodeType(node) == "transform":
            geoNodes.append(node)
        elif fuchsCmds.nodeType(node) in materialDictionary["shaders"]:
                hostMaterial.append(node)

    # File sorter.

    for node in fileNodes:
        identifiedNodeType = None
        nodeName= (os.path.basename(fuchsCmds.getAttr(node + '.fileTextureName')).replace(".","_")).split('_')
        if nodeName[-2].isdigit() and len(nodeName[-2]) == 4 and isUdim==False:
            isUdim = True
            print("Texture set is UDIM.")
        for category, variants in materialDictionary.items():
            for item in nodeName:
                if item.lower() in variants:
                    identifiedNodeType = category
                    print("Found "+ category+ " in "+ node+".")
                    if category == "normal":
                        normalExists=True
                    if category == "normaldx":
                        normaldxExists=True
                    break
        if identifiedNodeType:
            if identifiedNodeType not in nodePairs:
                nodePairs[identifiedNodeType]=[]
                nodePairs[identifiedNodeType].append(node)
            else:
                if isUdim:
                    pendingDeletion.append(node)
                else:
                    print("Duplicated "+identifiedNodeType+" detected.")
                    duplicated=True
        else:
            print("Coulnd't identify "+node+".")
            uncategorizedFiles.append(node)

    if duplicated:
        fuchsCmds.warning("Duplicated file types detected. Select only 1 material at a time and make sure files are named correctly. Stopping")
        return
    
    if pendingDeletion:
        print("Removing unnecesary nodes.")
        for node in pendingDeletion:
            p2dConnection=((fuchsCmds.listConnections(node+".uvCoord", c=True, p=True))[1].split(".")[0])
            if p2dNodes:
                p2dNodes.remove(p2dConnection)
            fuchsCmds.delete(p2dConnection)
            fileNodes.remove(node)
            fuchsCmds.delete(node)
            if logStatus:
                print("Deleting "+node)
        pendingDeletion=[]

    if nodePairs:        
        if geoNodes:
            print ("Detected geometry:",geoNodes)
        else:
            print ("No geometry was selected")
        if not p2dNodes:
            print ("No place2dTexture node was selected.")

        # Material Name Picker
        if not hostMaterial:
            for nodeType, nodeFiles in nodePairs.items():
                for nodeFileName in nodeFiles:
                    mtlName = (os.path.basename(fuchsCmds.getAttr(nodeFileName + '.fileTextureName')).replace(".","_")).split('_')[0]
                    break
        else:
            mtlName = str(hostMaterial[0])

        # Material Creation Multi engine
        if hostMaterial:
            if len(hostMaterial)>1:
                fuchsCmds.warning("More than 1 material node was selected. Please select just 1 material node, or skip material selection to create a new material.")
                return
            else:
                if fuchsCmds.nodeType(hostMaterial[0]) == engineDicts[activeEngine]["material"]:
                    mtlNode = hostMaterial[0]
                    print("Using ", hostMaterial[0]," as material host.")
                    mtlConnections=fuchsCmds.listConnections(mtlNode)
                    for node in mtlConnections:
                        if fuchsCmds.nodeType(node) == "shadingEngine":
                            sgNode = node
                            print(sgNode, "set as host Shading Engine")
                else:
                    if fuchsCmds.nodeType(hostMaterial[0]) == "blinn" or activeEngine == "Blinn":
                        fuchsCmds.warning("Blinn is not supported for multi engine mode. Stopping.")
                        return
                    if activeEngine == "Vray":
                        print("In order to use Vray in a multiEngine configuration, Vray material has to be the host material.")
                        fuchsCmds.warning("Vray does not have a propietary Shading input in the Shading engine to act as secondary engine. Stopping")
                        return
                    else:
                        fuchsCmds.warning("Selected "+fuchsCmds.nodeType(hostMaterial[0])+" is not a "+engineDicts[activeEngine]["material"]+". Creating an auxiliar material instead.")
                        mtlConnections=fuchsCmds.listConnections(hostMaterial[0])
                        for nodeType, nodeFiles in nodePairs.items():
                            for nodeFileName in nodeFiles:
                                mtlName = (os.path.basename(fuchsCmds.getAttr(nodeFileName + '.fileTextureName')).replace(".","_")).split('_')[0]
                                break
                        mtlNode=fuchsCmds.shadingNode(engineDicts[activeEngine]["material"], asShader=True, name=mtlName+engineDicts[activeEngine]["naming"])
                        auxiliar=True
                        for node in mtlConnections:
                            if fuchsCmds.nodeType(node) == "shadingEngine":
                                sgNode = node
                                print(sgNode, "set as host Shading Engine")
                        fuchsCmds.connectAttr (mtlNode+".outColor", sgNode+(engineDicts[activeEngine]["shader"]))
        else:
            mtlNode=fuchsCmds.shadingNode(engineDicts[activeEngine]["material"], asShader=True, name=mtlName+"_MTL")
            sgNode=fuchsCmds.sets(renderable=True,noSurfaceShader=True,empty=True, name=mtlName+"_SG")
            fuchsCmds.connectAttr (mtlNode+".outColor", sgNode+".surfaceShader")  

        # Color Space Assigner

        def setColorSpace(fileNode,colorSpace):
            fuchsCmds.setAttr(fileNode+".colorSpace", colorSpace, type="string")
            fuchsCmds.setAttr(fileNode+".ignoreColorSpaceFileRules", 1)

        # Connection Sorter
        for connection, fileNames in nodePairs.items():
            for singleFile in fileNames:
                if connection == "opacity":
                    if activeEngine == "Blinn":
                        fuchsCmds.connectAttr(singleFile+".outColor", mtlNode+engineDicts[activeEngine]["opacity"], force=True)
                        setColorSpace(singleFile,"Raw")
                        break
                    else:
                        print("Opacity has to be manually reviewed for "+activeEngine+". Skipping.")
                        p2dConnection=((fuchsCmds.listConnections(singleFile+".uvCoord", c=True, p=True))[1].split(".")[0])
                        p2dNodes.remove(p2dConnection)
                        uncategorizedFiles.append(singleFile)
                        break
                if connection == "color":
                    fuchsCmds.connectAttr(singleFile+".outColor", mtlNode+engineDicts[activeEngine]["color"], force=True)
                    setColorSpace(singleFile,"sRGB")
                    break
                if connection == "roughness":
                    if activeEngine=="Blinn":
                        setRangeNodeRough = fuchsCmds.shadingNode("setRange", asUtility=True)   
                        fuchsCmds.setAttr(setRangeNodeRough+".minX",0.1)
                        fuchsCmds.setAttr(setRangeNodeRough+".maxX",1)
                        fuchsCmds.setAttr(setRangeNodeRough+".oldMaxX",1)
                        fuchsCmds.connectAttr(singleFile+".outAlpha", setRangeNodeRough+".value.valueX", force=True)
                        fuchsCmds.connectAttr(setRangeNodeRough+".outValue.outValueX", mtlNode+engineDicts[activeEngine]["roughness"][0], force=True)
                        break
                    if activeEngine=="Vray":
                        fuchsCmds.setAttr(mtlNode+".useRoughness",1)     
                    fuchsCmds.connectAttr(singleFile+".outAlpha", mtlNode+engineDicts[activeEngine]["roughness"][0], force=True)
                    setColorSpace(singleFile,"Raw")
                    break
                if connection == "metallic":
                    if activeEngine=="RedshiftOld":
                        fuchsCmds.setAttr(mtlNode+".refl_fresnel_mode", 2, force=True)
                    fuchsCmds.connectAttr(singleFile+".outAlpha", mtlNode+engineDicts[activeEngine]["metallic"], force=True)
                    setColorSpace(singleFile,"Raw")
                    break
                if connection == "ao":
                    if activeEngine=="Redshift" or activeEngine=="RedshiftOld":
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["ao"][0], mtlNode+engineDicts[activeEngine]["ao"][1], force=True)
                        setColorSpace(singleFile,"sRGB")
                        break
                    if activeEngine =="Arnold":
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["ao"][0], mtlNode+engineDicts[activeEngine]["ao"][1], force=True)
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["ao"][0], mtlNode+engineDicts[activeEngine]["ao"][2], force=True)
                        setColorSpace(singleFile,"sRGB")
                        break
                    if activeEngine =="Vray":
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["ao"][0], mtlNode+engineDicts[activeEngine]["ao"][1], force=True)
                        setColorSpace(singleFile,"sRGB")
                        break
                    if activeEngine =="Blinn":
                        setRangeNodeAO = fuchsCmds.shadingNode("setRange", asUtility=True)   
                        fuchsCmds.setAttr(setRangeNodeAO+".maxX",0.8)
                        fuchsCmds.setAttr(setRangeNodeAO+".oldMaxX",1)
                        fuchsCmds.connectAttr(singleFile+".outColor", setRangeNodeAO+".value", force=True)
                        fuchsCmds.connectAttr(setRangeNodeAO+".outValue.outValueX", mtlNode+engineDicts[activeEngine]["ao"][0], force=True)
                        fuchsCmds.connectAttr(setRangeNodeAO+".outValue", mtlNode+engineDicts[activeEngine]["ao"][1], force=True)
                        break
                if connection == "emission":
                    fuchsCmds.connectAttr(singleFile+".outColor", mtlNode+engineDicts[activeEngine]["emission"], force=True)
                    setColorSpace(singleFile,"sRGB")
                    break
                if connection == "rmo":
                    if activeEngine =="Blinn":
                        setRangeNodeRough = fuchsCmds.shadingNode("setRange", asUtility=True)   
                        fuchsCmds.setAttr(setRangeNodeRough+".minX",0.1)
                        fuchsCmds.setAttr(setRangeNodeRough+".maxX",1)
                        fuchsCmds.setAttr(setRangeNodeRough+".oldMaxX",1)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorR", setRangeNodeRough+".value.valueX", force=True)
                        fuchsCmds.connectAttr(setRangeNodeRough+".outValue.outValueX", mtlNode+engineDicts[activeEngine]["roughness"], force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorG", mtlNode+engineDicts[activeEngine]["metallic"], force=True)
                        setRangeNodeAO = fuchsCmds.shadingNode("setRange", asUtility=True)   
                        fuchsCmds.setAttr(setRangeNodeAO+".maxX",0.8)
                        fuchsCmds.setAttr(setRangeNodeAO+".oldMaxX",1)
                        fuchsCmds.connectAttr(singleFile+".outColor", setRangeNodeAO+".value", force=True)
                        fuchsCmds.connectAttr(setRangeNodeAO+".outValue.outValueX", mtlNode+engineDicts[activeEngine]["ao"][0], force=True)
                        fuchsCmds.connectAttr(setRangeNodeAO+".outValue", mtlNode+engineDicts[activeEngine]["ao"][1], force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", setRangeNodeRough+".value.valueX", force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", setRangeNodeRough+".value.valueY", force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", setRangeNodeRough+".value.valueZ", force=True)
                        setColorSpace(singleFile,"Raw")
                        break
                    else:
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorR", mtlNode+engineDicts[activeEngine]["roughness"][0], force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorG", mtlNode+engineDicts[activeEngine]["metallic"], force=True)
                    if activeEngine =="Arnold":
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+engineDicts[activeEngine]["ao"][1], force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+engineDicts[activeEngine]["ao"][2], force=True)
                        break
                    if activeEngine=="Redshift" or activeEngine=="RedshiftOld":
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+engineDicts[activeEngine]["ao"][1]+engineDicts[activeEngine]["ao"][1]+"R", force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+engineDicts[activeEngine]["ao"][1]+engineDicts[activeEngine]["ao"][1]+"G", force=True)
                        fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+engineDicts[activeEngine]["ao"][1]+engineDicts[activeEngine]["ao"][1]+"B", force=True)
                        setColorSpace(singleFile,"Raw")
                        break
                    if activeEngine=="Vray":
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["ao"][0], mtlNode+engineDicts[activeEngine]["ao"][1], force=True)
                        fuchsCmds.setAttr(mtlNode+".useRoughness",1)    
                        setColorSpace(singleFile,"Raw")
                        break
                if connection == "displacement":
                    if activeEngine=="Vray":
                        print ("OCP does not support Vray Displacement. Use Vray Displacement Sets instead. Skipping.")
                        p2dConnection=((fuchsCmds.listConnections(singleFile+".uvCoord", c=True, p=True))[1].split(".")[0])
                        p2dNodes.remove(p2dConnection)
                        uncategorizedFiles.append(singleFile)
                        print(p2dConnection)
                        break
                    else:
                        displacementNode = fuchsCmds.shadingNode(engineDicts[activeEngine]["displacement"][1], name=singleFile.split("_")[0]+"_dispN", asShader=True)        
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["displacement"][0], displacementNode+engineDicts[activeEngine]["displacement"][2], force=True)
                        fuchsCmds.connectAttr(displacementNode+engineDicts[activeEngine]["displacement"][3], sgNode+engineDicts[activeEngine]["displacement"][4], force=True)
                        setColorSpace(singleFile,"Raw")
                        break
                if connection == "normal":
                    bumpNode = fuchsCmds.shadingNode(engineDicts[activeEngine]["normal"][1], name=singleFile.split("_")[0]+"_normalN", asShader=True) 
                    fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["normal"][0], bumpNode+engineDicts[activeEngine]["normal"][2], force=True)
                    fuchsCmds.connectAttr(bumpNode+engineDicts[activeEngine]["normal"][3], mtlNode+engineDicts[activeEngine]["normal"][4], force=True)
                    if activeEngine == "Redshift" or activeEngine=="RedshiftOld":
                        fuchsCmds.setAttr(bumpNode+".inputType", 1)
                        fuchsCmds.setAttr(bumpNode+".scale", 1)
                        setColorSpace(singleFile,"Raw")
                        break
                    if activeEngine == "Blinn" or activeEngine == "Arnold":
                        fuchsCmds.setAttr(bumpNode+".bumpInterp", 1)
                        fuchsCmds.setAttr(bumpNode+".bumpDepth", 0.5)
                        setColorSpace(singleFile,"Raw")
                        break
                    if activeEngine == "Vray":
                        fuchsCmds.setAttr(bumpNode+".mapType", 1)
                        setColorSpace(singleFile,"Raw")
                        break
                if connection == "normaldx":
                    if not normalExists:
                        print ("Normal map is a DirectX. Flipping green channel.")      
                        bumpNode = fuchsCmds.shadingNode(engineDicts[activeEngine]["normal"][1], name=singleFile.split("_")[0]+"_normalN", asShader=True) 
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["normal"][0], bumpNode+engineDicts[activeEngine]["normal"][2], force=True)
                        fuchsCmds.connectAttr(bumpNode+engineDicts[activeEngine]["normal"][3], mtlNode+engineDicts[activeEngine]["normal"][4], force=True)
                        if activeEngine == "Redshift" or activeEngine=="RedshiftOld":
                            fuchsCmds.setAttr(bumpNode+".inputType", 1)
                            fuchsCmds.setAttr(bumpNode+".scale", 1)
                            fuchsCmds.setAttr(bumpNode+".flipY", 1) 
                            setColorSpace(singleFile,"Raw")
                            normaldxExists=True
                            break
                        if activeEngine == "Blinn" or activeEngine == "Arnold":                       
                            fuchsCmds.setAttr(bumpNode+".bumpInterp", 1)
                            fuchsCmds.setAttr(bumpNode+".bumpDepth", -0.5)
                            fuchsCmds.setAttr(bumpNode+".aiFlipG", 1) 
                            setColorSpace(singleFile,"Raw")
                            normaldxExists=True
                            break
                        if activeEngine == "Vray":
                            fuchsCmds.setAttr(bumpNode+".mapType", 1)
                            fuchsCmds.setAttr(bumpNode+".flipGreen", 1)
                            setColorSpace(singleFile,"Raw")
                            break
                    else:
                        print ("Skipping NormalDX map.")
                        pendingDeletion.append(singleFile)
                        break
                if connection == "bump":
                    if not normaldxExists and not normalExists:
                        bumpNode = fuchsCmds.shadingNode(engineDicts[activeEngine]["normal"][1], name=singleFile.split("_")[0]+"_normalN", asShader=True) 
                        fuchsCmds.connectAttr(singleFile+engineDicts[activeEngine]["normal"][0], bumpNode+engineDicts[activeEngine]["normal"][2], force=True)
                        fuchsCmds.connectAttr(bumpNode+engineDicts[activeEngine]["normal"][3], mtlNode+engineDicts[activeEngine]["normal"][4], force=True)
                        setColorSpace(singleFile,"Raw")
                        print ("No normal map found. Using "+singleFile+" as bump instead.")
                        break
                    else:
                        print ("Skipping bump map.")
                        pendingDeletion.append(singleFile)
                        break

        # Getting rid of the trash

        if pendingDeletion:
            for node in pendingDeletion:
                p2dConnection=((fuchsCmds.listConnections(node+".uvCoord", c=True, p=True))[1].split(".")[0]) 
                if p2dNodes:
                    p2dNodes.remove(p2dConnection)
                fuchsCmds.delete(p2dConnection)
                fileNodes.remove(node)
                fuchsCmds.delete(node)
                if logStatus:
                    print("Deleting "+node)
                pendingDeletion.clear
            for node in uncategorizedFiles:
                if p2dNodes:
                    try:
                        p2dNodes.remove((fuchsCmds.listConnections(node+".uvCoord", c=True, p=True))[1].split(".")[0])
                    except:
                        pass
                fileNodes.remove(node)

        # Merging place2dTexture Nodes

        if p2dNodes:
            targetP2D = fuchsCmds.shadingNode("place2dTexture", asUtility=True, name = mtlName+"_p2dt")
            print ("Merging place2dTexture nodes.")

            for fileNode in fileNodes:
                fuchsCmds.connectAttr(targetP2D+".coverage", fileNode+".coverage", force=True)
                fuchsCmds.connectAttr(targetP2D+".mirrorU", fileNode+".mirrorU", force=True)
                fuchsCmds.connectAttr(targetP2D+".mirrorV", fileNode+".mirrorV", force=True)
                fuchsCmds.connectAttr(targetP2D+".noiseUV", fileNode+".noiseUV", force=True)
                fuchsCmds.connectAttr(targetP2D+".offset", fileNode+".offset", force=True)
                fuchsCmds.connectAttr(targetP2D+".repeatUV", fileNode+".repeatUV", force=True)
                fuchsCmds.connectAttr(targetP2D+".rotateFrame", fileNode+".rotateFrame", force=True)
                fuchsCmds.connectAttr(targetP2D+".rotateUV", fileNode+".rotateUV", force=True)
                fuchsCmds.connectAttr(targetP2D+".stagger", fileNode+".stagger", force=True)
                fuchsCmds.connectAttr(targetP2D+".translateFrame", fileNode+".translateFrame", force=True)
                fuchsCmds.connectAttr(targetP2D+".outUV", fileNode+".uvCoord", force=True)
                fuchsCmds.connectAttr(targetP2D+".outUvFilterSize", fileNode+".uvFilterSize", force=True)
                fuchsCmds.connectAttr(targetP2D+".vertexCameraOne", fileNode+".vertexCameraOne", force=True)
                fuchsCmds.connectAttr(targetP2D+".vertexUvOne", fileNode+".vertexUvOne", force=True)
                fuchsCmds.connectAttr(targetP2D+".vertexUvTwo", fileNode+".vertexUvTwo", force=True)
                fuchsCmds.connectAttr(targetP2D+".vertexUvThree", fileNode+".vertexUvThree", force=True)
                fuchsCmds.connectAttr(targetP2D+".wrapU", fileNode+".wrapU", force=True)
                fuchsCmds.connectAttr(targetP2D+".wrapV", fileNode+".wrapV", force=True)

            for p2dNode in p2dNodes:
                fuchsCmds.delete(p2dNode)

        if isUdim:
            for node in fileNodes:
                fuchsCmds.setAttr(node+".uvTilingMode", 3)

        if geoNodes:
            print ("Applying material to selected Geometry.")
            for targetTransform in geoNodes:
                fuchsCmds.sets( targetTransform, edit=True, forceElement=sgNode)
        print ("""----------------------------------
""")
        if hostMaterial:
            print ("Material", mtlName, "updated.")
        else:
            print ("Material", mtlName, "created.")
    else:
        print ("First select at least 1 file node you will use for the material creation.")
        fuchsCmds.warning("First select at least 1 file node you will use for the material creation.")
    
    if logStatus:
        print (nodePairs)