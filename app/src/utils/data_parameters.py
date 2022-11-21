from dataclasses import dataclass, field
from typing import List


@dataclass
class BaseData:
    alpha: float = 0.05
    power: float = 0.8
    group: int = 2
    alternative: str = "two-sided"
    lifts: List[float] = field(default_factory=list)

    def get_options(self):
        return {"alpha": self.alpha, "power": self.power, "alternative": self.alternative, "lifts": self.lifts}


@dataclass
class AvgData(BaseData):
    avg: float = 100.0
    var: float = 100.0
    sample: float = 10000.0

    def get_default_inputs(self):
        return {"avg": self.avg, "var": self.var, "sample": self.sample, "group": self.group}


@dataclass
class RatioData(BaseData):
    rate: float = 0.1
    sample: float = 10000.0

    def get_default_inputs(self):
        return {"rate": self.rate, "sample": self.sample, "group": self.group}
