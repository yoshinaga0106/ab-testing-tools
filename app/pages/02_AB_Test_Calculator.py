import pandas as pd
import streamlit as st

# web icon
st.set_page_config(
    page_title="AB Test Validator",
    page_icon="bar_chart",
)


def main() -> None:

    st.title("AB Test Calculator")
    st.write("Validate the result of AB test using testing of statistical hypothesis.")

    # testing methods
    st.subheader("1. Testing Family")
    selected_filters = st.selectbox(
        "Select which testing family to enable",
        ["The differece of ratio", "The differece of average value"],
    )

    # set input data
    st.subheader("2. Set Input Paramters")

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
    st.dataframe(tbl)

    # set approach (frequentist / bayesian)
    st.subheader("3. Set Approaches")
    st.radio(
        label="Choose a approach (Frequentist is recommended)",
        options=["Frequentist", "Bayesian"],
    )

    # Statistical test
    st.subheader("4. Test")
    st.write("Under construction.")


if __name__ == "__main__":
    main()
