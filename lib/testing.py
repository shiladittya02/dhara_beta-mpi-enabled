'''import boundary
import compressible as cs
from derivative import dfz
from mpi_module import rank
import sys
sys.path.append("..\input")
import init_fields

init_fields.init_fields()
boundary.boundary()
a = dfz(cs.ux)
#b = dfz(cs.ux)
print("mpi: ", rank, "\n", a)
#print("sequence: ", rank, "\n", b)'''