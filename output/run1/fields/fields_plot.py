import h5py
import sys
import numpy as np
#sys.path.append("../output/run1/fields")
nprocs = 4
size= 1025
lag = size//nprocs
#size= 257
ux1 = np.empty([size,size], dtype=np.float64)
uz1 = np.empty([size,size], dtype=np.float64)
rho1 = np.empty([size,size], dtype=np.float64)
print("rho1: ", rho1.shape)

for i in range(nprocs):
    filename = f'2D_10.00proc {i}.h5'
    if i<3:
        f = h5py.File(filename,'r')
        rho1[:,i*lag:(i+1)*lag] = f['rho']
        ux1[:,i*lag:(i+1)*lag] = f['ux']
        uz1[:,i*lag:(i+1)*lag] = f['uz']
        print(i)
    else:
        f = h5py.File(filename, 'r')
        rho1[:, i * lag:(i + 1) * lag+1] = f['rho']
        ux1[:, i * lag:(i + 1) * lag+1] = f['ux']
        uz1[:, i * lag:(i + 1) * lag+1] = f['uz']
        print(i)


print("rho1: ", rho1.shape)
print("ux: ", rho1.shape)
print("uz1: ", rho1.shape)

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt



from mpl_toolkits.axes_grid1 import make_axes_locatable

ax = plt.subplot()
im = ax.imshow(rho1)

# create an Axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)

plt.colorbar(im, cax=cax)

plt.show()



# x and y axis
'''x = np.linspace(0, 2*np.pi, 129)
y = np.linspace(0, 2*np.pi, 129)

X, Y = np.meshgrid(x, y)

fig, axes = plt.subplots()

for ax in axes.flat:
    im = ax.imshow(rho1, vmin=0, vmax=1)

plt.colorbar(im, ax=axes.ravel().tolist())

plt.show()'''
'''fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y, Z, color='green')
ax.set_title('wireframe geeks for geeks')'''
plt.show()

# Vectorplot

# Meshgrid
x, y = np.meshgrid(np.linspace(0, 2*np.pi, size),
                   np.linspace(0, 2*np.pi, size))

# Directional vectors
u = ux1
v = uz1

# Plotting Vector Field with QUIVER
#plt.quiver(x, y, u, v, color='g', scale=1)
plt.streamplot(x,y,u,v, density=1.4, linewidth=None, color='#A23BEC')
plt.title('Vector Field')

# Setting x, y boundary limits
'''plt.xlim(-7, 7)
plt.ylim(-7, 7)'''

# Show plot with grid
plt.grid()
plt.show()