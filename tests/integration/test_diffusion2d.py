"""
Tests for functionality checks in class SolveDiffusion2D
"""

from diffusion2d import SolveDiffusion2D
import pytest

def test_initialize_physical_parameters():
    """
    Checks function SolveDiffusion2D.initialize_domain
    """
    solver = SolveDiffusion2D()
    
    # fixture
    w, h, dx, dy = [25., 40., 10., 2.]
    solver.initialize_domain(w, h, dx, dy)
    d, T_cold, T_hot = [10., 20., 1200.]
    solver.initialize_physical_parameters(d, T_cold, T_hot)
    expected_dt = pytest.approx(0.192308,abs=1e-6)
    assert expected_dt == solver.dt


def test_set_initial_condition():
    """
    Check function SolveDiffusion2D.set_initial_condition
    """
    solver = SolveDiffusion2D()
    import numpy as np

    # Directly set necessary attributes
    solver.dx, solver.dy, solver.nx, solver.ny, solver.T_cold, solver.T_hot = [0.1,0.3,100,130,30.,897]

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
    assert np.allclose(computed_u, expected_u)
    
