import pandas as pd
import streamlit as st

from src.stats.sample_size import SampleSizeAvg, SampleSizeRatio
from src.utils.data_parameters import AvgData, BaseData, RatioData

# web icon
st.set_page_config(
    page_title="Sample Size Calculator",
    page_icon="clipboard",
)


def get_required_inputs(selected_filters: str):

    if selected_filters == "The difference of average value":

        # default values
        default_values = AvgData().get_default_inputs()
        # input
        col1, col2, col3 = st.columns(3)
        avg = col1.number_input("Average value (daily)", value=default_values.get("avg"))
        var = col2.number_input("Variance (daily)", value=default_values.get("var"))
        sample = col3.number_input("\# of sample (daily)", value=default_values.get("sample"))

        res = AvgData(avg=avg, var=var, sample=sample).get_default_inputs()

    elif selected_filters == "The difference of ratio":

        # default values
        default_values = RatioData().get_default_inputs()
        # input
        col1, col2, col3 = st.columns(3)
        rate = col1.number_input("Rate (daily)", value=default_values.get("rate"))
        sample = col2.number_input("\# of sample (daily)", value=default_values.get("sample"))

        res = RatioData(rate=rate, sample=sample).get_default_inputs()

    else:
        raise ValueError

    return res


def get_options(is_cheched: bool):

    default_values = BaseData(lifts=[0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1.0]).get_options()
    res = default_values

    if is_cheched:

        col1, col2, col3, col4 = st.columns(4)
        alpha = col1.number_input("Alpha", min_value=0.0, max_value=1.0, value=default_values.get("alpha"))
        power = col2.number_input("Power (1 - beta)", min_value=0.0, max_value=1.0, value=default_values.get("power"))
        ## group
        group = col3.number_input("\# of test groups", value=default_values.get("group"))
        ## one-sided or two-sided
        alternative = col4.selectbox("One-tailed / Two-tailed Test", ("two-sided", "larger", "smaller"))
        ## lift
        lifts = st.multiselect(
            "Please select numbers by lift",
            [0.01, 0.02, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            default=default_values.get("lifts"),
        )

        res = BaseData(alpha=alpha, power=power, group=group, alternative=alternative, lifts=lifts).get_options()

    return res


def get_table(selected_filters: str, mandatories: dict, options: dict):

    res = pd.DataFrame(
        columns=[
            "lift",
            "target",
            "sample size by group",
            "days",
            "rate by group (1 week)",
            "rate by group (2 week)",
        ]
    )

    for lift in options.get("lifts"):

        if selected_filters == "The difference of average value":

            ssa = SampleSizeAvg(
                avg=mandatories.get("avg"),
                var=mandatories.get("var"),
                alpha=options.get("alpha"),
                lift=lift,
                power=options.get("power"),
                group=options.get("group"),
                alternative=options.get("alternative"),
            )
            n = ssa.calc_sample_size()

            res = res.append(
                {
                    "lift": lift,
                    "target": (1 + lift) * mandatories.get("avg"),
                    "sample size by group": round(n),
                    "days": options.get("group") * n / mandatories.get("sample"),
                    "rate by group (1 week)": n / (7 * mandatories.get("sample")),
                    "rate by group (2 week)": n / (14 * mandatories.get("sample")),
                },
                ignore_index=True,
            )

        elif selected_filters == "The difference of ratio":

            ssr = SampleSizeRatio(
                rate=mandatories.get("rate"),
                alpha=options.get("alpha"),
                lift=lift,
                power=options.get("power"),
                group=options.get("group"),
                alternative=options.get("alternative"),
            )
            n = ssr.calc_sample_size()

            res = res.append(
                {
                    "lift": lift,
                    "target": (1 + lift) * mandatories.get("rate"),
                    "sample size by group": round(n),
                    "days": options.get("group") * n / mandatories.get("sample"),
                    "rate by group (1 week)": n / (7 * mandatories.get("sample")),
                    "rate by group (2 week)": n / (14 * mandatories.get("sample")),
                },
                ignore_index=True,
            )

        else:
            raise ValueError

    return res


def main() -> None:

    st.title("Sample Size Calculator")
    st.write("Sample size calculation tool for the difference of (avarage value | ratio).")

    st.subheader("1. Testing Family")
    selected_filters = st.selectbox(
        "Select which testing family to enable",
        ["The difference of ratio", "The difference of average value"],
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
    is_ds = st.checkbox("I want to choose detailed options", value=False)
    options = get_options(is_ds)

    st.subheader("3. Caluculate Sample Size")
    if st.button("Execute"):
        tbl = get_table(selected_filters, mandatories, options)

        # check input parameters (user expander)
        with st.expander("If you check input parametes, see explanation"):
            params = dict(**mandatories, **options)
            params = pd.DataFrame(data=params.values(), index=params.keys()).T
            st.write(params)
            params_csv = params.to_csv()
            # download
            st.download_button(
                label="Download data as CSV", data=params_csv, file_name="input_params.csv", mime="text/csv"
            )

        # table
        st.dataframe(tbl)
        tbl_csv = tbl.to_csv()
        # download
        st.download_button(label="Download data as CSV", data=tbl_csv, file_name="table.csv", mime="text/csv")
    else:
        st.write("Please Execute")


if __name__ == "__main__":
    main()
