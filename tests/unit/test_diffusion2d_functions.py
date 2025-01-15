"""
Tests for functions in class SolveDiffusion2D
"""

from diffusion2d import SolveDiffusion2D
import unittest
from unittest import TestCase

class TestDiffusion2D(TestCase):
    def setUp(self):
        # fixture
        self.data_domain = [25., 40., 0.25, 0.5]
        self.data_params = [10., 20., 1200., 10., 2.]
        self.data_condition = [1., 1., 10, 10, 300., 700.]

    def test_initialize_domain(self):
        """
        Check function SolveDiffusion2D.initialize_domain
        """
        solver = SolveDiffusion2D()
        w, h, dx, dy = self.data_domain

        # test
        solver.initialize_domain(w, h, dx, dy)
        self.assertEqual(solver.w, w)
        self.assertEqual(solver.h, h)
        self.assertEqual(solver.dx, dx)
        self.assertEqual(solver.dy, dy)
        self.assertIsInstance(solver.nx, int)
        self.assertEqual(solver.nx, 100)
        self.assertIsInstance(solver.ny, int)
        self.assertEqual(solver.ny, 80)

    def test_initialize_physical_parameters(self):
        """
        Checks function SolveDiffusion2D.initialize_physical_parameters
        """
        solver = SolveDiffusion2D()
        d, T_cold, T_hot, solver.dx, solver.dy = self.data_params
        solver.initialize_physical_parameters(d, T_cold, T_hot)
        expected_dt = 0.192308

        # test
        self.assertEqual(solver.D, d)
        self.assertEqual(solver.T_cold, T_cold)
        self.assertEqual(solver.T_hot, T_hot)
        self.assertAlmostEqual(solver.dt, expected_dt, 6)

    def test_set_initial_condition(self):
        """
        Check function SolveDiffusion2D.set_initial_condition
        """
        solver = SolveDiffusion2D()
        import numpy as np

        # Directly set necessary attributes
        solver.dx, solver.dy, solver.nx, solver.ny, solver.T_cold, solver.T_hot = self.data_condition

        # Parameters for the hot circle
        r, cx, cy = 2, 5, 5  # Radius and center of the hot circle
        r2 = r ** 2

        # Call the method to generate the computed grid
        computed_u = solver.set_initial_condition()

        # Generate the ground truth
        expected_u = solver.T_cold * np.ones((solver.nx, solver.ny))
        for i in range(solver.nx):
            for j in range(solver.ny):
                p2 = (i * solver.dx - cx) ** 2 + (j * solver.dy - cy) ** 2
                if p2 < r2:
                    expected_u[i, j] = solver.T_hot

        # Assert that the computed and expected grids are the same
        self.assertTrue(np.allclose(computed_u, expected_u))


if __name__ == "__main__":
    # Run the tests
    unittest.main()
