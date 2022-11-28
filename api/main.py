from enum import Enum
from pydantic import BaseModel, Field

import numpy as np
from math import sqrt
from scipy.special import comb
from statsmodels.stats.power import tt_ind_solve_power, zt_ind_solve_power
from statsmodels.stats.proportion import proportion_effectsize

from fastapi import FastAPI

class Alternative(Enum):
    two_sided = "two-sided"
    larger = "larger"
    smaller = "smaller"

class SampleSizeBase(BaseModel):
    alpha: float = Field(..., ge = 0.0, le = 1.0)
    power: float = Field(..., ge = 0.0, le = 1.0)
    group: int = Field(..., ge = 0)
    lift: float = Field(..., ge = 0.0)
    alternative: Alternative

class SampleSizeAvg(SampleSizeBase):
    avg: float = Field(..., ge = 0.0)
    var: float = Field(..., ge = 0.0)

class SampleSizeRatio(SampleSizeBase):
    rate: float = Field(..., ge = 0.0, le = 1.0)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/stats/avg/samplesize/")
async def calc_sample_size(params: SampleSizeAvg):
    # OK: requests.post("http://127.0.0.1:8000/stats/avg/samplesize", json = {"avg": 1.0, "var": 1.0, "alpha": 0.05, "power": 0.8, "group": 2, "lift": 0.03, "alternative": "two-sided"})
    e_alpha = params.alpha / comb(params.group, 2)
    effect_size = params.lift * params.avg / sqrt(params.var)
    sample_size = tt_ind_solve_power(
        effect_size = effect_size,
        alpha = e_alpha,
        power = params.power,
        alternative = params.alternative.value
    )
    sample_size = 0.0 if type(sample_size) is np.ndarray else sample_size
    return {"params": params, "sample size": sample_size}

@app.post("/stats/ratio/samplesize/")
async def calc_sample_size(params: SampleSizeRatio):
    # OK: requests.post("http://127.0.0.1:8000/stats/ratio/samplesize", json = {"avg": 1.0, "var": 1.0, "alpha": 0.05, "power": 0.8, "group": 2, "lift": 0.03, "alternative": "two-sided"})
    e_alpha = params.alpha / comb(params.group, 2)
    effect_size = proportion_effectsize((1 + params.lift) * params.rate, params.rate)
    sample_size = zt_ind_solve_power(
            effect_size=effect_size,
            alpha=e_alpha,
            power=params.power,
            ratio=1 + params.lift,
            alternative=params.alternative.value,
        )
    sample_size = 0.0 if type(sample_size) is np.ndarray else sample_size
    return {"params": params, "sample size": sample_size}
