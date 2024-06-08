import streamlit as st
from langchain.schema import AIMessage, HumanMessage
from api import HuaweiPanguAPI

st.set_page_config(page_title="Welcome to SL", layout="wide")

# 初始化 HuaweiPanguAPI 对象
chat = None

if "PANGU_API_KEY" not in st.session_state:
    st.session_state["PANGU_API_KEY"] = ""
if "PANGU_API_SECRET" not in st.session_state:
    st.session_state["PANGU_API_SECRET"] = ""

if "PINECONE_API_KEY" not in st.session_state:
    st.session_state["PINECONE_API_KEY"] = ""

if "PINECONE_ENVIRONMENT" not in st.session_state:
    st.session_state["PINECONE_ENVIRONMENT"] = ""

# 设置 page_title ，标签栏的 title
st.title("🏃‍♂️ Welcome to SL")

if "message" not in st.session_state:
    st.session_state["message"] = []

# chat 完成实例化
if chat:
    with st.container():
        st.header("Chat with Pangu")

        # 消息渲染
        for message in st.session_state["message"]:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)

        prompt = st.chat_input("Type something...")

        if prompt:
            st.session_state["message"].append(HumanMessage(content=prompt))
            with st.chat_message("user"):
                st.markdown(prompt)
            ai_message = chat([HumanMessage(content=prompt)])
            st.session_state["message"].append(ai_message)
            with st.chat_message("assistant"):
                st.markdown(ai_message.content)
else:
    with st.container():
        try:
            if st.session_state["PANGU_API_KEY"] and st.session_state["PANGU_API_SECRET"]:
                chat = HuaweiPanguAPI(api_key=st.session_state["PANGU_API_KEY"],
                                      api_secret=st.session_state["PANGU_API_SECRET"])
                st.success("Huawei Pangu API initialized successfully.")
            else:
                st.warning("Please provide your Huawei Pangu API key and secret in the settings page.")
        except Exception as e:
            st.warning(f"Failed to initialize Huawei Pangu API. Please check your API key and secret. Error: {e}")
