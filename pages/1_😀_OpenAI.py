import streamlit as st

# 如果会话中没有 api_key 则置为空
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""

st.set_page_config(page_title="OpenAI Settings", layout="wide")

st.title("OpenAI Settings")

# 值从会话状态中获取，
openai_api_key = st.text_input("API Key",value=st.session_state["OPENAI_API_KEY"],max_chars=None,key=None,type='password')

# 提交按钮
saved = st.button("Save")

# 将 save 的 api_key 保存在会话中
if saved:
    st.session_state["OPENAI_API_KEY"] = openai_api_key
