from enum import Enum
from pydantic import BaseModel, Field

from math import sqrt
from statsmodels.stats.power import tt_ind_solve_power 
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
    # TODO str -> Alternative
    alternative: str


class SampleSizeAvg(SampleSizeBase):
    avg: float = Field(..., ge = 0.0)
    var: float = Field(..., ge = 0.0)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/stats/avg")
async def calc_sample_size(params: SampleSizeAvg):
    # OK (alternative: str case): requests.post("http://127.0.0.1:8000/stats/avg", json = {"avg": 1.0, "var": 1.0, "alpha": 0.05, "power": 0.8, "group": 2, "lift": 0.03, "alternative": "two-sided"})
    effect_size = params.lift * params.avg / sqrt(params.var)
    sample_size = tt_ind_solve_power(
        effect_size = effect_size,
        alpha = params.alpha,
        power = params.power,
        alternative = params.alternative
    )
    return {"params": params, "sample size": sample_size}
