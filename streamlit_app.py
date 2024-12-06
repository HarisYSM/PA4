import streamlit as st
import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')  # Retrieve API key from environment variables
)

# Title and description for the app
st.title("📚 Book Summary Subject Headings and Tags Generator")
st.write(
    "Updated 21:41, This app uses OpenAI's GPT-3.5 model to generate the 8 most relevant Library of Congress subject headings "
    "and tags based on a provided book summary. "
    "To use this app, you need to provide your OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Request OpenAI API key from the user
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set the OpenAI API key dynamically
    client.api_key = openai_api_key

    # Ask the user for the book summary
    book_summary = st.text_area("Enter the book summary here:")

    # Check if the user has provided a book summary
    if book_summary:
        # Define the prompt to generate subject headings and tags
        prompt = f"""
        Given the following book summary, provide the 8 most relevant Library of Congress subject headings related to the book's subject and the tags for the book summary.

        Book Summary: {book_summary}

        Please provide the Library of Congress subject headings as a list of strings (8 subject headings) and the tags as a list of strings. Each list should be returned separately.
        """

        # Request a response from OpenAI using the new API
        try:
            completion = client.completions.create(
                model="gpt-3.5-turbo",  # Use GPT-3.5-turbo model
                prompt=prompt,
                max_tokens=300
            )

            # Extract the response text
            response_text = completion.choices[0].text.strip()

            # Split the response into two parts: subject headings and tags
            st.write("### Generated Subject Headings and Tags")

            # Assuming the response contains the lists in a simple format, split and display them
            try:
                # Separate the subject headings and tags using simple text parsing
                subject_headings = []
                tags = []

                # Separate based on expected response structure
                lines = response_text.split("\n")
                for line in lines:
                    if line.lower().startswith("subject headings"):
                        subject_headings = line[len("Subject Headings: "):].strip().split(", ")
                    elif line.lower().startswith("tags"):
                        tags = line[len("Tags: "):].strip().split(", ")

                # Display the subject headings and tags
                st.subheader("Library of Congress Subject Headings:")
                st.write(subject_headings)

                st.subheader("Tags for the Book Summary:")
                st.write(tags)
            except Exception as e:
                st.error(f"Error parsing the response: {e}")

        except Exception as e:
            st.error(f"An error occurred while communicating with OpenAI: {e}")
    else:
        st.info("Please enter a book summary to proceed.")
