import streamlit as st
import pandas as pd
import json

st.title('Ignorome Base')

with open('epilepsy_database.json', encoding='utf-8') as f:
    data = json.load(f)

db = pd.DataFrame(data).sort_values(by="year")
paper2author = db[["pid", "gaps"]].explode("gaps")
paper2author = db[["pid", "authors"]].explode("authors")
paper = db[["pid", "title", "year"]].drop_duplicates().reset_index(drop=True)

# draw the barplot with the number of papers per year
st.subheader('Number of papers per year')
paper_per_year = paper.groupby("year").size().reset_index(name='count')
st.bar_chart(paper_per_year.set_index("year"), color='#EC9704')

# show a table with authors ordered by number of papers
# ✅ Author selection
st.subheader('Select an author to see their papers')
author_count = paper2author.groupby("authors").size().reset_index(name='count').sort_values(by='count', ascending=False)
selected_author = st.selectbox("Choose an author", author_count["authors"])

# Show the selected author's papers
if selected_author:
    author_papers = db[db["authors"].apply(lambda authors: selected_author in authors)][["pid","title", "year"]]
    st.write(f"### Papers by {selected_author}")
    st.dataframe(author_papers.reset_index(drop=True))


# Show the table with gaps for the selected paper
st.subheader('Gaps in the literature')
selected_paper_id = st.selectbox("Select a paper by ID", paper["pid"].unique())
if selected_paper_id:
    gaps = db[db["pid"] == selected_paper_id]["gaps"].values[0]
    if gaps:
        st.write(f"### Gaps in paper ID {selected_paper_id}")
        st.write(gaps)
    else:
        st.write("No gaps found for this paper.")
