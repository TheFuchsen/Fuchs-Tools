# By @TheFuchsen - Angel Canales
# https://github.com/TheFuchsen
# May 2023
# To do: Cleaner material assembly for easier engine port.

import maya.cmds as fuchsCmds
import os

def OCM_Redshift():

    print ("""
    
----------------------------------
One click Material for Redshift v3
----------------------------------
""")

    # Base Lists and selection sorter.

    mayaSelection=fuchsCmds.ls(selection=True)
    fileNodes=[]
    p2dNodes=[]
    geoNodes=[]
    uncategorizedFiles=[]
    nodePairs={}
    normalList = []
    isUdim=False
    mtlName = None

    for node in mayaSelection:
        if fuchsCmds.nodeType(node) == "file":
            fileNodes.append(node)
        if fuchsCmds.nodeType(node) == "place2dTexture":
            p2dNodes.append(node)
        elif fuchsCmds.nodeType(node) == "transform":
            geoNodes.append(node)

    # Node Sorter

    materialDictionary = {
        "color":["color","basecolor","albedo","diffuse"],
        "roughness":["roughness"],
        "metallic":["metalness","metallic"],
        "ao":["ambientocclusion","ao","occlusion"],
        "emission":["emissive","emission"],
        "normal":["normal","normaldx","normalgl","bump"],
        "rmo":["rmo"],
        "displacement":["displacement","height"],
        "opacity":["alpha","mask","opacity","sprite","cutout"]
    }

    # Node connection Sorting

    for node in fileNodes:
        identifiedNodeType = None
        nodeName= (os.path.basename(fuchsCmds.getAttr(node + '.fileTextureName')).replace(".","_")).split('_')
        for category, variants in materialDictionary.items():
            for variant in variants:
                for item in nodeName:
                    if item.lower() == variant:
                        identifiedNodeType = category
                        print("Found ", category, " in ", node,".")
                        break
        second_to_last = nodeName[-2]
        if second_to_last.isdigit() and len(second_to_last) == 4:
            isUdim = True
        if identifiedNodeType:
            if identifiedNodeType not in nodePairs:
                nodePairs[identifiedNodeType]=[]
            nodePairs[identifiedNodeType].append(node)
        else:
            print("Coulnd't identify ", node,".")
            uncategorizedFiles.append(node)

    # Script Execution

    if nodePairs:        
        if geoNodes:
            print ("Detected geometry:",geoNodes)
        else:
            print ("No geometry was selected")
        if not p2dNodes:
            print ("No place2dTexture node was selected.")

        # Material Name Picker

        for nodeType, nodeFiles in nodePairs.items():
            for nodeFileName in nodeFiles:
                mtlName = (os.path.basename(fuchsCmds.getAttr(nodeFileName + '.fileTextureName')).replace(".","_")).split('_')[0]
                break

        # Material Creation

        mtlNode=fuchsCmds.shadingNode("RedshiftStandardMaterial", asShader=True, name=mtlName+"_MTL")
        sgNode=fuchsCmds.sets(renderable=True,noSurfaceShader=True,empty=True, name=mtlName+"_SG")
        fuchsCmds.connectAttr (mtlNode+".outColor", sgNode+".surfaceShader")  



        # Color Space Assigner

        def setColorSpace(fileNode,colorSpace):
            fuchsCmds.setAttr(fileNode+".colorSpace", colorSpace, type="string")
            fuchsCmds.setAttr(fileNode+".ignoreColorSpaceFileRules", 1)

        # Connection Sorter

        for connection, fileNames in nodePairs.items():
            for singleFile in fileNames:
                if connection == "color":
                    fuchsCmds.connectAttr(singleFile+".outColor", mtlNode+".base_color", force=True)
                    setColorSpace(singleFile,"sRGB")
                    break
                if connection == "roughness":
                    fuchsCmds.connectAttr(singleFile+".outAlpha", mtlNode+".refl_roughness", force=True)
                    setColorSpace(singleFile,"Raw")
                    break
                if connection == "metallic":
                    fuchsCmds.connectAttr(singleFile+".outAlpha", mtlNode+".metalness", force=True)
                    setColorSpace(singleFile,"Raw")
                    break
                if connection == "ao":
                    fuchsCmds.connectAttr(singleFile+".outColor", mtlNode+".overall_color", force=True)
                    setColorSpace(singleFile,"sRGB")
                    break
                if connection == "emission":
                    fuchsCmds.connectAttr(singleFile+".outColor", mtlNode+".emission_color", force=True)
                    setColorSpace(singleFile,"sRGB")
                    break
                if connection == "rmo":
                    fuchsCmds.connectAttr(singleFile+".outColor.outColorR", mtlNode+".refl_roughness", force=True)
                    fuchsCmds.connectAttr(singleFile+".outColor.outColorG", mtlNode+".metalness", force=True)
                    fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+".overall_color.overall_colorR", force=True)
                    fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+".overall_color.overall_colorG", force=True)
                    fuchsCmds.connectAttr(singleFile+".outColor.outColorB", mtlNode+".overall_color.overall_colorB", force=True)
                    setColorSpace(singleFile,"Raw")
                    break
                if connection == "displacement":
                    displacementNode = fuchsCmds.shadingNode("RedshiftDisplacement", name=singleFile.split("_")[0]+"_rsHeight", asShader=True)        
                    fuchsCmds.connectAttr(singleFile+".outColor", displacementNode+".texMap", force=True)
                    fuchsCmds.connectAttr(displacementNode+".out", sgNode+".displacementShader", force=True)
                    setColorSpace(singleFile,"Raw")
                    break
                if connection == "normal":
                    normalList.append(singleFile)
                    setColorSpace(singleFile,"Raw")
        
        # Normal Sorting and Assignment

        if normalList:
            for normalNode in normalList:
                normalNodeName = os.path.basename(fuchsCmds.getAttr(normalNode+".fileTextureName")).replace(".","_")
                if "normaldx" in normalNodeName.lower():
                    if len(normalList)>1:
                        print ("Skipping NormalDX map.")
                        fileNodes.remove(normalNode)
                        if p2dNodes:
                            p2dNodes.remove((fuchsCmds.listConnections(normalNode+".uvCoord", c=True, p=True))[1].split(".")[0])

                    else:
                        print ("Normal map is a DirectX. Flipping green channel.")      
                        bumpNode = fuchsCmds.shadingNode("RedshiftBumpMap", name=normalNodeName.split("_")[0]+"_rsBump", asTexture=True) # Node is named same as the normal map file
                        fuchsCmds.connectAttr(normalNode+".outColor", bumpNode+".input", force=True)
                        fuchsCmds.connectAttr(bumpNode+".out", mtlNode+".bump_input", force=True)
                        fuchsCmds.setAttr(bumpNode+".inputType", 1) # Sets node to Tangent Space
                        fuchsCmds.setAttr(bumpNode+".scale", 1) # Sets scale to base.
                        fuchsCmds.setAttr(bumpNode+".flipY", 1) # Flips green channel
                else:
                    bumpNode = fuchsCmds.shadingNode("RedshiftBumpMap", name=normalNodeName.split("_")[0]+"_rsBump", asTexture=True) 
                    fuchsCmds.connectAttr(normalNode+".outColor", bumpNode+".input", force=True)
                    fuchsCmds.connectAttr(bumpNode+".out", mtlNode+".bump_input", force=True)
                    fuchsCmds.setAttr(bumpNode+".inputType", 1)
                    fuchsCmds.setAttr(bumpNode+".scale", 1)

        # Remove Unused Nodes from Lists

        for node in uncategorizedFiles:
            if p2dNodes:
                p2dNodes.remove((fuchsCmds.listConnections(node+".uvCoord", c=True, p=True))[1].split(".")[0])
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
            print("Material is UDIM tiled.")
            for node in fileNodes:
                fuchsCmds.setAttr(node+".uvTilingMode", 3)

        if geoNodes:
            print ("Applying material to selected Geometry.")
            for targetTransform in geoNodes:
                fuchsCmds.sets( targetTransform, edit=True, forceElement=sgNode)
        print ("""----------------------------------
""")
        print ("Material", mtlName, "created.")
    else:
        print ("First select at least 1 file node you will use for the material creation.")
        fuchsCmds.warning("First select at least 1 file node you will use for the material creation.")