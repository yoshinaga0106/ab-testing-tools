from itertools import combinations

import pandas as pd
import streamlit as st

from src.stats.frequentist import FreqChisqTest, FreqTTest, FreqZTest
from src.utils.data_parameters import BaseData

# web icon
st.set_page_config(
    page_title="AB Test Calculator",
    page_icon="bar_chart",
)


def get_options(approach: str):

    # default values
    default_values = BaseData().get_options()
    # common input
    col1, col2, col3 = st.columns(3)
    alpha = col1.number_input("Alpha", min_value=0.0, max_value=1.0, value=default_values.get("alpha"))
    group = col2.number_input("\# of test groups", value=default_values.get("group"))
    alternative = col3.selectbox("One-tailed / Two-tailed Test", ("two-sided", "larger", "smaller"))
    res = {"alpha": alpha, "group": group, "alternative": alternative}

    if approach == "Bayesian":
        st.write("Not implemented yet")

    return res


def get_table(tbl: pd.DataFrame, selected_filters: str, second_filters: str, options: dict):

    res = pd.DataFrame(
        columns=[
            "pair",
            "alpha",
            "e_alpha",
            "pvalue",
            "is_significant",
        ]
    )

    if selected_filters == "The difference of ratio":

        if second_filters == "t-test":

            group_pair = [
                {
                    "pair": pair,
                    "c": [1] * int(tbl[tbl.get("group") == pair[0]].yes.iloc[-1])
                    + [0] * int(tbl[tbl.get("group") == pair[1]].yes.iloc[-1]),
                    "t": [1] * int(tbl[tbl.get("group") == pair[0]].no.iloc[-1])
                    + [0] * int(tbl[tbl.get("group") == pair[1]].no.iloc[-1]),
                }
                for pair in combinations(tbl.get("group"), 2)
            ]

            for pair in group_pair:
                ins = FreqTTest(
                    alpha=options.get("alpha"),
                    power=None,
                    group=options.get("group"),
                    lift=[],
                    alternative=options.get("alternative"),
                    c=pair.get("c"),
                    t=pair.get("t"),
                )
                res_itr = {"pair": pair.get("pair"), **ins.check_significance()}
                st.write(res_itr)
                res = res.append(res_itr, ignore_index=True)

        elif second_filters == "z-test":

            group_pair = [
                {
                    "pair": pair,
                    "yes": tbl[(tbl.get("group") == pair[0]) | (tbl.get("group") == pair[1])].yes.tolist(),
                    "no": tbl[(tbl.get("group") == pair[0]) | (tbl.get("group") == pair[1])].no.tolist(),
                }
                for pair in combinations(tbl.get("group"), 2)
            ]
            for pair in group_pair:
                ins = FreqZTest(
                    alpha=options.get("alpha"),
                    power=None,
                    group=options.get("group"),
                    lift=[],
                    alternative=options.get("alternative"),
                    yes=pair.get("yes"),
                    no=pair.get("no"),
                )
                res_itr = {"pair": pair.get("pair"), **ins.check_significance()}
                st.write(res_itr)
                res = res.append(res_itr, ignore_index=True)

        elif second_filters == "chi-squire test":

            group_pair = [
                {
                    "pair": pair,
                    "yes": tbl[(tbl.get("group") == pair[0]) | (tbl.get("group") == pair[1])].yes.tolist(),
                    "no": tbl[(tbl.get("group") == pair[0]) | (tbl.get("group") == pair[1])].no.tolist(),
                }
                for pair in combinations(tbl.get("group"), 2)
            ]
            for pair in group_pair:
                ins = FreqChisqTest(
                    alpha=options.get("alpha"),
                    power=None,
                    group=options.get("group"),
                    lift=[],
                    alternative="",
                    yes=pair.get("yes"),
                    no=pair.get("no"),
                )
                res_itr = {"pair": pair.get("pair"), **ins.check_significance()}
                res = res.append(res_itr, ignore_index=True)

    elif selected_filters == "The difference of average value":

        st.write("Not implemented yet")

    return res


