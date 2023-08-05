"""
pyDiffusion combines tools like diffusion simulation, diffusion data smooth,
forward simulation analysis (FSA), etc. to help people analyze diffusion data
efficiently.
"""
__version__ = '0.2.1'


from pydiffusion.core import DiffProfile, DiffSystem
from pydiffusion.simulation import mphSim
from pydiffusion.smooth import datasmooth
from pydiffusion.plot import profileplot, DCplot, SFplot
from pydiffusion.utils import matanocalc, mesh, step
from pydiffusion.Dtools import SF, Hall, Dmodel, FSA
from pydiffusion.io import read_csv, save_csv
