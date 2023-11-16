import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

import rec_model
from ingredient_parser import ingredient_parser

import nltk

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")


def make_clickable(name, link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = name
    return f'<a target="_blank" href="{link}">{text}</a>'


def main():
  
    st.markdown("# *What's Cooking? :cooking:*")

    st.markdown(
        "## Given a list of ingredients, what different recipes can I can make? :tomato: "
    )

    st.text("")

    session_state = st.session_state
    session_state.recipe_df = ""
    session_state.recipes = ""
    # session_state.model_computed = False
    session_state.execute_recsys = False
    session_state.recipe_df_clean = ""


    ingredients = st.text_input("Enter ingredients you would like to cook with")
    session_state.execute_recsys = st.button("Give me recommendations!")

    if session_state.execute_recsys:
      
        recipe = rec_model.rec_sys(ingredients)

        session_state.recipe_df_clean = recipe.copy()

        # link is the column with hyperlinks
        recipe["url"] = recipe.apply(
            lambda row: make_clickable(row["recipe"], row["url"]), axis=1
        )
        recipe_display = recipe[["recipe", "url", "ingredients", "score"]]
        session_state.recipe_display = recipe_display.to_html(escape=False)
        session_state.recipes = recipe.recipe.values.tolist()
        # session_state.model_computed = True
        session_state.execute_recsys = False
        st.write(session_state.recipe_display, unsafe_allow_html=True)

    # if session_state.model_computed:
    #     # st.write("Either pick a particular recipe or see the top 5 recommendations.")
    #     recipe_all_box = st.selectbox(
    #         "Either see the top 5 recommendations or pick a particular recipe ya fancy",
    #         ["Show me them all!", "Select a single recipe"],
    #     )
    #     if recipe_all_box == "Show me them all!":
        
    #     else:
    #         selection = st.selectbox(
    #             "Select a delicious recipe", options=session_state.recipes
    #         )
    #         selection_details = session_state.recipe_df_clean.loc[
    #             session_state.recipe_df_clean.recipe == selection
    #         ]
    #         st.write(f"Recipe: {selection_details.recipe.values[0]}")
    #         st.write(f"Ingredients: {selection_details.ingredients.values[0]}")
    #         st.write(f"URL: {selection_details.url.values[0]}")
    #         st.write(f"Score: {selection_details.score.values[0]}")

    # sidebar stuff
    # with st.sidebar.expander("How it works?", expanded=True):
    #     st.markdown("## How it works? :thought_balloon:")
        


if __name__ == "__main__":
    main()