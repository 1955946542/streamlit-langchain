import streamlit as st
from langchain.schema import AIMessage, HumanMessage
from api import HuaweiPanguAPI
import ollama

st.set_page_config(page_title="Welcome to DonkChat", layout="wide")

# 设置 page_title ，标签栏的 title
st.title("🏃‍♂️ Welcome to DonkChat")

# 初始化 HuaweiPanguAPI 对象
chat = None

if "PANGU_API_KEY" not in st.session_state:
    st.session_state["PANGU_API_KEY"] = ""
if "PANGU_API_SECRET" not in st.session_state:
    st.session_state["PANGU_API_SECRET"] = ""

if "MODEL_CHOOSE" not in st.session_state:
    st.session_state["MODEL_CHOOSE"] = ""


# 检查Pangu和本地模型是否存在
def check_models():
    return bool(st.session_state["MODEL_CHOOSE"] or (
                st.session_state["PANGU_API_KEY"] and st.session_state["PANGU_API_SECRET"]))


# 验证Pangu凭证
def validate_pangu_credentials(api_key, api_secret):
    try:
        test_chat = HuaweiPanguAPI(api_key=api_key, api_secret=api_secret)
        test_chat([HumanMessage(content="ping")])  # 验证凭证有效性
        return True
    except:
        return False


# 首页显示检查结果
if not check_models():
    st.warning("Neither local model nor Pangu API is set up. Please configure at least one to proceed.")
    st.stop()
else:
    if st.session_state["PANGU_API_KEY"] and st.session_state["PANGU_API_SECRET"]:
        if validate_pangu_credentials(st.session_state["PANGU_API_KEY"], st.session_state["PANGU_API_SECRET"]):
            chat = HuaweiPanguAPI(api_key=st.session_state["PANGU_API_KEY"],
                                  api_secret=st.session_state["PANGU_API_SECRET"])
            st.success("Huawei Pangu API initialized successfully.")
        else:
            st.error("Invalid Pangu API Key or Secret. Please provide correct credentials.")
            st.stop()

# 消息渲染和对话框逻辑
with st.container():
    if chat:
        model_name = "Pangu"
    else:
        model_name = st.session_state['MODEL_CHOOSE']
    st.header(f"Chat with {model_name}!!")

    # 消息渲染
    if "message" not in st.session_state:
        st.session_state["message"] = []

    for message in st.session_state.get("message", []):
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

    prompt = st.chat_input("Type something...")

    if prompt:
        # 检查用户输入时，判断模型是否存在
        if not check_models():
            st.warning("Neither local model nor Pangu API is set up. Please configure at least one to proceed.")
        else:
            st.session_state["message"].append(HumanMessage(content=prompt))
            with st.chat_message("user"):
                st.markdown(prompt)

            if chat:
                ai_message = chat([HumanMessage(content=prompt)])
                st.session_state["message"].append(ai_message)
                with st.chat_message("assistant"):
                    st.markdown(ai_message.content)
            else:
                ai_message_content = ""
                message_placeholder = st.empty()
                for chunk in ollama.chat(
                        model=st.session_state["MODEL_CHOOSE"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state["message"]
                        ],
                        stream=True,
                ):
                    if 'message' in chunk and 'content' in chunk['message']:
                        ai_message_content += (chunk['message']['content'] or "")
                        message_placeholder.markdown(ai_message_content + "▌")

                st.session_state['message'].append(AIMessage(content=ai_message_content))
                message_placeholder.markdown(ai_message_content)