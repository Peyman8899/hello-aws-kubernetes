import streamlit as st
import os
import redis
import pickle  # Used to "freeze" LangChain objects into Redis
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# --- REDIS SETUP ---
# 'redis-service' is the name we gave to the K8s Service in the YAML
r = redis.Redis(host='redis-service', port=6379, db=0)

def save_history_to_redis(history):
    # We use pickle because LangChain messages are objects, not just strings
    r.set("chat_history_key", pickle.dumps(history))

def load_history_from_redis():
    data = r.get("chat_history_key")
    if data:
        return pickle.loads(data)
    return []
# -------------------

st.set_page_config(page_title="LangChain Chatbot")
st.title("🦜 LangChain + AWS Bot")

api_key = os.getenv("API_KEY")

if not api_key:
    st.error("Missing OpenAI API Key!")
    st.stop()

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)

# 3. Initialize Chat History from Redis (instead of just session_state)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_history_from_redis()

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
    
    # --- SAVE TO REDIS ---
    save_history_to_redis(st.session_state.chat_history)