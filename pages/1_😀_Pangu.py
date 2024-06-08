import streamlit as st

# 如果会话中没有 api_key 则置为空
if "PANGU_API_KEY" not in st.session_state:
    st.session_state["PANGU_API_KEY"] = ""
if "PANGU_API_SECRET" not in st.session_state:
    st.session_state["PANGU_API_SECRET"] = ""

st.set_page_config(page_title="Pangu Settings", layout="wide")

st.title("PANGU Settings")

# 值从会话状态中获取，
pangu_api_key = st.text_input("API Key",value=st.session_state["PANGU_API_KEY"],max_chars=None,key=None,type='password')
pangu_api_secret = st.text_input("API Secret",value=st.session_state["PANGU_API_SECRET"],max_chars=None,key=None,type='password')

# 提交按钮
saved = st.button("Save")

# 将 save 的 api_key 保存在会话中
if saved:
    st.session_state["PANGU_API_KEY"] = pangu_api_key
    st.session_state["PANGU_API_SECRET"] = pangu_api_secret
