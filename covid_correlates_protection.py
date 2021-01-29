
import streamlit as st
import scispacy
from spacy import displacy
import pandas as pd
import numpy as np
import spacy

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


@st.cache
def load_data(file):
    # read in excel file of abstracts
    df = pd.read_excel(file)
    return df

def load_nlp_model(model):
    # load spacy model
    return spacy.load(model)

st.sidebar.title("Interactive spaCy visualizer")
st.sidebar.header("Named Entities")
default_labels = ["CORRELATE","VACCINE","ANIMAL","ASSAY"]
labels = st.sidebar.multiselect(
    "Entity labels", default_labels, # options
    default = default_labels # default - show all labels
)

st.title("Correlates of Protection")

st.write("The following are articles, both preprint and published, that discuss correlates of protection to COVID-19.")

# file name
file = "covid_relevant_abstracts.xlsx"

lit_df = load_data(file)
lit_df = lit_df.sort_values(by="Publication_Date")
lit_df_high = lit_df[lit_df.probability >= 0.85]
lit_df_subset = lit_df_high.head(20)
nlp_lg = load_nlp_model("en_core_sci_lg")
nlp = load_nlp_model("draft_NER/basic_NER")

# name of entities
#entities = {"CORRELATE","VACCINE","ANIMAL","ASSAY"}
# Add colors to displacy visualization
colors = {"ANIMAL": "#A672F6", "ASSAY": "#F75555","CORRELATE": "#55ABF7", "VACCINE": "#7EE581"}
options = {"ents": labels, "colors": colors}

for i in lit_df_subset.index:
    #st.write(lit_df_subset["Title"][i])
    title = lit_df_subset["Title"][i]
    st.markdown("<p style='color:blue'>{}</p>".format(title), unsafe_allow_html=True)
    doc = nlp(lit_df_subset["Abstract"][i])
    html = displacy.render(doc, style="ent", options=options)
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    st.text("")
