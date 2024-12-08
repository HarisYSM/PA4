import streamlit as st
import openai 

# Title and description for the app
st.title("📚 Book Summary Subject Headings and Tags Generator")
st.write(
    "Updated 23:46-07-12-24, This app uses OpenAI's GPT-3.5 model to generate the 8 most relevant Library of Congress subject headings "
    "and tags based on a provided book summary. "
    "To use this app, you need to provide your OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Sidebar for API key input
st.sidebar.title("🔑 API Key Input")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key in the sidebar to continue.", icon="🗝️")
else:
    # Initialize the OpenAI client with the provided API key
    client = OpenAI(api_key=openai_api_key)

    # Main app content
    st.header("📖 Generate Subject Headings and Tags")
    book_summary = st.text_area("Enter the book summary here:")

    # Check if the user has provided a book summary
    if book_summary:
        # Define the prompt to generate subject headings and tags
        prompt = f"""
        Given the following book summary, provide the 3 most relevant Library of Congress subject headings related to the book's subject and the tags for the book summary.

        Book Summary: {book_summary}

        Please provide the Library of Congress subject headings as a list of strings (3 subject headings) and the tags as a list of strings. Each list should be returned separately.
        """

        # Request a response from OpenAI using the client
        try:

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.7,
            )
            result = response["choices"][0]["message"]["content"].strip()
            st.success("Tags and Headline generated successfully!")

            # Extract the response text
            #response_text = completion.choices[0].text.strip()

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
