import streamlit as st
from PIL import Image

from src.utils.pages import get_page_names, switch_page

HOME_SCRIPT_NAME = "Home.py"
# web icon
st.set_page_config(
    page_title="Home",
    page_icon="memo",
)


def main() -> None:
    # title
    st.title("Welcome to A/B Testing tools 👋")
    st.write(
        """
    You can calculate sample size and/or
    validate the result of A/B test in this application. \\
    If you have question, please contact to data scientists.
    """
    )

    menu_list = [
        "I want to stay here: No transition",
        "I want to calculate sample size: Moved to Sample Size Calculator",
        "I want to validate an A/B testing: Moved to A/B Test Calculator",
    ]
    page_names_to_funcs = dict(zip(menu_list, get_page_names(HOME_SCRIPT_NAME)))
    choose = st.selectbox(
        label="Select pages: What is your purpose?",
        options=page_names_to_funcs.keys(),
    )
    # if you select somethig other than the home page, move to the page
    if page_names_to_funcs.get(choose) != get_page_names(HOME_SCRIPT_NAME)[0]:
        switch_page(page_names_to_funcs.get(choose), HOME_SCRIPT_NAME)

    # image
    # if you want to open to streamlit cloud, use ./app/images/ab.png, otherwise use ./images/ab.png
    image = Image.open("./app/images/ab.png")
    st.image(image, use_column_width=True)


if __name__ == "__main__":
    main()
