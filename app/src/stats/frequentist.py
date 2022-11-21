from dataclasses import dataclass
from typing import List

from statsmodels.stats.proportion import proportions_chisquare, proportions_ztest
from statsmodels.stats.weightstats import ttest_ind

from src.stats.sample_size import SampleSizeBase
from src.utils.models import Metrics


@dataclass
class FreqTTest(SampleSizeBase):
    c: List[float]
    t: List[float]

    def get_pvalue(self):
        # t-test
        _, pvalue, _ = ttest_ind(
            x1=self.c,
            x2=self.t,
            alternative=self.alternative,
        )
        return pvalue

    def check_significance(self):
        e_alpha = self._calc_effective_alpha()
        pvalue = self.get_pvalue()
        return Metrics(alpha=self.alpha, e_alpha=e_alpha, pvalue=pvalue, is_significant=pvalue < e_alpha).get_metrics()


@dataclass
class FreqZTest(SampleSizeBase):
    yes: List[float]
    no: List[float]

    def get_pvalue(self):
        # z-test
        _, pvalue = proportions_ztest(
            count=self.yes,
            nobs=[x + y for (x, y) in zip(self.yes, self.no)],
            alternative=self.alternative,
        )
        return pvalue

    def check_significance(self):
        e_alpha = self._calc_effective_alpha()
        pvalue = self.get_pvalue()
        return Metrics(alpha=self.alpha, e_alpha=e_alpha, pvalue=pvalue, is_significant=pvalue < e_alpha).get_metrics()


@dataclass
class FreqChisqTest(SampleSizeBase):
    yes: List[float]
    no: List[float]

    def get_pvalue(self):
        # chisq-test
        _, pvalue, _ = proportions_chisquare(
            count=self.yes,
            nobs=[x + y for (x, y) in zip(self.yes, self.no)],
        )
        return pvalue

    def check_significance(self):
        e_alpha = self._calc_effective_alpha()
        pvalue = self.get_pvalue()
        return Metrics(alpha=self.alpha, e_alpha=e_alpha, pvalue=pvalue, is_significant=pvalue < e_alpha).get_metrics()
