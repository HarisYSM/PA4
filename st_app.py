import streamlit as st
import openai
import pandas as pd
import json

# Sidebar for API Key
st.sidebar.title("Settings")
st.sidebar.text("Provide your OpenAI API Key")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# App Title and Description
st.title("📚 Book Summary Subject Headings and Tags Generator")
st.write(
    "This app generates the 8 most relevant Library of Congress subject headings "
    "and descriptive tags for a given book summary using OpenAI's GPT-3.5 model."
)

# Input for Book Summary
st.subheader("Book Summary Input")
book_summary = st.text_area("Enter the book summary here:")

# Define prompt
PROMPT = """
You are a helpful assistant for generating Library of Congress Subject Headings and tags. Your task is to analyze the provided book summary and output the results in JSON format.

1. Generate the following outputs:
   - Subject Headings: A list of the 8 most relevant Library of Congress Subject Headings for the book.
   - Tags: A list of descriptive tags summarizing the book's main topics and themes.

2. Output the result in the following JSON format:
{
    "subject_headings": [
        "Subject Heading 1",
        "Subject Heading 2",
        ...
    ],
    "tags": [
        "Tag 1",
        "Tag 2",
        ...
    ]
}
"""

# Function to call OpenAI API
def generate_subject_headings_and_tags(summary, apikey):
    try:
        # Set the API key dynamically
        openai.api_key = apikey

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": f"Analyze the following book summary:\n{summary}"},
            ],
        )

        # Parse the response content
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"OpenAI API error: {e}")

# Perform action when the user provides a book summary and API key
if api_key and book_summary:
    if st.button("Generate Subject Headings and Tags"):
        with st.spinner("Generating subject headings and tags..."):
            try:
                # Generate subject headings and tags
                analysis_result = generate_subject_headings_and_tags(book_summary, api_key)

                # Display the results
                if "subject_headings" in analysis_result:
                    subject_df = pd.DataFrame(analysis_result["subject_headings"], columns=["Library of Congress Subject Headings"])
                    st.subheader("Library of Congress Subject Headings:")
                    st.dataframe(subject_df)
                else:
                    st.info("No subject headings found.")

                if "tags" in analysis_result:
                    tags_df = pd.DataFrame(analysis_result["tags"], columns=["Tags"])
                    st.subheader("Tags for the Book Summary:")
                    st.dataframe(tags_df)
                else:
                    st.info("No tags found.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
elif not api_key:
    st.info("Please provide your OpenAI API key.")
elif not book_summary:
    st.info("Please provide a book summary.")
