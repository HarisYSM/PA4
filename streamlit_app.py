import streamlit as st
from openai import OpenAI

# Title and description for the app
st.title("📚 Book Summary Subject Headings and Tags Generator")
st.write(
    "This app uses OpenAI's GPT-3.5 model to generate the 8 most relevant Library of Congress subject headings "
    "and tags based on a provided book summary. "
    "To use this app, you need to provide your OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Request OpenAI API key from the user
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize the OpenAI client with the provided API key
    client = OpenAI(api_key=openai_api_key)

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

        # Request a response from OpenAI using the client
        try:
            completion = client.completions.create(
                model="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=100
            )

            # Extract the response text
            response_text = completion.choices[0].text.strip()

            # Split the response into two parts: subject headings and tags
            st.write("### Generated Subject Headings and Tags")

            try:
                # Parse the response into subject headings and tags
                subject_headings = []
                tags = []

                lines = response_text.split("\n")
                for line in lines:
                    if line.lower().startswith("subject headings"):
                        subject_headings = line[len("Subject Headings: "):].strip().split(", ")
                    elif line.lower().startswith("tags"):
                        tags = line[len("Tags: "):].strip().split(", ")

                # Display the results
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
