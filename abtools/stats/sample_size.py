from scipy.special import comb
from statsmodels.stats.power import tt_ind_solve_power, zt_ind_solve_power
from statsmodels.stats.proportion import proportion_effectsize

def effective_alpha(alpha: float, groups: int) -> float:
    
    e_alpha = alpha / comb(groups, 2)
    return e_alpha

def calculate_sample_size_avg(avg: float, 
                          var: float, 
                          alpha: int, 
                          lift: float, 
                          power: float = 0.8, 
                          group: int = 2, 
                          method: str = 't-test', 
                          alternative: str = 'two-sided',
                          ) -> int:
    
    # correct alpha (if groups >= 2)
    e_alpha = effective_alpha(alpha, group)
    # effect size
    effect_size = lift * avg / var
    
    if method == 't-test':
        sample_size = tt_ind_solve_power(effect_size=effect_size,  alpha=e_alpha, power=power, alternative=alternative)
    else:
        print("Not implemented yet")
    
    return sample_size

def calculate_sample_size_ratio(rate: float, 
                          alpha: int, 
                          lift: float, 
                          power: float = 0.8, 
                          group: int = 2, 
                          alternative: str = 'two-sided',
                          ) -> int:
    
    # correct alpha (if groups >= 2)
    e_alpha = effective_alpha(alpha, group)
    # effect size
    effect_size = proportion_effectsize((1 + lift) * rate, rate)
    
    sample_size = zt_ind_solve_power(effect_size=effect_size, alpha=e_alpha, power=power, ratio = 1 + lift, alternative=alternative)
    
    return sample_size
