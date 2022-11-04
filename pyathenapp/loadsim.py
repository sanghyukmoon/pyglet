from athena_read import athdf, athinput
import xarray as xr
import numpy as np
from pathlib import Path
from matplotlib.colors import LogNorm

class LoadSim(object):
    """Class to prepare Athena++ simulation data analysis. Read input files and hdf5 outputs.

    Properties
    ----------
        basedir : str
            base directory of simulation output
        basename : str
            basename (tail) of basedir
        files : dict
            output file paths for athdf, hst, rst
        problem_id : str
            prefix for (athdf, hst, rst) output
        meta : dict
            simulation metadata (information in athinput file)
        nums : list of int
            athdf output numbers

    Methods
    -------
        load_athdf() :
            reads hdf5 file using athena_read and returns xarray object
    """

    def __init__(self, basedir):
        """Constructor for LoadSim class.

        Parameters
        ----------
        basedir : str
            Name of the directory where all data is stored
 
        """

        # Use pathlib.Path for handling file paths
        self.basedir = Path(basedir)
        self.basename = self.basedir.name
        
        # Find output files by matching glob patterns
        self.files = {}
        patterns = dict(athinput='athinput.*',
                        hst='*.hst',
                        athdf='*.athdf',
                        rst='*.rst') # add additional patterns here
        for key, pattern in patterns.items():
            self.files[key] = sorted(self.basedir.glob(pattern))

        # Get metadata from input file
        if len(self.files['athinput']) == 0:
            print("WARNING: found no input file")
        elif len(self.files['athinput']) > 1:
            print("WARNING: found more than one input file")
        else:
            self.files['athinput'] = self.files['athinput'][0]
            self.meta = athinput(self.files['athinput'])

        # TODO Get metadata from restart file
        # This will be useful for restart experiments that do not have
        # input file in their basedir.

        # Get problem_id from metadata
        self.problem_id = self.meta['job']['problem_id']

        # Unique history dump? if not, issue warning
        if len(self.files['hst']) == 0:
            print("WARNING: found no history dump")
        elif len(self.files['hst']) > 1:
            print("WARNING: found more than one history dumps")
        else:
            self.files['hst'] = self.files['hst'][0]

        # Find athdf output numbers
        self.nums = sorted(map(lambda x: int(x.name.strip('.athdf')[-5:]),
                               self.files['athdf']))

    def load_athdf(self, num=None):
        """Function to read Athena hdf5 file using athena_read
        return xarray object.

        Parameters
        ----------
        num : int
           Snapshot number, e.g., /basedir/problem_id.00042.athdf

        Returns
        -------
        dat : xarray object
        """

        # Find output_id of hdf5 files
        fname = self.files['athdf'][0].name
        idx = fname.find('.out')
        output_id = fname[idx+4]

        # Read athdf file using athena_read
        dat = athdf(self.basedir / '{}.out{}.{:05d}.athdf'.format(
                                    self.problem_id, output_id, num))
        
        # Convert to xarray object
        varnames = set(np.array(dat['VariableNames'], dtype=str))
        variables = [(['z', 'y', 'x'], dat[varname]) for varname in varnames]
        attr_keys = (set(dat.keys()) - varnames
                     - {'VariableNames','x1f','x2f','x3f','x1v','x2v','x3v'})
        attrs = {attr_key:dat[attr_key] for attr_key in attr_keys}
        ds = xr.Dataset(
            data_vars=dict(zip(varnames, variables)),
            coords=dict(x=dat['x1v'], y=dat['x2v'], z=dat['x3v']),
            attrs=attrs
        )
        return ds
