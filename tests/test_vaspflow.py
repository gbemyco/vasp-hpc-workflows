import tempfile
import unittest
from pathlib import Path

from vaspflow.parsers import parse_outcar
from vaspflow.thermo import hydrogen_adsorption_free_energy


class ParserTests(unittest.TestCase):
    def test_parse_last_energy_and_convergence(self):
        sample = """
 free  energy   TOTEN  =       -10.0000 eV
 aborting loop because EDIFF is reached
 FORCES: max atom, RMS = 0.031 0.010
 free  energy   TOTEN  =       -10.2500 eV
 reached required accuracy - stopping structural energy minimisation
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "OUTCAR"
            path.write_text(sample)
            result = parse_outcar(path)
        self.assertEqual(result.energy_ev, -10.25)
        self.assertEqual(result.max_force_ev_a, 0.031)
        self.assertTrue(result.electronic_converged)
        self.assertTrue(result.ionic_converged)

    def test_her_free_energy(self):
        value = hydrogen_adsorption_free_energy(-100.0, -103.45, -6.8, 0.04, 0.20)
        self.assertAlmostEqual(value, -0.21)


if __name__ == "__main__":
    unittest.main()
