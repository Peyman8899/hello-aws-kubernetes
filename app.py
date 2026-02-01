import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="LangChain Chatbot")
st.title("🦜 LangChain + AWS Bot")

# 1. Get API Key from Environment Variable (Safe way for AWS)
api_key = os.getenv("API_KEY")

if not api_key:
    st.error("Missing OpenAI API Key! Please add it to your ECS Task Environment Variables.")
    st.stop()

# 2. Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)

# 3. Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. Display History
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

# 5. Chat Input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Generate Response
    with st.chat_message("assistant"):
        response = llm.invoke(st.session_state.chat_history)
        st.markdown(response.content)
    
    st.session_state.chat_history.append(AIMessage(content=response.content))