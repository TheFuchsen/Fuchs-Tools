# FuchsTools

## One Click Material

## Material Set

## Shader Helper

## Place 2d Merger

## Refresh UV Tiles and Remove Unused Shading Nodes

These are just shortcuts for already available tools in maya, but that are usually in a very inconvenient place.

## Color Space Shortcuts

## Make Me Random

## FBX node patcher

## Unpaste

## Select Hard Edges

Very handy tool to select hard edges.

## Tesselation Switch

Batch modify Tesselation settings for multiple objects. TBH I made this before I was aware the Object Mesh Parameters existed, so use that instead, it is better in every way.

## Quick Toggles

### Wireframe

### Primary Visibility

This can also be done better with Mesh Parameters but I've gotten used to this.

### Filter Mesh

### Auto Sweep

### Toggle Hair

### Dup Detector

## Alembic Tools

### Alembic Shortcuts

![AlembicExport](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/55207e74-9cdd-45e5-b6d6-b5b120814651)![AlembicImport](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/11380e0e-d75c-46b5-b8ff-a8e210f52c2e)![AlembicUpdate](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/ca13eb4f-e7c2-4cc5-bf16-2c0b29153472)

We do a lot of our pipeline around Alembics, so having quick access to these options is vital. 

1. Export Alembic Cache: Exports selected geometry as an alembic file
2. Import: This is just the import button. We use it to import alembics :D
3. Update alembic: This is a tricky one. By default, "Replace Alembic" just deletes your original geo and reimports your alembic. However, there is a special setting in the "import alembic" button that allows you to just create a new alembic node into existing geometry, efectively allowing you to update the alembic file that's driving your geo. It is already pre configured. 

### Alembic Blendshapes

![AlembicBlender](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/204f7224-af50-43ca-a23a-77c2ac798e04)

Given a source and target, creates a blendshape between multiple geometries. Usefull to link animation Alembic with Lookdev geo or simulation hosts.



## Animation Helpers

### Toggle Evaluation

![EvaDG](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/98a73daa-1394-4694-b21f-f512b9c5fc1c)![EvaParallel](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/707582a3-e9c3-4cc5-b660-06dd28c2182b)

Quick shortcut to switch between parallel and DG evaluation mode. 

### Timeline Snap

![TimeFloat](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/f83f2214-c9fd-4a8c-9a8f-26b562d60761)![TimeInt](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/758b71a9-4560-4d72-9d07-621c42d82640)

Toggles Frame Snap in the timeline.  Incredibly usefull when animating for motion blur.

![maya_tQxUQz2u4k](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/937d8c54-505c-48f7-87c0-f686dfe8494d)

### Playback Step

![FrameHalf](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/aa59726a-3173-467a-a2da-0fbde60cb44c)![FrameFull](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/05ba8e08-3296-4185-8460-eed1278ec4ed)

Little script that allows to change the playback step from 1.0 to 0.5 (Will add 0.25 in the future). Very handy for limited subframe exports (Like alembic)

![BoxRender](https://github.com/TheFuchsen/Fuchs-Tools/assets/104402512/9700d13b-4a24-4bc6-af04-7d3c1e69ad74)

