# pyathenapp
Minimal package for converting athena++ hdf5 output into xarray dataset

## Basic Usage
Suppose you ran a simulation in a directory `/scratch/user/shock01`
```
$ls /scratch/user/shock01
athena
athinput.sod
shock_tube.hst
shock_tube.out2.00000.athdf
shock_tube.out2.00001.athdf
...
shock_tube.00000.rst
shock_tube.final.rst
...
```
You can read output by doing
```
from pyathenapp.loadsim import LoadSim
# load simulation, find output files
s = LoadSim('/scratch/user/shock01')
s.problem_id          # 'shock_tube'
s.basename            # 'shock01'
s.basedir             # '/scratch/user/shock01'
s.files               # dictionary containing all output files
s.nums                # output numbers of all hdf5 files
dat = s.load_athdf(7) # reads problem.out2.00007.athdf and convert it to xarray dataset
(dat.dens*dat.dz).sum(dim='z').plot.imshow() # plot surface density map
for num in s.nums:
    dat = s.load_athdf(num)
    # loop through all outputs and post-process
    ...
```
