# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

"""
This module defines the InputGenerator classes that generate VaspInputSet
objects customized for specific types of calculations using parameters developed
and tested by the core team of pymatgen, including the Materials Project,
Materials Virtual Lab, and MIT high throughput project.

VASP InputGenerator classes are part of a 3-tiered hierarchy of pymatgen
clases for storing and writing calculation inputs.

1. An InputFile object represents the contents of a single input file, e.g.
   the INCAR
2. An InputSet is a dict-like container that maps filenames (keys) to file
   contents (either strings or InputFile objects)
3. InputGenerator classes implement a get_input_set method that, when provided
   with a structure, return an InputSet object with all parameters set correctly.
   Calculation input files can be written to disk with the write_inputs method.

If you want to implement a new InputGenerator, please take note of the following:

1. You must implement a get_input_set method that returns an InputSet
2. All customization of calculation parameters should be done in the __init__
   method of the InputGenerator. The idea is that the generator contains
   the "recipe" and get_input_set simply applies that recipe to a particular
   structure.
3. All InputGenerator must save all supplied args and kwargs as instance variables.
   E.g., self.my_arg = my_arg and self.kwargs = kwargs in the __init__. This
   ensures the as_dict and from_dict work correctly.
"""

from pathlib import Path

from pymatgen.io.core import InputGenerator
from pymatgen.io.vasp.sets import VaspInputSet

__author__ = "Alex Ganose, Ryan Kingsbury"
__email__ = "RKingsbury@lbl.gov"
__status__ = "Development"
__date__ = "November 2021"


MODULE_DIR = Path(__file__).resolve().parent


class MITRelaxGen(InputGenerator):
    """
    Generates a VaspInputSet for PBE structural relaxation with parameters used
    in the MIT High-throughput project.

    The parameters are chosen specifically for a high-throughput project,
    which means in general pseudopotentials with fewer electrons were chosen.

    Please refer::

        A Jain, G. Hautier, C. Moore, S. P. Ong, C. Fischer, T. Mueller,
        K. A. Persson, G. Ceder. A high-throughput infrastructure for density
        functional theory calculations. Computational Materials Science,
        2011, 50(8), 2295-2310. doi:10.1016/j.commatsci.2011.02.023
    """

    def get_input_set(self, structure=None) -> VaspInputSet:
        """
        Yield a VaspInputSet for a structure relaxation using settings employed by the MIT High-throughput project.
        """
        pass


class MPRelaxGen(InputGenerator):
    """
    Generates a VaspInputSet for PBE structural relaxation with parameters used in
    the public Materials Project database.

    Typically, the pseudopotentials chosen contain more electrons than the MIT
    parameters, and the k-point grid is ~50% more dense. The LDAUU parameters are
    also different due to the different psps used, which result in different fitted
    values.
    """

    def get_input_set(self, structure=None) -> VaspInputSet:
        """
        Yield a VaspInputSet for a structure relaxation using settings employed by the Materials Project.
        """
        pass


class MPScanRelaxGen(InputGenerator):
    """
    Generates a VaspInputSet for structure relaxation using the accurate and numerically
    efficient r2SCAN variant of the Strongly Constrained and Appropriately Normed
    (SCAN) metaGGA density functional. The parameters correspond to those adopted by
    the Materials Project database for high-throughput metaGGA calcluations.

    Notes:
        1. This functional is officially supported in VASP 6.0.0 and above. On older versions,
        source code may be obtained by contacting the authors of the referenced manuscript.
        The original SCAN functional, available from VASP 5.4.3 onwards, maybe used instead
        by passing `user_incar_settings={"METAGGA": "SCAN"}` when instantiating this InputSet.
        r2SCAN and SCAN are expected to yield very similar results for most properties
        (see Kingsbury et al. reference below).

        2. Meta-GGA calculations require POTCAR files that include
        information on the kinetic energy density of the core-electrons,
        i.e. "PBE_52" or "PBE_54". Make sure the POTCARs include the
        following lines (see VASP wiki for more details):

            $ grep kinetic POTCAR
            kinetic energy-density
            mkinetic energy-density pseudized
            kinetic energy density (partial)

    References:
         James W. Furness, Aaron D. Kaplan, Jinliang Ning, John P. Perdew, and Jianwei Sun.
         Accurate and Numerically Efficient r2SCAN Meta-Generalized Gradient Approximation.
         The Journal of Physical Chemistry Letters 0, 11 DOI: 10.1021/acs.jpclett.0c02405

         R. Kingsbury, A. Gupta, C. Bartel, J. Munro, S. Dwaraknath, M. Horton, and K. Persson,
         ChemRxiv (2021). https://doi.org/10.33774/chemrxiv-2021-gwm9m-v2
    """

    def __init__(self, **kwargs):
        """
        Args:
            vdw (str): set "rVV10" to enable SCAN+rVV10, which is a versatile
                    van der Waals density functional by combing the SCAN functional
                    with the rVV10 non-local correlation functional. rvv10 is the only
                    dispersion correction available for SCAN at this time.
            **kwargs: Same as those supported by DictSet, except for structure and
                config_dict. config_dict is set internally and structure is passed
                to the get_input_set method instead.
        """
        pass

    def get_input_set(self, structure=None, bandgap=0) -> VaspInputSet:
        """
        Args:
            structure (Structure): Input structure.
            bandgap (int): Bandgap of the structure in eV. The bandgap is used to
                    compute the appropriate k-point density and determine the
                    smearing settings.

                    Metallic systems (default, bandgap = 0) use a KSPACING value of 0.22
                    and Methfessel-Paxton order 2 smearing (ISMEAR=2, SIGMA=0.2).

                    Non-metallic systems (bandgap > 0) use the tetrahedron smearing
                    method (ISMEAR=-5, SIGMA=0.05). The KSPACING value is
                    calculated from the bandgap via Eqs. 25 and 29 of Wisesa, McGill,
                    and Mueller [1] (see References). Note that if 'user_incar_settings'
                    or 'user_kpoints_settings' override KSPACING, the calculation from
                    bandgap is not performed.
        """
        pass
