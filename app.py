# Import necessary libraries
import openai
import streamlit as st
import pandas as pd

# Local imports
import utils
from utils.log import logger


def main():
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])
    if openai_api_key:
        openai.api_key = openai_api_key
        
    if uploaded_file is not None:
        logger.info("File uploaded successfully.")
        df, qp = initialize_query_engine(uploaded_file)
        initialize_chat()
        user_input_handler(qp)
    else:
        st.warning("Please upload an Excel file to proceed.")


def initialize_query_engine(uploaded_file):
    """Initializes the data frame and query processing engine with an uploaded Excel file."""
    logger.info("Initializing query engine")
    df = pd.read_excel(uploaded_file)
    (pandas_prompt, pandas_output_parser, response_synthesis_prompt) = (
        utils.get_prompts(df)
    )
    llm = utils.init_model(model=utils.DEFAULT_OPENAI_MODEL)
    qp = utils.query_engine(
        llm=llm,
        pandas_prompt=pandas_prompt,
        pandas_output_parser=pandas_output_parser,
        response_synthesis_prompt=response_synthesis_prompt,
    )
    return df, qp


def initialize_chat():
    """Initializes the chat history in the Streamlit session state if not already present."""
    logger.info("Initiazing chat.")
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_messages():
    """Displays chat messages stored in the session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def user_input_handler(qp):
    """Handles user input and generates responses using the query processing engine."""
    display_chat_messages()
    prompt = st.chat_input("What is up?")
    if prompt:
        process_user_prompt(prompt, qp)


def process_user_prompt(prompt, qp):
    """Processes the user's prompt, generates a response, and updates the chat history."""
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    response = response_generator(prompt, qp)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


def response_generator(prompt, qp):
    """Generates a response for a given prompt using the query processing engine."""
    try:
        logger.info("Generating Response.")
        response = qp.run(
            query_str=prompt,
        )
    except:
        logger.info("Error While generating response.")

    return response.message.content


if __name__ == "__main__":
    main()
