import os
import pandas as pd
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 1. 配置与密钥 ---
DEEPSEEK_API_KEY = "DEEPSEEK_API_KEY"

# --- 2. 页面美化配置 ---
st.set_page_config(page_title="IPAgent-OS", layout="wide", page_icon="⚖️")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 核心引擎加载 (带缓存) ---
@st.cache_resource
def init_system():
    # 本地向量模型 (对齐 02 文件)
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # 载入本地向量库
    vector_path = "embeddings/patent_vector_db"
    if not os.path.exists(vector_path):
        return None, None, None
    
    vectorstore = FAISS.load_local(vector_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # 云端 DeepSeek 引擎
    llm = ChatOpenAI(
        model='deepseek-chat', 
        openai_api_key=DEEPSEEK_API_KEY, 
        openai_api_base='https://api.deepseek.com',
        temperature=0.1
    )
    
    # 加载原始 CSV 用于预览
    df = pd.read_csv('parsed_data.csv')
    return llm, retriever, df

llm, retriever, df = init_system()

# --- 4. 专业侧边栏 (Sidebar) ---
with st.sidebar:
    st.title("IPAgent 控制面板")
    st.divider()
    
    if df is not None:
        st.success(f"📈 已加载专利数: {len(df)}")
    
    st.subheader("系统参数")
    temp = st.slider("发散程度 (Temperature)", 0.0, 1.0, 0.1)
    
    if st.button("清空对话历史"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("项目名称: Terminator - 螺旋藻PBR系统专利分析")

# --- 5. 主界面布局 ---
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("📄 专利库预览")
    if df is not None:
        st.dataframe(df, height=600)

with col1:
    st.subheader("💬 深度分析对话")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 循环显示对话
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("请下达分析指令 (例如: 总结这些专利的技术路线)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if llm and retriever:
            # 强化版提示词模板
            template = """你是一个资深的专利律师和技术专家。请基于以下专利片段回答问题。
            要求：逻辑严密、分点叙述、若涉及技术方案请详细解构。
            
            检索到的专利上下文:
            {context}
            
            分析指令: {question}
            
            专业建议:"""
            
            rag_prompt = ChatPromptTemplate.from_template(template)
            chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | rag_prompt
                | llm
                | StrOutputParser()
            )

            with st.chat_message("assistant"):
                with st.spinner("DeepSeek 正在扫描专利库..."):
                    response = chain.invoke(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
