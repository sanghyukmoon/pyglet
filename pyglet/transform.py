import numpy as np

def to_spherical(vec, origin):
    """Transform vector components from Cartesian to spherical coordinates

    Parameters
    ----------
    vec : tuple
        Cartesian vector components (vx, vy, vz)
    origin : tuple
        Origin of the spherical coordinates (x0, y0, z0)

    Returns
    -------
    vec_sph : tuple
        Spherical vector components (v_r, v_th, v_ph)
    """
    vx, vy, vz = vec
    x0, y0, z0 = origin
    x, y, z = vx.x, vx.y, vx.z
    # calculate spherical coordinates
    R = np.sqrt((x-x0)**2 + (y-y0)**2)
    r = np.sqrt(R**2 + (z-z0)**2)
    th = np.arctan2(R, z-z0)
    ph = np.arctan2(y-y0, x-x0)
    ph = ph.where(ph>=0, other=ph + 2*np.pi)
    sin_th, cos_th = R/r, (z-z0)/r
    sin_ph, cos_ph = (y-y0)/R, (x-x0)/R
    sin_th.loc[dict(x=x0,y=y0,z=z0)] = 0
    cos_th.loc[dict(x=x0,y=y0,z=z0)] = 0
    sin_ph.loc[dict(x=x0,y=y0)] = 0
    cos_ph.loc[dict(x=x0,y=y0)] = 0
    # transform vector components
    v_r = vx*sin_th*cos_ph + vy*sin_th*sin_ph + vz*cos_th
    v_th = vx*cos_th*cos_ph + vy*cos_th*sin_ph - vz*sin_th
    v_ph = -vx*sin_ph + vy*cos_ph
    # assign spherical coordinates
    v_r.coords['r'] = r
    v_th.coords['r'] = r
    v_ph.coords['r'] = r
    v_r.coords['th'] = th
    v_th.coords['th'] = th
    v_ph.coords['th'] = th
    v_r.coords['ph'] = ph
    v_th.coords['ph'] = ph
    v_ph.coords['ph'] = ph
    vec_sph = (v_r, v_th, v_ph)
    return vec_sph
