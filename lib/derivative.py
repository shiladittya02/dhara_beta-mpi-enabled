from grid import ncp,copy
import grid
from mpi_module import rank, nprocs, comm, buf, ndatz,ndatx
import sys
sys.path.append("..")

import para

def dfx(f):
    # sequential x-derivative (central difference method)
    # For peridoic f
    grid.temp_dx[1:-1,:] = (f[2:,:] - f[:-2,:])/(2*grid.dx)
    # Boundary terms when f is periodic in x
    grid.temp_dx[0,:] = (f[1,:] - f[-2,:])/(2*grid.dx)
    grid.temp_dx[-1,:] = copy(grid.temp_dx[0,:])
    return grid.temp_dx

if nprocs == 1:
    # sequential z-derivative (central difference method)
    def dfz(f):
        # Central difference of array 'f' w.r.t. z
        # For peridoic f
        grid.temp_dz[:,1:-1] = (f[:,2:] - f[:,:-2])/(2*grid.dz)
        # Boundary terms when f is periodic in z
        grid.temp_dz[:,0] = (f[:,1] - f[:,-2])/(2*grid.dz)
        grid.temp_dz[:,-1] = copy(grid.temp_dz[:,0])
        return grid.temp_dz
else:
    # mpi implemented z-derivative (central difference method)
    def dfz(f):
        if rank == 0:
            grid.temp_dz[:,1:-1] = (f[:,2:] - f[:,:-2])/(2*grid.dz)
            comm.Send(ncp.array(f[:, -1]), dest=(rank + 1), tag=int("1" + str(rank) + str(rank + 1)))
            comm.Recv(buf, source=(rank + 1), tag=int("1" + str(rank + 1) + str(rank)))
            grid.temp_dz[:,-1] = (buf - f[:,-2])/(2*grid.dz)
            comm.Send(ncp.array(f[:,1]), dest=(nprocs -1), tag=int("1"+str(rank)+str(nprocs-1)))
            comm.Recv(buf, source=(nprocs-1), tag=int("1"+str(nprocs-1)+str(rank)))
            grid.temp_dz[:,0] = buf
            return grid.temp_dz
        elif rank > 0 and rank < nprocs - 1:
            grid.temp_dz[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2 * grid.dz)
            comm.Send(ncp.array(f[:, -1]), dest=(rank + 1), tag=int("1" + str(rank) + str(rank + 1)))
            comm.Send(ncp.array(f[:, 0]), dest=(rank - 1), tag=int("1" + str(rank) + str(rank - 1)))
            comm.Recv(buf, source=(rank - 1), tag=int("1" + str(rank - 1) + str(rank)))
            grid.temp_dz[:,0] = (f[:,1] - buf)/(2*grid.dz)
            comm.Recv(buf, source=(rank + 1), tag=int("1" + str(rank + 1) + str(rank)))
            grid.temp_dz[:,-1] = (buf - f[:,-2])/(2*grid.dz)
            return grid.temp_dz
        elif rank == nprocs-1:
            grid.temp_dz[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2 * grid.dz)
            comm.Send(ncp.array(f[:,0]), dest=(rank-1), tag=int("1"+str(rank)+str(rank-1)))
            comm.Recv(buf, source=(rank - 1), tag=int("1" + str(rank - 1) + str(rank)))
            grid.temp_dz[:, 0] = (f[:,1] - buf)/(2*grid.dz)
            comm.Recv(buf, source=nprocs-nprocs, tag=int("1"+str(nprocs-nprocs)+str(nprocs-1)))
            grid.temp_dz[:, -1] = (buf - f[:,-2])/(2*grid.dz)
            comm.Send(ncp.array(grid.temp_dz[:, -1]), dest=nprocs-nprocs, tag=int("1"+str(nprocs-1)+str(nprocs-nprocs)))
            return grid.temp_dz

