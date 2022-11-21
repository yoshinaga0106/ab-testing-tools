from dataclasses import dataclass
from math import sqrt

import numpy as np
from scipy.special import comb
from statsmodels.stats.power import tt_ind_solve_power, zt_ind_solve_power
from statsmodels.stats.proportion import proportion_effectsize


@dataclass
class SampleSizeBase:
    alpha: float
    power: float
    group: int
    lift: float
    alternative: str

    def _calc_effective_alpha(self):
        return self.alpha / comb(self.group, 2)


@dataclass
class SampleSizeAvg(SampleSizeBase):
    avg: float
    var: float

    def _calc_effect_size(self):
        # cohen d: abs(mu1 - mu2) / sqrt(var)
        return self.lift * self.avg / sqrt(self.var)

    def calc_sample_size(self):
        # t-test
        n = tt_ind_solve_power(
            effect_size=self._calc_effect_size(),
            alpha=self._calc_effective_alpha(),
            power=self.power,
            alternative=self.alternative,
        )
        # we need to care if the solution does not converge
        # see https://github.com/statsmodels/statsmodels/issues/4022
        return 0.0 if type(n) is np.ndarray else n


@dataclass
class SampleSizeRatio(SampleSizeBase):
    rate: float

    def _calc_effect_size(self):
        # 2 * (arcsin(sqrt(p1)) - arcsin(sqrt(p2)))
        return proportion_effectsize((1 + self.lift) * self.rate, self.rate)

    def calc_sample_size(self):
        # z-test
        n = zt_ind_solve_power(
            effect_size=self._calc_effect_size(),
            alpha=self._calc_effective_alpha(),
            power=self.power,
            ratio=1 + self.lift,
            alternative=self.alternative,
        )
        # we need to care if the solution does not converge
        # see https://github.com/statsmodels/statsmodels/issues/4022
        return 0.0 if type(n) is np.ndarray else n
