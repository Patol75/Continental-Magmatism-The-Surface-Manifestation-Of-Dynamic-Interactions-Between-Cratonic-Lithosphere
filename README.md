# Continental Magmatism: The Surface Manifestation Of Dynamic Interactions Between Cratonic Lithosphere, Mantle Plumes And Edge-Driven Convection

In order to run the models, you must first download and compile Fluidity, available at https://github.com/FluidityProject/fluidity. Then, make sure to generate the mesh file by executing `gmsh -NDIM geo_file`(replace NDIM by 2 or 3 and geo_file by the gmsh file located in the mesh sub-directory) - you can download Gmsh at http://gmsh.info/. You should also decompose the problem into multiple sub-domains to benefit from parallelism - for example, use `mpirun -c NCPUS flredecomp -v -l -i 1 -o NCPUS fluidity_file decomposed_file` (replace NCPUS by the number of sub-domains you want to create, fluidity_file by the flml file without including the extension, and decomposed_file by a filename of your choice, again without the extension). Finally, run the model using `mpirun -c NCPUS fluidity -v2 -l decomposed_file.flml`.

Once the model starts running, output files will be generated. In particular, finite element fields are stored in VTU format and particle fields in HDF5 format. You can use ParaView, available at https://www.paraview.org/download/, to visualise both types of output.
