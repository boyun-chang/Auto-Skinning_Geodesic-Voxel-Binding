# Auto Skinning - Geodesic Voxel Binding
This project performs automatic skinning using the Geodesic Voxel Binding method.
### Main project(C++, OpenGL, CUDA)
The 3D character mesh is voxelized, including its interior, and classified into interior and boundary nodes using SAT and Scanline techniques.

Then, Dijkstra's algorithm is used to measure the geodesic distance from the skeleton node to the boundary node. This process was accelerated using CUDA.

The weights of the vertices corresponding to each bone are saved and saved as a .csv file.
### Maya Tool(Python)
Extract the required data from the main project in Maya, run the main project's algorithm, and apply the skinning weight results to the character mesh with one click.
### Result
Result video >> <a href="https://youtu.be/0q08LPMOR0k"><img src="https://img.shields.io/badge/Youtube-FF0000?style=flat-square&logo=youtube&logoColor=white"/></a>

<img width="508" height="494" alt="Image" src="https://github.com/user-attachments/assets/289d1f0c-85b0-4974-8e02-87b83713c3c7" />
