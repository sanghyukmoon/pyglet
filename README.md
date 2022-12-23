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
  - Using xarray
  ```
  from matplotlib.colors import LogNorm
  ds = s.load_athdf(42) # reads [basedir]/[problem_id].out?.00042.athdf
  ds.dens.sel(z=0, method='nearest').plot.imshow(norm=LogNorm()) # plot midplane density
  ```
  - Using yt
  ```
  ds = s.load_athdf(42, load_method='yt')
  ```
  - When you have multiple hdf5 outputs
  ```
  'output2': {'file_type': 'hdf5', 'variable': 'prim', 'dt': 0.01},
  'output3': {'file_type': 'hdf5', 'variable': 'uov', 'dt': 0.01},
  ```
  you can use `output_id` parameter to specify which one to read
  ```
  ds = s.load_athdf(42, output_id=2, load_method='yt')
  uov = s.load_athdf(42, output_id=3, load_method='xarray')
  ```

## Xarray tutorial
* `xarray` enables coordinate indexing as well as usual numpy-like indexing.
  ```
  ds = s.load_athdf(42)
  ds.interp(x=0, y=-1.2, z=2.3)                # (x,y,z) = (0,-1.2,2.3) by interpolating from neighboring cells
  ds.sel(x=0, y=-1.2, z=2.3, method='nearest') # nearest grid cell from the point (x,y,z) = (0,-1.2,2.3)
  ds.isel(x=0, y=1, z=4)                       # (i,j,k) = (0,1,4)
  ```
