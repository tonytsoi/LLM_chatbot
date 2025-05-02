from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from transformers import pipeline
import streamlit as st

def generate_response(input_text):       
    model_id = "meta-llama/Llama-3.2-1B-Instruct"
    
    pipe = pipeline(
                "text-generation",
                model=model_id,       
                
                # Maximum no. of new tokens
                max_new_tokens=2048,
                
                # Return only the text after the input text
                return_full_text=False
            )
    
    # Quick fix for Langchain error
    pipe.tokenizer.pad_token_id = pipe.tokenizer.eos_token_id
    
    llm = HuggingFacePipeline(pipeline = pipe)
    
    model = ChatHuggingFace(llm=llm)
    
    response = model.invoke(input_text).content
    
    for sentence in response.split("/n"):
        yield sentence + " "
        
st.title("LLM Chatbot")
st.caption("A Streamlit chatbot powerd by Llama3.2")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat messages from hisotry on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])
        
# Accept user input
if prompt := st.chat_input("What do want to ask?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(generate_response(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})