import pandas as pd
import streamlit as st
from abtools.stats.sample_size import calculate_sample_size_avg, calculate_sample_size_ratio

def get_required_inputs(selected_filters: str):

    if selected_filters == "The differece of average value":

        column_1st, column_2nd, column_3rd, column_4th = st.columns(4)
        avg = column_1st.number_input("Average value (daily)", value = 100.)
        var = column_2nd.number_input("Variance (daily)", value = 100.)
        sample_daily = column_3rd.number_input("\# of sample (daily)", value = 10000.)
        group = column_4th.number_input("\# of test groups", value = 2)

        res = {"avg": avg, "var": var, "sample_daily": sample_daily, "group": group}
    
    elif selected_filters == "The differece of ratio":

        column_1st, column_2nd, column_3rd = st.columns(3)
        rate = column_1st.number_input("Rate (daily)", value = 0.1)
        sample_daily = column_2nd.number_input("\# of sample (daily)", value = 10000.)
        group = column_3rd.number_input("\# of test groups", value = 2)

        res = {"rate": rate, "sample_daily": sample_daily, "group": group}
    
    else:
        raise ValueError
    
    return res

def get_options(is_cheched: bool):
    
    res = {
        "alpha": 0.05, 
        "power": 0.8, 
        "alternative": "two-sided", 
        "lifts": [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1.],
        }

    if is_cheched:

        column_1st, column_2nd, column_3rd, column_4th = st.columns(4)
        alpha = column_1st.number_input("Alpha", min_value=0., max_value=1., value = 0.05)
        power = column_2nd.number_input("Power (1 - beta)", min_value=0., max_value=1., value = 0.8)
        ## one-sided or two-sided
        alternative = column_3rd.selectbox(
            "One-tailed / Two-tailed Test",
            ("two-sided", "larger", "smaller")
            )
        ## lift
        lifts = st.multiselect("Please select numbers by lift", 
            [0.01, 0.02, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
            0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.], 
            default = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1.],
            )

        res = {"alpha": alpha, "power": power, "alternative": alternative, "lifts": lifts}

    return res

def get_table(selected_filters: str, mandatories: dict, options: dict):

    res = pd.DataFrame(
        columns = [
            "lift", 
            "target",
            "sample size by group", 
            "days", 
            "rate by group (1 week)",
            "rate by group (2 week)",
        ])

    for lift in options.get("lifts"):
        
        if selected_filters == "The differece of average value":
            
            n = calculate_sample_size_avg(
                avg=mandatories.get("avg"), 
                var=mandatories.get("var"), 
                alpha=options.get("alpha"), 
                lift=lift, 
                power=options.get("power"),
                group=mandatories.get("group"), 
                alternative=options.get("alternative")
            )

            res = res.append({"lift": lift, 
                "target": (1 + lift) * mandatories.get("avg"),
                "sample size by group": round(n),
                "days": mandatories.get("group") * n / mandatories.get("sample_daily"),
                "rate by group (1 week)": n / (7 * mandatories.get("sample_daily")), 
                "rate by group (2 week)": n / (14 * mandatories.get("sample_daily")), 
            }, ignore_index=True)

        elif selected_filters == "The differece of ratio":
            
            n = calculate_sample_size_ratio(
                rate=mandatories.get("rate"), 
                alpha=options.get("alpha"), 
                lift=lift, 
                power=options.get("power"),
                group=mandatories.get("group"), 
                alternative=options.get("alternative")
            )
                
            res = res.append({"lift": lift, 
                "target": (1 + lift) * mandatories.get("rate"),
                "sample size by group": round(n),
                "days": mandatories.get("group") * n / mandatories.get("sample_daily"),
                "rate by group (1 week)": n / (7 * mandatories.get("sample_daily")), 
                "rate by group (2 week)": n / (14 * mandatories.get("sample_daily")), 
            }, ignore_index=True)

        else:
            raise ValueError
    
    return res


def main() -> None:
    
    st.title("Sample Size Calculator")   
    st.write("Sample size calculation tool for the difference of (avarage value | ratio).")

    st.subheader("1. Testing methods")
    selected_filters = st.selectbox(
        "Select which testing methods to enable",
        ["The differece of average value", "The differece of ratio"],
    )
    st.subheader("2. Set input parameters")
    # mandatory
    mandatories = get_required_inputs(selected_filters)

    """
    ##### Options
    You don't need to choose options in many case. 
    If you want to choose detailed option but you don't know these meaning, please let contact data scientists.
    """
    # optional (for data scientist)
    is_ds = st.checkbox("I want to choose detailed options", value = False)
    options = get_options(is_ds)


    st.subheader("3. Caluculate Sample Size")
    if st.button("Execute"):
        tbl = get_table(selected_filters, mandatories, options)
        st.dataframe(tbl)

        csv = tbl.to_csv()
        st.download_button(
            label = "Download data as CSV", 
            data = csv, 
            file_name = "table.csv", 
            mime = "text/csv"
        )
    else:
        st.write("Please Execute")

if __name__ == "__main__":
    main()
