# environment-generator-Maya-plugin
Maya plugin UI to generate 3d environments using a PNG object placement map and the files of whatever 3d model files you want to appear in your environment.


INSTRUCTIONS FOR INSTALLING PLUGIN

1. Download all of the files in the "Demo Files" folder in the repo
2. In Maya, navigate to Windows>Settings/Preferences>Plug-in Manager
3. In the Plug-in Manager click on the "Browse" button and open the helloCmd.mll file you downloaded
4. After that plugin is loaded in, navigate to Windows>General Editors>Script Editor
5. Here open up the vfxResearchPython.py file you downloaded and run the script
6. The UI should now pop up in Maya

INSTRUCTIONS FOR USING PLUGIN

1. In 'Map File' file selector, select the pixel map PNG file you want to use for object placement _(you can use the testObjMap.png in the google drive folder for testing)_
2. In the 'Floor Layer' file selector, select the pixel map PNG file you want to use for floor topography _(you can use the testTopography.png in the google drive folder for testing)_
3. Hit the 'Interpret Map' button to get the object selectors for all the pixel colors in the 'Map File'
4. For each color you want an object to appear on, select an object file (.obj, .fbx) and use the dials to get the positioning you want
5. Hit the "Interpret Floor Map" button to create the floor of the environmentHit the "Create 3D Environment" button at the bottom of the UI to place the objects in the environment
