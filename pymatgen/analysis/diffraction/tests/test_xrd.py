# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

import unittest

import pytest

from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
from pymatgen.util.testing import PymatgenTest

"""
TODO: Modify unittest doc.
"""

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "5/22/14"


class XRDCalculatorTest(PymatgenTest):
    def test_type_wavelength(self):
        """Test TypeError is raised if wavelength is unaccepted type"""
        wavelength = [1.78, 2.78]  # just a list
        with pytest.raises(TypeError):
            XRDCalculator(wavelength)

    def test_get_pattern(self):
        s = self.get_structure("CsCl")
        c = XRDCalculator()
        xrd = c.get_pattern(s, two_theta_range=(0, 90))
        assert xrd.to_json()  # Test MSONAble property
        # Check the first two peaks
        assert xrd.x[0] == pytest.approx(21.107738329639844)
        assert xrd.y[0] == pytest.approx(36.483184003748946)
        assert xrd.hkls[0] == [{"hkl": (1, 0, 0), "multiplicity": 6}]
        assert xrd.d_hkls[0] == pytest.approx(4.2089999999999996)
        assert xrd.x[1] == pytest.approx(30.024695921112777)
        assert xrd.y[1] == pytest.approx(100)
        assert xrd.hkls[1] == [{"hkl": (1, 1, 0), "multiplicity": 12}]
        assert xrd.d_hkls[1] == pytest.approx(2.976212442014178)

        s = self.get_structure("LiFePO4")
        xrd = c.get_pattern(s, two_theta_range=(0, 90))
        assert xrd.x[1] == pytest.approx(17.03504233621785)
        assert xrd.y[1] == pytest.approx(50.400928948337075)

        s = self.get_structure("Li10GeP2S12")
        xrd = c.get_pattern(s, two_theta_range=(0, 90))
        assert xrd.x[1] == pytest.approx(14.058274883353876)
        assert xrd.y[1] == pytest.approx(4.4111123641667671)

        # Test a hexagonal structure.
        s = self.get_structure("Graphite")

        xrd = c.get_pattern(s, two_theta_range=(0, 90))
        assert xrd.x[0] == pytest.approx(26.21057350859598)
        assert xrd.y[0] == pytest.approx(100)
        assert len(xrd.hkls[0][0]["hkl"]) == pytest.approx(4)

        # Add test case with different lengths of coefficients.
        # Also test d_hkl.
        coords = [
            [0.25, 0.25, 0.173],
            [0.75, 0.75, 0.827],
            [0.75, 0.25, 0],
            [0.25, 0.75, 0],
            [0.25, 0.25, 0.676],
            [0.75, 0.75, 0.324],
        ]
        sp = ["Si", "Si", "Ru", "Ru", "Pr", "Pr"]
        s = Structure(Lattice.tetragonal(4.192, 6.88), sp, coords)
        xrd = c.get_pattern(s)
        assert xrd.x[0] == pytest.approx(12.86727341476735)
        assert xrd.y[0] == pytest.approx(31.448239816769796)
        assert xrd.d_hkls[0] == pytest.approx(6.88)
        assert len(xrd) == 42
        xrd = c.get_pattern(s, two_theta_range=[0, 60])
        assert len(xrd) == 18

        # Test with and without Debye-Waller factor
        tungsten = Structure(Lattice.cubic(3.1653), ["W"] * 2, [[0, 0, 0], [0.5, 0.5, 0.5]])
        xrd = c.get_pattern(tungsten, scaled=False)
        assert xrd.x[0] == pytest.approx(40.294828554672264)
        assert xrd.y[0] == pytest.approx(2414237.5633093244)
        assert xrd.d_hkls[0] == pytest.approx(2.2382050944897789)
        c = XRDCalculator(debye_waller_factors={"W": 0.1526})
        xrd = c.get_pattern(tungsten, scaled=False)
        assert xrd.x[0] == pytest.approx(40.294828554672264)
        assert xrd.y[0] == pytest.approx(2377745.2296686019)
        assert xrd.d_hkls[0] == pytest.approx(2.2382050944897789)


if __name__ == "__main__":
    unittest.main()
