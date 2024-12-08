import streamlit as st
import openai
import pandas as pd
import json

# Sidebar for API Key
st.sidebar.title("Settings")
st.sidebar.text("Provide your OpenAI API Key")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# App Title and Description
st.title("📚 Library of Congress Subject Headings and Tags Generator")
st.markdown(
    """<p>
    <strong>Generate Subject Headings and Tags for a Book Summary</strong><br>
    This app uses OpenAI's GPT-3.5 Turbo model to generate the 8 most relevant Library of Congress subject headings 
    and tags based on a provided book summary.
    </p>""",
    unsafe_allow_html=True,
)

# Input for Book Summary
st.subheader("Enter Book Summary")
book_summary = st.text_area("Paste the book summary here:")

# Check if inputs are provided
if not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to proceed.")
elif not book_summary:
    st.warning("Please provide a book summary to proceed.")
else:
    # Define the OpenAI prompt
    prompt = f"""
    Given the following book summary, provide the 8 most relevant Library of Congress subject headings related to the book's subject and the tags for the book summary.

    Book Summary: {book_summary}

    Please provide the Library of Congress subject headings as a list of strings (8 subject headings) and the tags as a list of strings in the following JSON format:
    {{
        "subject_headings": ["heading1", "heading2", ...],
        "tags": ["tag1", "tag2", ...]
    }}
    """

    # Call OpenAI API for Subject Headings and Tags
    def generate_subject_headings_and_tags(summary, api_key):
        openai.api_key = api_key
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that helps generate Library of Congress subject headings and tags for book summaries."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0
            )
            return response.choices[0].message["content"]
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")

    # Generate and Display Results
    if st.button("Generate Subject Headings and Tags"):
        with st.spinner("Generating..."):
            try:
                result = generate_subject_headings_and_tags(book_summary, api_key)
                result_dict = json.loads(result)
                subject_headings = result_dict.get("subject_headings", [])
                tags = result_dict.get("tags", [])

                # Convert to DataFrames for Display
                subject_headings_df = pd.DataFrame(subject_headings, columns=["Subject Headings"])
                tags_df = pd.DataFrame(tags, columns=["Tags"])

                # Display Results
                st.subheader("Library of Congress Subject Headings")
                st.dataframe(subject_headings_df)

                st.subheader("Tags for the Book Summary")
                st.dataframe(tags_df)

            except Exception as e:
                st.error(f"An error occurred: {e}")

