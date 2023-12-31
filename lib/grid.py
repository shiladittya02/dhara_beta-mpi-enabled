import sys
from mpi_module import nprocs,rank,comm,buf,ndatz
sys.path.append("D:\HPC M.Sc. Project\dhara_beta-main 2")
from para import *

if device == 'CPU':
    import numpy as ncp
    from numpy import copy

else:
    import cupy as ncp
    from cupy import copy

    dev = ncp.cuda.Device(device_rank)
    dev.use()

# ----------------------------- Time variables ----------------------------- #

t = ncp.arange(tinit, tfinal + dt, dt)  # Time axis

Nf = int((tfinal - tinit) / t_f)  # Number of field saving times
t_f_step = ncp.linspace(tinit, tfinal, Nf + 1)  # Field saving times
t_f_step = ncp.insert(t_f_step, len(t_f_step), tfinal + dt)
Np = int((tfinal - tinit) / t_p)  # Number of energies and other parameters printing saving times
t_p_step = ncp.linspace(tinit, tfinal, Np + 1)  # Energies and other parameters printing saving times
t_p_step = ncp.insert(t_p_step, len(t_p_step), tfinal + dt)
#print(t_p_step)
# -------------------------------------------------------------------------- #

# ----------------------------- Grid variables ----------------------------- #

Lx = A * Lz  # Length of box in x-direction

dx = Lx / Nx  # Length between two consecutive grid points in x-direction
dz = Lz / Nz  # Length between two consecutive grid points in z-direction

if rank < nprocs - 1:
    X = ncp.arange(0, Nx+1) * dx  # Array consisting of points in x-direction
    Z = ncp.arange(rank * ndatz, (rank + 1) * ndatz) * dz  # Array consisting of points in z-direction
    X_mesh, Z_mesh = ncp.meshgrid(X, Z, indexing='ij')  # Meshgrids
    #print("Xmesh",X_mesh)
    #print("Zmesh",Z_mesh)
    temp_dx = ncp.zeros_like(X_mesh)  # Temporary array for derivatives calcualtion and other purposes
    temp_dz = ncp.zeros_like(Z_mesh)  # Temporary array for derivatives calcualtion and other purposes
else:
    X = ncp.arange(0, Nx+1) * dx  # Array consisting of points in x-direction
    Z = ncp.arange(rank * ndatz, ((rank + 1) * ndatz) + 1) * dz  # Array consisting of points in z-direction
    X_mesh, Z_mesh = ncp.meshgrid(X, Z, indexing='ij')  # Meshgrids
    #print("Xmesh", X_mesh)
    #print("Zmesh", Z_mesh)
    temp_dx = ncp.zeros_like(X_mesh)  # Temporary array for derivatives calcualtion and other purposes
    temp_dz = ncp.zeros_like(Z_mesh)
# -------------------------------------------------------------------------- #

# Printing parameters in output
if(rank==0):
    print('\n# Nz =', Nz, ', Nx =', Nx, ', dt =', dt, ', A =', A, ', gamma =', gamma, ', C =', C)
    print('\n \n# The following columns contains in order: dt, t, Total mass, Total kinetic energy, Total internal energy, Volume average V_rms, Maximum Mach number\n')