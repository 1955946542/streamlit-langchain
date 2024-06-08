import streamlit as st
from langchain.chat_models import ChatOpenAI

# langchain 官方文档中有
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# 初始化 ChatOpenAI object
chat = None

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
else:
    chat = ChatOpenAI(openai_api_key=st.session_state["OPENAI_API_KEY"])

if "PINECONE_API_KEY" not in st.session_state:
    st.session_state["PINE_API_KEY"] = ""

if "PINECONE_ENVIRONMENT" not in st.session_state:
    st.session_state["PINECONE_ENVIRONMENT"] = ""

st.set_page_config(page_title="Welcome to SL",layout="wide")

# 设置 page_title ，标签栏的 title
st.title("🏃‍♂️ Welcome to SL")

# chat 完成实例化
if chat:
    with st.container():
        st.header("Chat with GPT")
        prompt = st.text_input("Prompt",value="",max_chars=None,key=None,type='default')
        asked = st.button("Ask")
        if asked:
            ai_message = chat([HumanMessage(content=prompt)])
            st.write(ai_message.content)
else:
    with st.container():
        st.warning("Please set your OpenAI API key in the settings page.")





# 下面的代码用处不大，只是起到说明作用

# with st.container():
#     st.header("OpenAI Settings")
#     # 使用 markdown 进行页面显示
#     st.markdown(f"""
#         | OpenAI API Key |
#         |----------------|
#         |{st.session_state["OPENAI_API_KEY"]}|
#     """)

# with st.container():
#     st.header("Pinecone Settings")
#     # 使用 markdown 进行页面显示
#     st.markdown(f"""
#             | Pinecone API key | Environment |
#             |------------------|-------------|
#             |{st.session_state["PINECONE_API_KEY"]}|{st.session_state["PINECONE_ENVIRONMENT"]}|
#         """)
