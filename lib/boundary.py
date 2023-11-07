import grid
import compressible as cs

import sys
import mpi_module as mp
sys.path.append("..")
import para

def imposeBC_u():
    # Boundary condition for velocity fields
    cs.ux[0,:] = cs.ux[-1,:]
    cs.uz[0,:] = cs.uz[-1,:]

    if mp.rank == (mp.nprocs-mp.nprocs) and mp.nprocs>1:
        mp.comm.Recv(mp.buf, source=mp.nprocs-1, tag=int("1"+str(mp.nprocs-1)+str(mp.nprocs-mp.nprocs)+"1"))
        cs.ux[:, 0] = mp.buf
        mp.comm.Recv(mp.buf, source=mp.nprocs - 1, tag=int("1" + str(mp.nprocs - 1) + str(mp.nprocs - mp.nprocs) + "2"))
        cs.uz[:, 0] = mp.buf
    elif mp.rank == (mp.nprocs-1) and mp.nprocs>1:
        mp.comm.Send(grid.ncp.array(cs.ux[:,-1]), dest=mp.nprocs-mp.nprocs, tag=int("1"+str(mp.nprocs-1)+str(mp.nprocs-mp.nprocs)+"1"))
        #cs.ux[:,-1] = mp.buf
        mp.comm.Send(grid.ncp.array(cs.uz[:,-1]), dest=mp.nprocs-mp.nprocs, tag=int("1" + str(mp.nprocs - 1) + str(mp.nprocs - mp.nprocs) + "2"))
        #cs.uz[:,-1] = mp.buf
    elif mp.nprocs==1:
        cs.ux[:, 0] = cs.ux[:, -1]
        cs.uz[:, 0] = cs.uz[:, -1]
    pass

def imposeBC_rho():
    # Boundary condition for density
    cs.rho[0,:] = cs.rho[-1,:]
    if mp.rank == (mp.nprocs - mp.nprocs) and mp.nprocs > 1:
        mp.comm.Recv(mp.buf, source=mp.nprocs - 1, tag=int("1" + str(mp.nprocs - 1) + str(mp.nprocs - mp.nprocs) + "3"))
        cs.rho[:, 0] = mp.buf
    elif mp.rank == (mp.nprocs - 1) and mp.nprocs > 1:
        mp.comm.Send(grid.ncp.array(cs.rho[:, -1]), dest=mp.nprocs - mp.nprocs, tag=int("1" + str(mp.nprocs - 1) + str(mp.nprocs - mp.nprocs) + "3"))
    elif mp.nprocs == 1:
        cs.rho[:, 0] = cs.rho[:, -1]
    pass

def boundary():
    imposeBC_rho()
    imposeBC_u()
    pass
