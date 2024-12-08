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
    "This app generates the 8 most relevant 🏷️ Library of Congress subject headings, descriptive tags, "
    "and their confidence scores based on a provided book summary using OpenAI's GPT-3.5 model. 🤖"
    "These outputs can help with categorizing and managing library resources, and aid in decision-making "
    "for purchasing new books based on library statistics. 🏫"
)

# Input for Book Summary
st.subheader("Book Summary Input")
book_summary = st.text_area("Enter the book summary here:")

# Calculate and display the word count
if book_summary:
    word_count = len(book_summary.split())
    st.write(f"**Word Count:** {word_count} words")
else:
    st.write("No text entered. Word count will appear here.")


# Define prompt
PROMPT = """
You are a helpful assistant for generating Library of Congress Subject Headings and tags. Your task is to analyze the provided book summary and output the results in JSON format.

1. Generate the following outputs:
   - Subject Headings: A list of the 8 most relevant Library of Congress Subject Headings for the book, along with a confidence score (0-100%) for each heading, indicating its relevance.
   - Tags: A list of descriptive 8 tags summarizing the book's main topics and themes, along with a confidence score (0-100%) for each tag, indicating its relevance.

2. Output the result in the following JSON format:
{
    "subject_headings": [
        {"heading": "Subject Heading 1", "confidence": 95},
        {"heading": "Subject Heading 2", "confidence": 90},
        ...
    ],
    "tags": [
        {"tag": "Tag 1", "confidence": 92},
        {"tag": "Tag 2", "confidence": 88},
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
                    subject_data = analysis_result["subject_headings"]
                    subject_df = pd.DataFrame(subject_data)
                    subject_df.columns = ["Library of Congress Subject Headings", "Confidence Score"]

                    st.subheader("Library of Congress Subject Headings:")
                    st.dataframe(subject_df)
                else:
                    st.info("No subject headings found.")

                if "tags" in analysis_result:
                    tags_data = analysis_result["tags"]
                    tags_df = pd.DataFrame(tags_data)
                    tags_df.columns = ["Tags", "Confidence Score"]

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
