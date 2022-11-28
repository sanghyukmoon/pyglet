# pyglet
Minimal package for converting athena++ hdf5 output into xarray dataset

## Quickstart
* Setup conda environment
  ```
  cd /path/to/pyglet
  conda env create -f env.yml
  conda activate pyglet
  ```
* Load metadata (problem id, mesh info, etc.) of your simulation and setup file paths
  ```
  from pyglet.loadsim import LoadSim
  s = LoadSim('/path/to/simulation/directory/model')
  
  s.basedir    # '/path/to/simulation/directory/model'
  s.basename   # 'model'
  s.meta       # dictionary containing simulation metadata (including those in athinput file)
  s.files      # dictionary containing file paths of simulation outputs
  s.problem_id # drefix of your simulation (e.g., shock_tube for shock_tube.out2.00042.athdf)
  ```
* Read history dump
  ```
  hst = s.load_hst()        # reads s.files['hst']
  plt.plot(hst.t, hst.mass) # plot total mass evolution
  ```
* Read hdf5 output
  ```
  from matplotlib.colors import LogNorm
  dat = s.load_athdf(42) # reads [basedir]/[problem_id].out?.00042.athdf
  dat.dens.sel(z=0, method='nearest').plot.imshow(norm=LogNorm()) # plot midplane density
  ```

## Xarray tutorial
* We use `xarray` to store both history and hdf5 data. `xarray` enables coordinate indexing as well as usual numpy-like indexing.
  ```
  dat = s.load_athdf(42)
  dat.interp(x=0, y=-1.2, z=2.3)                # (x,y,z) = (0,-1.2,2.3) by interpolating from neighboring cells
  dat.sel(x=0, y=-1.2, z=2.3, method='nearest') # nearest grid cell from the point (x,y,z) = (0,-1.2,2.3)
  dat.isel(x=0, y=1, z=4)                       # (i,j,k) = (0,1,4)
  ```
