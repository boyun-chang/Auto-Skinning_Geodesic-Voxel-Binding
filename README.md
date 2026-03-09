# Auto Skinning - Geodesic Voxel Binding
This project performs automatic skinning using the Geodesic Voxel Binding method.
### Main project(C++, OpenGL, CUDA)
The 3D character mesh is voxelized, including its interior, and classified into interior and boundary nodes using SAT and Scanline techniques.

Then, Dijkstra's algorithm is used to measure the geodesic distance from the skeleton node to the boundary node. This process was accelerated using CUDA.

The weights of the vertices corresponding to each bone are saved and saved as a .csv file.
### Maya Scripts(Python)
Extract the required data from the main project in Maya, run the main project's algorithm, and apply the skinning weight results to the character mesh with one click.

### How to work
0. Download the main project's .exe file (located at x64/Release/) and the Maya script code. Organize the Maya script code in your Maya project's script folder. (All MayaScripts code must be in one folder.)
1. Prepare a rigged 3D model in Maya.
2. Drag the L_AutoSkinning.py code from the script window and drop it onto the shelf.
3. Select the 3D model to be skinned and click the icon created on the shelf.
4. In the window that appears, locate and select the folder containing the Maya script code and the main project's .exe file. Set the skinning weight resolution.
5. After completing the settings, click the blue Run button to run the code.
6. Confirm that the code execution is complete in the script window and run the animation.

### Result
Result video >> <a href="https://youtu.be/0q08LPMOR0k"><img src="https://img.shields.io/badge/Youtube-FF0000?style=flat-square&logo=youtube&logoColor=white"/></a>

<img width="508" height="494" alt="Image" src="https://github.com/user-attachments/assets/289d1f0c-85b0-4974-8e02-87b83713c3c7" />
