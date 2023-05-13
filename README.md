# Fuchs Tools

**One Click Material For Maya 2023 - Redshift Edition**

Instantly assemble almost any material you cross in your path into a single shader! Just 1 click away.



![Image](https://user-images.githubusercontent.com/104402512/238112780-88913a52-ad0a-43cc-8113-56daf604fbd6.gif)

## What can it do?


* Detects maps, geometry and place2dTexture nodes and sorts them.
* Creates the material using your maps name structure.
* Sets color space for every map.
* Enables UDIM if detected.
* Merges all place2dTexture nodes if selected.
* Creates and sets necessary utility nodes if needed for bump, normal and displacement maps.
* Applies the material to any geometry selected.
* Filters out normal maps by type and adjusts them if necessary for proper normal display (DX or GL if on the file name).

Works with:

Color, Roughness, Metalness, Ambient Occlusion, Normal, RMO and Displacement.

If map is not recognized, it is filtered out.

Works flawlessly with ambientcg.com materials! (It was designed using the library as a playtesting field).

## Installation:

1. [Download OCM_RedshiftEdition](https://github.com/TheFuchsen/Fuchs-Tools/tree/main/OCM_Redshift)
2. Copy files to maya 2023 scripts folder (documents/maya/2023/scripts)
3. Create a shelf button using this command:

```
import OCM_RedshiftEdition_v1 as ocmrs
ocmrs.OCM_Redshift()
```

Enjoy!


TO DO:

* -Arnold Edition (Coming)
* -Vray Edition (Needs the engine)
