import streamlit as st
import openai
import pandas as pd

# Sidebar for API Key
st.sidebar.title("Settings")
st.sidebar.text("Provide your OpenAI API Key")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# App Title and Description
st.title("📚 Book Summary Subject Headings and Tags Generator")
st.write(
    "Updated 14:50 08-12-24. This app uses OpenAI's GPT-3.5 model to generate the 8 most relevant Library of Congress subject headings "
    "and tags based on a provided book summary. "
    "To use this app, you need to provide your OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Input for Book Summary
st.subheader("Book Summary Input")
book_summary = st.text_area("Enter the book summary here:")

# Function to generate subject headings and tags
def generate_subject_headings_and_tags(summary, apikey):
    try:
        # Set the API key
        openai.api_key = apikey

        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating Library of Congress subject headings."},
                {"role": "user", "content": f"Given the following book summary, provide the 8 most relevant Library of Congress subject headings and tags:\n\n{summary}"},
            ],
        )

        # Return the response content
        return response.choices[0]['message']['content']
    except Exception as e:
        raise Exception(f"OpenAI API error: {e}")

# Perform action when the user provides a book summary and API key
if api_key and book_summary:
    if st.button("Generate Subject Headings and Tags"):
        with st.spinner("Generating subject headings and tags..."):
            try:
                # Generate subject headings and tags
                analysis_result = generate_subject_headings_and_tags(book_summary, api_key)
                
                # Display the result
                st.subheader("Generated Subject Headings and Tags")
                st.write(analysis_result)

                # Parse the result into subject headings and tags
                try:
                    # Extracting subject headings and tags
                    lines = analysis_result.split("\n")
                    subject_headings = []
                    tags = []

                    for line in lines:
                        if line.lower().startswith("subject headings"):
                            subject_headings = line[len("Subject Headings: "):].strip().split(", ")
                        elif line.lower().startswith("tags"):
                            tags = line[len("Tags: "):].strip().split(", ")

                    # Show subject headings and tags in a dataframe
                    subject_df = pd.DataFrame(subject_headings, columns=["Library of Congress Subject Headings"])
                    tags_df = pd.DataFrame(tags, columns=["Tags"])

                    st.subheader("Library of Congress Subject Headings:")
                    st.dataframe(subject_df)

                    st.subheader("Tags for the Book Summary:")
                    st.dataframe(tags_df)

                except Exception as e:
                    st.error(f"Error parsing the response: {e}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    if not api_key:
        st.info("Please provide your OpenAI API key to continue.")
    elif not book_summary:
        st.info("Please enter a book summary to proceed.")
