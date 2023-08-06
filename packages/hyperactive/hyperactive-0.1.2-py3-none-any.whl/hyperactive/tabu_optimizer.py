# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import tqdm

from .base import BaseOptimizer


class Tabu_Optimizer(BaseOptimizer):
    def __init__(
        self,
        search_space,
        n_iter,
        scoring="accuracy",
        tabu_memory=None,
        n_jobs=1,
        cv=5,
        verbosity=1,
        random_state=None,
        start_points=None,
    ):
        super().__init__(
            search_space,
            n_iter,
            scoring,
            tabu_memory,
            n_jobs,
            cv,
            verbosity,
            random_state,
            start_points,
        )
        self._search = self._start_evolution_strategy_optimizer

    def _start_tabu_optimizer(self, n_process):
        self._set_random_seed(n_process)
        n_steps = int(self.n_iter / self.n_jobs)

        for i in tqdm.tqdm(range(n_steps), position=n_process, leave=False):
            pass
