# chat_page.py

import streamlit as st
from model import qa_bot  # Ensure this import points to your qa_bot function

def display_chat():
    st.title("Patient Chat with MediAssist")
    st.write("Ask your question:")

    # Create a text input for user query
    user_input = st.text_input("Your question:")

    if user_input:
        # Call the QA bot with user input
        response = qa_bot()

        # Use .ainvoke() to handle async calls if necessary (for Langchain models with multiple outputs)
        result = response({'query': user_input})  # This will return the result and source_documents

        # Extract the answer and the source documents if needed
        answer = result['result']  # Assuming 'result' holds the final answer
        sources = result.get('source_documents', [])

        # Display the answer
        st.write("Answer:", answer)

        # Optionally, show source documents
        if sources:
            st.write("Source Documents:")
            for doc in sources:
                # Access the content of the document properly
                st.write(doc.page_content)  # Corrected: Access page_content attribute
        else:
            st.write("No sources found")
