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
st.markdown(
    """<p>
    <strong>NLP Application for Library of Congress Subject Headings</strong><br>
    This application generates the most relevant Library of Congress subject headings and tags for a given book summary using OpenAI's GPT-3.5 Turbo model.
    </p>""",
    unsafe_allow_html=True,
)

# Input for Book Summary
st.subheader("Enter Book Summary")
book_summary = st.text_area("Provide a book summary here:")

# Prompt for the model
prompt_template = """
Given the following book summary, provide the 8 most relevant Library of Congress subject headings related to the book's subject and the tags for the book summary.

Book Summary: {book_summary}

Please provide the Library of Congress subject headings as a list of strings (8 subject headings) and the tags as a list of strings. Each list should be returned separately in JSON format.
"""

# Define the function to interact with OpenAI API
def generate_subject_headings_and_tags(summary, apikey):
    try:
        openai.api_key = apikey
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating Library of Congress subject headings."},
                {"role": "user", "content": prompt_template.format(book_summary=summary)},
            ],
            max_tokens=300,
        )
        return response.choices[0].message['content']
    except Exception as e:
        raise Exception(f"OpenAI API error: {e}")

# Perform Analysis
if api_key and book_summary:
    if st.button("Generate Subject Headings and Tags"):
        with st.spinner("Generating subject headings and tags..."):
            try:
                # Call the OpenAI function
                analysis_result = generate_subject_headings_and_tags(book_summary, api_key)
                
                # Parse the JSON response
                result_dict = json.loads(analysis_result)
                subject_headings = result_dict.get("subject_headings", [])
                tags = result_dict.get("tags", [])
                
                # Display the results
                st.subheader("Library of Congress Subject Headings")
                st.write(subject_headings)
                
                st.subheader("Tags for the Book Summary")
                st.write(tags)
                
                # Option to export results
                headings_df = pd.DataFrame({"Subject Headings": subject_headings})
                tags_df = pd.DataFrame({"Tags": tags})
                
                st.download_button(
                    label="Download Subject Headings",
                    data=headings_df.to_csv(index=False),
                    file_name="subject_headings.csv",
                    mime="text/csv",
                )
                st.download_button(
                    label="Download Tags",
                    data=tags_df.to_csv(index=False),
                    file_name="tags.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please provide both the API Key and a book summary to enable the Generate button.")