def main() -> None:

    st.title("AB Test Calculator")
    st.write("Validate the result of AB test using testing of statistical hypothesis.")

    # testing methods
    st.subheader("1. Testing Family")
    selected_filters = st.selectbox(
        "Select which testing family to enable",
        ["The difference of ratio", "The difference of average value"],
    )
    if selected_filters == "The difference of ratio":
        second_filters = st.selectbox(
            "Select which testing methods to enable",
            ["t-test", "z-test", "chi-squire test"],
        )
    elif selected_filters == "The difference of average value":
        second_filters = st.selectbox(
            "Select which testing methods to enable",
            ["t-test"],
        )

    # set input data
    st.subheader("2. Set Input Paramters")

    if selected_filters == "The difference of ratio":
        # table
        tbl = pd.DataFrame(columns=["group", "yes", "no"])

        # add the key choices_len to the session_state
        if not "choices_len" in st.session_state:
            st.session_state["choices_len"] = 0

        c_from = st.container()  # form
        c_button = st.container()  # button

        with c_from:
            with st.form("Input data"):
                c_input = st.container()  # c1 contains choices
                c_submit = st.container()  # c2 contains submit button
                with c_submit:
                    st.form_submit_button("Submit")

        with c_button:
            col_l, col_r = st.columns(2)
            with col_l:
                if st.button("Add Choise"):
                    st.session_state["choices_len"] += 1

            with col_r:
                if st.button("Remove Choise") and st.session_state["choices_len"] > 1:
                    st.session_state["choices_len"] -= 1
                    st.session_state.pop(f'{st.session_state["choices_len"]}')

        for x in range(st.session_state["choices_len"]):  # create many choices

            with c_input:
                col1, col2, col3 = st.columns(3)
                col1.text_input(label="Group", value="C", key=f"{3 * x + 0}")
                col2.number_input(label="Yes", key=f"{3 * x + 1}")
                col3.number_input(label="No", key=f"{3 * x + 2}")

        for x in range(st.session_state["choices_len"]):
            group = st.session_state[f"{3 * x + 0}"]
            a = st.session_state[f"{3 * x + 1}"]
            b = st.session_state[f"{3 * x + 2}"]
            res = {"group": group, "yes": a, "no": b}
            tbl = tbl.append(res, ignore_index=True)

        # show table
        st.dataframe(tbl, width=600)

    elif selected_filters == "The difference of average value":
        uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
        if uploaded_file is not None:
            tbl = pd.read_csv(uploaded_file)
        else:
            st.write("This is sample data")
            tbl = pd.DataFrame({"C": [100, 300, 500], "T1": [600, 654, 170], "T2": [456, 678, 301]})

        # show table
        st.dataframe(tbl, width=600)
 

    # set approach (frequentist / bayesian)
    st.subheader("3. Set Approaches")
    approach = st.radio(
        label="Choose a approach (Frequentist is recommended)",
        options=["Frequentist", "Bayesian"],
    )
    options = get_options(approach=approach)

    # Statistical test
    st.subheader("4. Test")
    if st.button("Execute"):

        # check input parameters (user expander)
        with st.expander("If you check input parametes, see explanation"):
            params = dict(options)
            params = pd.DataFrame(data=params.values(), index=params.keys()).T
            st.write(params)
            params_csv = params.to_csv()
            # download
            st.download_button(
                label="Download data as CSV", data=params_csv, file_name="input_params.csv", mime="text/csv"
            )

        res = get_table(tbl=tbl, selected_filters=selected_filters, second_filters=second_filters, options=options)

        st.dataframe(res, width=600)
        res_csv = res.to_csv()
        # download
        st.download_button(label="Download data as CSV", data=res_csv, file_name="table.csv", mime="text/csv")


if __name__ == "__main__":
    main()
