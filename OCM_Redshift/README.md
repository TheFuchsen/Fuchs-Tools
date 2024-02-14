# OBSOLETE, DO NOT USE - One Click Material For Maya 2023 - Redshift Edition -


USE OCP INSTEAD: (Temp link)


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

## Works with:

Color, Roughness, Metalness, Ambient Occlusion, Normal, RMO and Displacement. (Automatically targets name variants, like "diffuse" or "Albedo" or "Metallic", etc)

If map is not recognized, it is filtered out.

Works flawlessly with [ambientcg.com](https://ambientcg.com/) materials! (It was designed using the library as a playtesting field).

## Installation:

1. [Download OCM_RedshiftEdition](https://github.com/TheFuchsen/Fuchs-Tools/tree/main/OCM_Redshift)
2. Copy files to maya 2023 scripts folder (documents/maya/2023/scripts)
3. Create a shelf button using this command:

```
import OCM_RedshiftEdition_v1 as ocmrs
ocmrs.OCM_Redshift()
```

## Usage:

OCM can create a material for any group of maps as long as a single map convention is detected. It can use every file or just one.
Each instance of OCM creates a new material using the files first text block.

![maya_yDNinXU5q5](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/ce127936-5b74-4827-a438-aee6827004ad)

If the selection also includes the place2dNodes, OCM will merge them.

![maya_X2nI5VNnAP](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/460a9065-436a-4287-83e0-df5b7667f85d)

If geometry is selected, OCM will apply the material to the selected geometry.

![maya_vm5yQelwDv](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/e2123556-d31d-49dc-9007-ca56feacb600)

OCM detects and fixes conflictive normal files. If more than 1 normal file is selected, it will prefer the best option (OpenGL for Redshift)

![maya_FySDI0nI7l](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/f3288347-578a-4b1e-9a9b-3fa5b3b4fe7b)

A future version will support selection of Redshift Material nodes in order to add selected files to existing Redshift Standard Material.


Enjoy!


TO DO:

* -Arnold Edition (Coming)
* -Vray Edition (Needs the engine)
* -Material Updating

[![BuyMeACoffee](https://i.imgur.com/BRDKf5t.png)](https://ko-fi.com/thefuchsen)

