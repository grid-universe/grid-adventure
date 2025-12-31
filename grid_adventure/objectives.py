"""Objective functions for Grid Adventure environments."""

from grid_universe.objectives import (
    collect_and_exit_objective_fn as collect_and_exit_objective_fn,
)
from grid_universe.objectives import exit_objective_fn as exit_objective_fn


objectives = {
    "collect_and_exit": collect_and_exit_objective_fn,
    "exit": exit_objective_fn,
}
