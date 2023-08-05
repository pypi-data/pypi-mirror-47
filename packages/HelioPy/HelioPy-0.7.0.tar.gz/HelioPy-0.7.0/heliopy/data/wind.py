"""
Methods for importing data from the WIND spacecraft.
All data is publically available at ftp://spdf.gsfc.nasa.gov/pub/data/wind.
See https://wind.nasa.gov/data_sources.php for more information on different
data products.
"""
from collections import OrderedDict
import datetime as dt
import pathlib as path
import warnings

import astropy.units as u
import cdflib
import numpy as np
import pandas as pd

from heliopy.data import cdasrest
from heliopy.data import util
from heliopy import config

data_dir = path.Path(config['download_dir'])
wind_dir = data_dir / 'wind'
use_hdf = config['use_hdf']
remote_wind_dir = 'ftp://spdf.gsfc.nasa.gov/pub/data/wind/'


def _docstring(identifier, description):
    return cdasrest._docstring(identifier, 'W', description)


def _wind(starttime, endtime, identifier, units=None, badvalues=None):
    """
    Generic method for downloading ACE data.
    """
    dataset = 'wi'
    return cdasrest._process_cdas(starttime, endtime, identifier, dataset,
                                  wind_dir,
                                  units=units,
                                  badvalues=badvalues)


# Actual download functions start here
def swe_h1(starttime, endtime):
    identifier = 'WI_H1_SWE'
    badvalues = 99999.9
    units = {'ChisQ_DOF_nonlin': u.dimensionless_unscaled}
    return _wind(starttime, endtime, identifier,
                 badvalues=badvalues, units=units)


swe_h1.__doc__ = _docstring(
    'WI_H1_SWE', '92-second Solar Wind Alpha and Proton Anisotropy Analysis')


def mfi_h0(starttime, endtime):
    identifier = 'WI_H0_MFI'
    return _wind(starttime, endtime, identifier)


mfi_h0.__doc__ = _docstring(
    'WI_H0_MFI', 'Composite magnetic field')


def mfi_h2(starttime, endtime):
    identifier = 'WI_H2_MFI'
    return _wind(starttime, endtime, identifier)


mfi_h2.__doc__ = _docstring(
    'WI_H2_MFI', 'High resolution magnetic field')


def threedp_pm(starttime, endtime):
    identifier = 'WI_PM_3DP'
    return _wind(starttime, endtime, identifier)


threedp_pm.__doc__ = _docstring(
    'WI_PM_3DP', '1 spin resolution ion (proton and alpha) moment')


def threedp_e0_emfits(starttime, endtime):
    identifier = 'WI_EMFITS_E0_3DP'
    return _wind(starttime, endtime, identifier)


threedp_e0_emfits.__doc__ = _docstring(
    'WI_EMFITS_E0_3DP', 'Electron moment')
