# ECHIDNA (echidna_obj)

Echidna is a package for parsing .obj data models working with ADENITA - a nanoscience software tool application developed at the AIT by Elisa DeLlano and Haichao Miao - 
and supports novel approaches in the design process for DNA nanostructures. The python package has an independent, built-in representation for abstract visualization of the model. 
It is supposed to be used with the molecular modeling software SAMSON via the IPy console.
(More informations here : www.samson-connect.net)
The package can be installed via PyPI to view models within the terminal/console and python 3. 

In Terminal/Console (wireframe example): 
```python
$ python3 parse_wire_.py 
```

In Ipython (in SAMSON) (nanotube example): 
```
from parse_tube_ import Obj_tube
file = Obj_tube("/User/.../file.obj")
# for visual (abstract) representation (optional) 
file.vis()
```
After calling the module, the program will ask for the input file to proceed. 

For initial use with SAMSON and ADENITA copy the package folder into SAMSON/Binaries folder 
and call it via IPy in SAMSON. (for User input see SAMSON_IPY Userinput.md)

### INPUT DATA / Construction of the input *.obj file 

The input data can be generated with diverse 3D software, which is able to export to the .obj data format.
Optional a model can be constructed with Polygon mesh based sofware (https://en.wikipedia.org/wiki/Polygon_mesh)
or NURBS based software (https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline).
Before exporting the enclosed meshes should be assigned with material to implement the material propoerties into the data model.
For nanotube parsing each cylinder primitive (i.e. each tube) should be prepared as individual joined mesh and reduced to minimal vertex count.
The export options after construction : 
- Export options for Polygon mesh models : create a polygon mesh model and export the final geometry as .obj without specifications.

- Export options for NURBS models : create a nurbs-based model, do not change nurbs model to mesh and export 
with choosing "polygon mesh" in export options.


### DEPENDENCIES

To install and use this Package, SAMSON (with IPy) and Python 3.6.X is required. 
For abstract visualization of the object file, this package can also be run directly via console / terminal (python3).

For more informations on the installation and pre-set up process for using the package in SAMSON environment, please visit https://www.samson-connect.net/ and https://documentation.samson-connect.net/scripting-guide/.
##### Python Dependencies :
   - math
   - os
   - re
   - numpy
   - scipy
   - scipy.spatial.distance
   - matplotlib 3.0.2 (or higher)
   - mpl_toolkits (will be automatically installed by matplotlib version)
   - scikit learn (requires scipy 0.13.3, numpy 1.8.2)



