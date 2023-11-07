import numpy as np
from mpi4py import MPI
import sys
sys.path.append("..")
import para

#setting up MPI environment and communicator
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()
ndatz = para.Nz//nprocs
ndatx = para.Nx//nprocs
buf = np.empty(para.Nz+1, dtype=np.float64)