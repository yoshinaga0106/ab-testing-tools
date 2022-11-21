from dataclasses import dataclass


@dataclass
class Metrics:
    alpha: float
    e_alpha: float
    pvalue: float
    is_significant: bool

    def get_metrics(self):
        return {
            "alpha": self.alpha,
            "e_alpha": self.e_alpha,
            "pvalue": self.pvalue,
            "is_significant": self.is_significant,
        }
