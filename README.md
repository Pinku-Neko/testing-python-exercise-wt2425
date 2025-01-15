# Python code to solve the diffusion equation in 2D

Please follow the instructions in [python_testing_exercise.md](https://github.com/Simulation-Software-Engineering/Lecture-Material/blob/main/05_testing_and_ci/python_testing_exercise.md).

## Test logs (for submission)

### pytest log
```

tests\integration\test_diffusion2d.py ..                                                                                      [ 40%] 
tests\unit\test_diffusion2d_functions.py F..                                                                                  [100%]

============================================================= FAILURES ============================================================= 
______________________________________________________ test_initialize_domain ______________________________________________________ 

    def test_initialize_domain():
        """
        Check function SolveDiffusion2D.initialize_domain
        """
        solver = SolveDiffusion2D()
        # fixture
        w = 25.
        h = 40.
        dx = 0.25
        dy = 0.5

        # test
        solver.initialize_domain(w, h, dx, dy)
        assert solver.w == w
        assert solver.h == h
        assert solver.dx == dx
        assert solver.dy == dy
>       assert (solver.nx == 100) and (isinstance(solver.nx, int))
E       assert (160 == 100)
E        +  where 160 = <diffusion2d.SolveDiffusion2D object at 0x0000019D97399E10>.nx

tests\unit\test_diffusion2d_functions.py:26: AssertionError
===================================================== short test summary info ====================================================== 
FAILED tests/unit/test_diffusion2d_functions.py::test_initialize_domain - assert (160 == 100)
=================================================== 1 failed, 4 passed in 0.40s ====================================================

```
### unittest log
```
Fdt = 192.30769230769232
FF
======================================================================
FAIL: test_initialize_domain (tests.unit.test_diffusion2d_functions.TestDiffusion2D)
Check function SolveDiffusion2D.initialize_domain
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\SSM\exercise\testing-python-exercise-wt2425\tests\unit\test_diffusion2d_functions.py", line 32, in test_initialize_domain 
    self.assertEqual(solver.ny, 80)
AssertionError: 50 != 80

======================================================================
FAIL: test_initialize_physical_parameters (tests.unit.test_diffusion2d_functions.TestDiffusion2D)
Checks function SolveDiffusion2D.initialize_physical_parameters
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\SSM\exercise\testing-python-exercise-wt2425\tests\unit\test_diffusion2d_functions.py", line 47, in test_initialize_physical_parameters
    self.assertAlmostEqual(solver.dt, expected_dt, 6)
AssertionError: 192.30769230769232 != 0.192308 within 6 places (192.11538430769232 difference)

======================================================================
FAIL: test_set_initial_condition (tests.unit.test_diffusion2d_functions.TestDiffusion2D)
Check function SolveDiffusion2D.set_initial_condition
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\SSM\exercise\testing-python-exercise-wt2425\tests\unit\test_diffusion2d_functions.py", line 75, in test_set_initial_condition
    self.assertTrue(np.allclose(computed_u, expected_u))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 3 tests in 0.002s

FAILED (failures=3)
```

## integration test log

```
======================================================= test session starts ========================================================
platform win32 -- Python 3.10.11, pytest-8.3.4, pluggy-1.5.0
rootdir: D:\SSM\exercise\testing-python-exercise-wt2425
collected 2 items

tests\integration\test_diffusion2d.py FF                                                                                      [100%]

============================================================= FAILURES ============================================================= 
_______________________________________________ test_initialize_physical_parameters ________________________________________________ 

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
>       assert expected_dt == solver.dt
E       assert 0.192308 ± 1.0e-06 == 1.1923076923076923
E
E         comparison failed
E         Obtained: 1.1923076923076923
E         Expected: 0.192308 ± 1.0e-06

tests\integration\test_diffusion2d.py:20: AssertionError
------------------------------------------------------- Captured stdout call ------------------------------------------------------- 
dt = 1.1923076923076923
____________________________________________________ test_set_initial_condition ____________________________________________________ 

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
>       assert np.allclose(computed_u, expected_u)
E       AssertionError: assert False
E        +  where False = <function allclose at 0x000001F6FE148A70>(array([[30., 30., 30., ..., 30., 30., 30.],\n       [30., 30., 30., ..., 30., 30., 30.],\n       [30., 30., 30., ..., 30..., 30., 30.],\n       [30., 30., 30., ..., 30., 30., 30.],\n       [30., 30., 30., ..., 30., 30., 30.]], shape=(100, 130)), array([[30., 30., 30., ..., 30., 30., 30.],\n       [30., 30., 30., ..., 30., 30., 30.],\n       [30., 30., 30., ..., 30..., 30., 30.],\n       [30., 30., 30., ..., 30., 30., 30.],\n       [30., 30., 30., ..., 30., 30., 30.]], shape=(100, 130)))
E        +    where <function allclose at 0x000001F6FE148A70> = <module 'numpy' from 'd:\\SSM\\exercise\\testing-python-exercise-wt2425\\.venv\\lib\\site-packages\\numpy\\__init__.py'>.allclose

tests\integration\test_diffusion2d.py:49: AssertionError
===================================================== short test summary info ====================================================== 
FAILED tests/integration/test_diffusion2d.py::test_initialize_physical_parameters - assert 0.192308 ± 1.0e-06 == 1.1923076923076923  
FAILED tests/integration/test_diffusion2d.py::test_set_initial_condition - AssertionError: assert False
======================================================== 2 failed in 0.43s =========================================================
```

## Citing

The code used in this exercise is based on [Chapter 7 of the book "Learning Scientific Programming with Python"](https://scipython.com/book/chapter-7-matplotlib/examples/the-two-dimensional-diffusion-equation/).
