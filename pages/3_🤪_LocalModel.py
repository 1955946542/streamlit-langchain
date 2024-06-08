import streamlit as st
import ollama

st.set_page_config(page_title="Choose Model", layout="wide")

st.title("Choose Model")

try:
    # 获取本地模型列表
    model_list = ollama.list()

    # 检查本地模型列表是否为空
    if 'models' in model_list and model_list['models']:
        option = st.selectbox(
            'Select a model',
            [model['name'] for model in model_list['models']]
        )
        st.session_state["MODEL_CHOOSE"] = option
    else:
        st.warning("No local models found. Please download a model from Ollama to proceed.")
except Exception as e:
    st.warning("Failed to retrieve local models. Please ensure Ollama is installed correctly and running.")