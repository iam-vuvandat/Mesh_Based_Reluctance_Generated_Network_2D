MBGRN PROJECT

DESCRIPTION
MBGRN is a high performance Python solver for the electromagnetic analysis of electric motors. It utilizes a mesh based reluctance network with trapezoidal elements. This method serves as an efficient alternative to the Finite Element Method or FEM.

KEY FEATURES
Average computational speedup of 12.7 times compared to FEM.
Discrepancy is less than 1 percent for flux linkage and back EMF.
Cogging torque error is maintained below 6 percent.
Uses a unique index shifting technique for motion simulation.
Requires approximately half the number of elements used in FEM.
Trapezoidal elements in polar coordinates fit curved boundaries perfectly.

PROJECT STRUCTURE
core: Contains the main solver and mesh generation.
models: Defines motor geometry and material properties.
utils: Provides functions for index shifting and post processing.
main.py: The entry point to run simulations.

REQUIREMENTS
Python 3
Numpy
Scipy
Matplotlib

CITATION
Vu Van Dat et al. Development of the Mesh Based Generated Reluctance Network by Using Trapezoidal Elements Based on the Lumped Parameter Model. Przeglad Elektrotechniczny 2026.

CONTACT
Author: Vu Van Dat
Affiliation: Hanoi University of Science and Technology