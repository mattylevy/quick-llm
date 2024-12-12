import streamlit as st
import ollama

st.title("QuickLLM")


# Set a default model
if "llm_model" not in st.session_state:
    st.session_state["llm_model"] = "mistral"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input():
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # This creates an empty placeholder in the Streamlit app.A placeholder is a special Streamlit element that can be updated later. It's used here to display the assistant's response as it's being generated.
        message_placeholder = st.empty()
        # This initializes an empty string that will be used to accumulate the full response from the assistant.
        full_response = ""
        # Stream the response
        stream = ollama.chat(
            model=st.session_state["llm_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        for chunk in stream:
            full_response += chunk["message"]["content"]
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
