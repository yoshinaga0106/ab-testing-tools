from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages


def standardize_name(name: str) -> str:
    return name.lower().replace("_", " ")


def get_page_names(home_script_name: str):

    page_names = [standardize_name(config.get("page_name")) for config in get_pages(home_script_name).values()]
    return page_names


def switch_page(page_name: str, home_script_name: str):

    # starndardize
    page_name = standardize_name(page_name)

    # get page informations
    pages = get_pages(home_script_name)

    for page_hash, config in pages.items():
        if standardize_name(config.get("page_name")) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")
