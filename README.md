# 2d_flow_mpi_dhara_beta
## - MPI enabled beta version of DHARA Compressible Flow Solver 

- The base sequential code (GPU enabled), `dhara_beta`, was developed by @harshitiwari.
- This is an MPI and GPU enabled Python code which solves fully compressible equations for polytropic fluid in 2D Cartesian box.  

### Instructions to run the code:
1. `para.py` contains the control parameters. 
  - Change the device type (GPU/CPU) using `device` and its rank.
  - For CPU, the rank in the `para.py` file need not be changed. Set the no. of processes in the `terminal`.
  - Set the output directory and path using `output_dir`. 
  - You can change the time advance scheme from `Scheme`.
  - Put the grid parameters and control parameters.
2. To execute the solver run `main.py` using Python. You can save the output in a text file using one of the following commands:
  - Windows MPI: ` .\mpiexec -n 'no. of procs' py main.py`
  - Linux sequential: `python3 main.py`
  - Linux MPI: `mpirun -np 'no. of procs' main.py`
