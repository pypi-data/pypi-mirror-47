# Licensed under a 3-clause BSD style license - see LICENSE.rst
# (taken from photutils: should probably migrate into astropy.wcs)
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from astropy import units as u
from astropy.coordinates import UnitSphericalRepresentation
from astropy.wcs.utils import skycoord_to_pixel
from ..core.pixcoord import PixCoord

skycoord_to_pixel_mode = 'all'


def skycoord_to_pixel_scale_angle(skycoord, wcs, small_offset=1 * u.arcsec):
    """
    Convert a set of SkyCoord coordinates into pixel coordinates, pixel
    scales, and position angles.

    Parameters
    ----------
    skycoord : `~astropy.coordinates.SkyCoord`
        Sky coordinates
    wcs : `~astropy.wcs.WCS`
        The WCS transformation to use
    small_offset : `~astropy.units.Quantity`
        A small offset to use to compute the angle

    Returns
    -------
    pixcoord : `~regions.PixCoord`
        Pixel coordinates
    scale : float
        The pixel scale at each location, in degrees/pixel
    angle : `~astropy.units.Quantity`
        The position angle of the celestial coordinate system in pixel space.
    """

    # Convert to pixel coordinates
    x, y = skycoord_to_pixel(skycoord, wcs, mode=skycoord_to_pixel_mode)
    pixcoord = PixCoord(x=x, y=y)

    # We take a point directly 'above' (in latitude) the position requested
    # and convert it to pixel coordinates, then we use that to figure out the
    # scale and position angle of the coordinate system at the location of
    # the points.

    # Find the coordinates as a representation object
    r_old = skycoord.represent_as('unitspherical')

    # Add a a small perturbation in the latitude direction (since longitude
    # is more difficult because it is not directly an angle).
    dlat = small_offset
    r_new = UnitSphericalRepresentation(r_old.lon, r_old.lat + dlat)
    coords_offset = skycoord.realize_frame(r_new)

    # Find pixel coordinates of offset coordinates
    x_offset, y_offset = skycoord_to_pixel(coords_offset, wcs,
                                           mode=skycoord_to_pixel_mode)

    # Find vector
    dx = x_offset - x
    dy = y_offset - y

    # Find the length of the vector
    scale = np.hypot(dx, dy) / dlat.to('degree').value

    # Find the position angle
    angle = np.arctan2(dy, dx) * u.radian

    return pixcoord, scale, angle


def assert_angle_or_pixel(name, q):
    """
    Check that ``q`` is either an angular or a pixel `~astropy.units.Quantity`.
    """
    if isinstance(q, u.Quantity):
        if q.unit.physical_type == 'angle' or q.unit is u.pixel:
            pass
        else:
            raise ValueError("{0} should have angular or pixel "
                             "units".format(name))
    else:
        raise TypeError("{0} should be a Quantity instance".format(name))


def assert_angle(name, q):
    """
    Check that ``q`` is an angular `~astropy.units.Quantity`.
    """
    if isinstance(q, u.Quantity):
        if q.unit.physical_type == 'angle':
            pass
        else:
            raise ValueError("{0} should have angular units".format(name))
    else:
        raise TypeError("{0} should be a Quantity instance".format(name))
