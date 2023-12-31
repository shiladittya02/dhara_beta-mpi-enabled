from grid import ncp,copy
import grid
from derivative import *
import h5py

# Setting arrays initially in each of the processes

if rank < nprocs - 1:
    # Velocity vector components
    ux = ncp.empty([grid.Nx+1,ndatz])
    uz = ncp.empty([grid.Nx+1,ndatz])

    # Scalar fields
    rho = ncp.empty([grid.Nx+1,ndatz])
    T = ncp.empty([grid.Nx+1,ndatz])

    # Conserved variables
    Q = ncp.empty([3,grid.Nx+1,ndatz])
    F = ncp.empty([3,grid.Nx+1,ndatz])

    temp = ncp.zeros([grid.Nx+1,ndatz])
else:
    # Velocity vector components
    ux = ncp.empty([grid.Nx+1,ndatz+1])
    uz = ncp.empty([grid.Nx+1,ndatz+1])

    # Scalar fields
    rho = ncp.empty([grid.Nx+1,ndatz+1])
    T = ncp.empty([grid.Nx+1,ndatz+1])

    # Conserved variables
    Q = ncp.empty([3,grid.Nx+1,ndatz+1])
    F = ncp.empty([3,grid.Nx+1,ndatz+1])

    temp = ncp.zeros([grid.Nx+1,ndatz+1])
def update_conserved():
    # Put the primitive variables inside Q's
    Q[0] = copy(rho)
    Q[1] = rho*ux
    Q[2] = rho*uz
    pass

def compute_convective_flux_x():
    # Convective flux terms in x-direction
    F[0] = rho*ux
    F[1] = rho*ux**2 + para.C*rho**para.gamma
    F[2] = rho*ux*uz
    pass

def compute_convective_flux_z():
    # Convective flux terms in z-direction
    F[0] = rho*uz
    F[1] = rho*ux*uz
    F[2] = rho*uz**2 + para.C*rho**para.gamma 
    pass

def flux_derivative_x():
    # Derivatives of total flux terms in x-direction
    F[0] = copy(dfx(F[0]))
    F[1] = copy(dfx(F[1]))
    F[2] = copy(dfx(F[2]))
    pass

def flux_derivative_z():
    # Derivatives of total flux terms in z-direction
    F[0] = copy(dfz(F[0]))
    F[1] = copy(dfz(F[1]))
    F[2] = copy(dfz(F[2]))
    pass


