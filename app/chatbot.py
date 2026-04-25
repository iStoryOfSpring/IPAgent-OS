import os
import pandas as pd
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-reasoner")

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
SILICONFLOW_EMBED_MODEL = os.getenv("SILICONFLOW_EMBED_MODEL", "BAAI/bge-m3")

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY 未设置，请在 .env 文件中配置")
if not SILICONFLOW_API_KEY:
    raise ValueError("SILICONFLOW_API_KEY 未设置，请在 .env 文件中配置")

st.set_page_config(page_title="IPAgent-OS", layout="wide", page_icon="⚖️")

st.markdown("""
<style>
    .stApp { background: #f0f2f6; }
    .main > .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

    /* ===== Sidebar 白底黑字 ===== */
    section[data-testid="stSidebar"] {
        background: #fff;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] *:hover {
        background-color: #f5f5f5 !important;
    }
    section[data-testid="stSidebar"] .stSubheader {
        color: #64748b; font-size: 0.7rem;
        text-transform: uppercase; letter-spacing: 1.5px; margin-top: 0;
    }
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stSlider p,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stNumberInput p,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stRadio p,
    section[data-testid="stSidebar"] .stTextArea textarea,
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] .st-emotion-cache-1inwz65 {
        color: #1e293b !important;
    }
    section[data-testid="stSidebar"] .stAlert {
        background: #f0fdf4; border: 1px solid #bbf7d0;
        color: #166534; font-size: 0.85rem; padding: 0.5rem 0.8rem;
    }
    section[data-testid="stSidebar"] hr { border-color: #e2e8f0; margin: 0.5rem 0; }
    section[data-testid="stSidebar"] .stButton button {
        background: #fff; border: 1px solid #cbd5e1;
        color: #1e293b; border-radius: 8px; width: 100%; transition: all 0.15s;
        font-size: 0.85rem;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #f1f5f9; border-color: #94a3b8;
    }
    section[data-testid="stSidebar"] .stDownloadButton button {
        background: #eff6ff; border: 1px solid #bfdbfe;
        color: #1d4ed8; border-radius: 8px; width: 100%; transition: all 0.15s;
        font-size: 0.85rem;
    }
    section[data-testid="stSidebar"] .stDownloadButton button:hover {
        background: #dbeafe; border-color: #93c5fd;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #fff !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important; font-size: 0.85rem !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
        border-color: #94a3b8 !important;
    }
    /* sidebar textarea */
    section[data-testid="stSidebar"] .stTextArea textarea {
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
        font-size: 0.85rem !important;
    }
    /* sidebar expander */
    section[data-testid="stSidebar"] [data-testid="stExpander"] {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px;
        margin-bottom: 4px;
    }
    section[data-testid="stSidebar"] [data-testid="stExpander"]:hover {
        background: #f1f5f9 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: #334155 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        color: #0f172a !important;
    }
    /* sidebar expander internal content does NOT get hover gray */
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderContent"]:hover {
        background-color: transparent !important;
    }
    /* sidebar expander internal elements */
    section[data-testid="stSidebar"] [data-testid="stExpander"] p,
    section[data-testid="stSidebar"] [data-testid="stExpander"] label,
    section[data-testid="stSidebar"] [data-testid="stExpander"] .st-emotion-cache-1inwz65 {
        color: #1e293b !important;
    }
    /* sidebar selectbox inside expander */
    section[data-testid="stSidebar"] [data-testid="stExpander"] div[data-baseweb="select"] > div {
        color: #1e293b !important;
    }
    /* sidebar radio buttons */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        color: #1e293b !important;
    }

    /* ===== Chat ===== */
    div[data-testid="stChatMessage"] {
        background: #fff; border-radius: 10px; padding: 0.7rem 1rem;
        margin-bottom: 0.4rem; border: 1px solid #e2e8f0;
    }
    div[data-testid="stChatMessage"][data-testid*="user"] { border-left: 3px solid #3b82f6; }
    div[data-testid="stChatMessage"][data-testid*="assistant"] { border-left: 3px solid #10b981; }

    div[data-testid="stChatInput"] {
        border-radius: 10px; border: 1px solid #cbd5e1;
        background: #fff;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #3b82f6; box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
    }

    .source-patent {
        font-size: 0.8em; color: #64748b;
        padding: 2px 0 2px 8px; border-left: 3px solid #f59e0b;
        margin: 2px 0;
    }
    .source-patent a { color: #2563eb; text-decoration: none; font-weight: 500; }
    .source-patent a:hover { text-decoration: underline; }

    .stDataFrame { border-radius: 8px; overflow: hidden; }
    .stDataFrame td, .stDataFrame th { font-size: 0.78rem !important; }
    .stSpinner > div { border-top-color: #3b82f6 !important; }

    .sys-info {
        font-size: 0.72rem; color: #94a3b8;
        padding: 0.2rem 0; line-height: 1.6;
    }

    .preview-label {
        font-size: 0.85rem; font-weight: 600; color: #334155;
        padding: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)


def google_patent_url(pub_num):
    return f"https://patents.google.com/?q={pub_num}"


@st.cache_resource
def _init_system():
    embeddings = OpenAIEmbeddings(
        openai_api_key=SILICONFLOW_API_KEY,
        openai_api_base=SILICONFLOW_BASE_URL,
        model=SILICONFLOW_EMBED_MODEL
    )
    vector_path = "embeddings/patent_vector_db"
    if not os.path.exists(vector_path):
        return None, None, None, None
    vectorstore = FAISS.load_local(vector_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    llm = ChatOpenAI(
        model=DEEPSEEK_MODEL, openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base=DEEPSEEK_BASE_URL, temperature=0.1
    )
    df = pd.read_csv('parsed_data.csv')
    return llm, retriever, df, vectorstore

llm, retriever, df, vectorstore = _init_system()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources_map" not in st.session_state:
    st.session_state.sources_map = {}
if "highlight_indices" not in st.session_state:
    st.session_state.highlight_indices = set()

RETRIEVAL_MODES = {
    "相似度": "similarity",
    "MMR（多样性）": "mmr",
    "相似度阈值": "similarity_score_threshold",
}


def _rebuild_retriever(vs, search_type, k, score_threshold, fetch_k):
    if search_type == "similarity":
        return vs.as_retriever(search_kwargs={"k": k})
    elif search_type == "mmr":
        return vs.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k, "fetch_k": fetch_k}
        )
    else:
        return vs.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": k, "score_threshold": score_threshold}
        )


def _count_tokens(text):
    if isinstance(text, (int, float)):
        return int(text)
    en_chars = sum(1 for c in text if c.isascii())
    cn_chars = len(text) - en_chars
    return int(cn_chars * 1.5 + en_chars / 4)


# ================================================================
# Sidebar — 折叠参数组
# ================================================================
with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:8px;margin-bottom:2px;">'
        '<span style="font-size:1.4rem;">⚖️</span>'
        '<span style="font-size:1.1rem;font-weight:700;color:#0f172a;">IPAgent-OS</span>'
        '</div>',
        unsafe_allow_html=True
    )
    st.caption("Patent Intelligence Workstation")

    if df is not None:
        st.success(f"已加载 {len(df)} 篇专利")

    # ----- 检索 -----
    with st.expander("检索设置", expanded=False):
        search_type_label = st.selectbox(
            "检索模式", options=list(RETRIEVAL_MODES.keys()), index=0
        )
        search_type = RETRIEVAL_MODES[search_type_label]
        retrieve_k = st.number_input("返回数量", 1, 50, 10)

        fetch_k = 30
        if search_type == "mmr":
            fetch_k = st.number_input("候选数", retrieve_k, 100, 30)

        score_threshold = 0.0
        if search_type == "similarity_score_threshold":
            score_threshold = st.slider("相似度阈值", 0.0, 1.0, 0.5)

        if vectorstore is not None:
            retriever = _rebuild_retriever(
                vectorstore, search_type, retrieve_k, score_threshold, fetch_k
            )

    # ----- 生成 -----
    with st.expander("生成设置", expanded=False):
        temperature = st.slider("发散程度", 0.0, 1.0, 0.1)
        st.caption("注意: DeepSeek Reasoner 不支持 temperature 参数，调节后不生效。若需控制发散程度请切换模型。")
        max_tokens = st.slider("最大输出长度", 256, 4096, 2048, step=128)

    # ----- 角色 -----
    with st.expander("分析角色", expanded=False):
        role_preset = st.radio(
            "回答风格",
            [
                "专利律师（严谨专业）",
                "技术专家（深入浅出）",
                "商业分析师（市场视角）",
            ],
            index=0, label_visibility="collapsed"
        )
        if role_preset == "专利律师（严谨专业）":
            role_instruction = "你是一个资深的专利律师和技术专家。请基于以下专利片段回答问题。要求：逻辑严密、分点叙述、若涉及技术方案请详细解构。"
        elif role_preset == "技术专家（深入浅出）":
            role_instruction = "你是一个跨领域的技术专家。请用通俗易懂的语言解释这些专利中的技术方案，注重原理说明和实际应用场景，帮助非专利专业人员理解。"
        else:
            role_instruction = "你是一个商业分析师与知识产权顾问。请从市场竞争、技术趋势、商业价值等角度分析这些专利，给出战略层面的见解。\n要求：指出潜在应用领域、竞争对手动向、商业化可能性。"
        extra_instruction = st.text_area(
            "附加要求（可选）", placeholder="例：用表格对比各专利的技术差异", height=70,
            label_visibility="collapsed"
        )

    # ----- 操作 -----
    st.divider()
    if st.button("清空对话历史", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources_map = {}
        st.session_state.highlight_indices = set()
        st.rerun()

    if st.session_state.messages:
        chat_lines = [
            f"{'用户' if m['role'] == 'user' else 'AI助理'}:\n{m['content']}"
            for m in st.session_state.messages
        ]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="导出对话记录",
            data="\n\n---\n\n".join(chat_lines),
            file_name=f"ipagent_chat_{ts}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()
    if df is not None:
        total_chars = int(df["title"].str.len().sum() + df["abstract"].str.len().sum())
        total_tokens = _count_tokens(total_chars)
        st.markdown(
            f'<div class="sys-info">'
            f'专利数: {len(df)} | 估算 tokens: {total_tokens:,}<br>'
            f'模型: DeepSeek Reasoner + BGE-M3</div>',
            unsafe_allow_html=True
        )

    st.caption("DeepSeek Reasoner · SiliconFlow BGE-M3")

# ================================================================
# 主区域 — 3:1 对话优先
# ================================================================
col_dialogue, col_preview = st.columns([3, 1])

with col_preview:
    st.markdown('<div class="preview-label">专利库</div>', unsafe_allow_html=True)
    if df is not None:
        if st.session_state.highlight_indices:
            def hl(row):
                return ['background-color: #fff3cd'] * len(row) if row.name in st.session_state.highlight_indices else [''] * len(row)
            st.dataframe(df.style.apply(hl, axis=1), height=700, use_container_width=True)
        else:
            st.dataframe(df, height=700, use_container_width=True)

with col_dialogue:
    st.markdown('<div class="preview-label">对话</div>', unsafe_allow_html=True)

    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
        if msg["role"] == "assistant" and idx in st.session_state.sources_map:
            for s in st.session_state.sources_map[idx]:
                st.markdown(
                    f'<div class="source-patent">检索来源: <a href="{google_patent_url(s["publication_number"])}" target="_blank">{s["publication_number"]}</a> — {s["title"]}</div>',
                    unsafe_allow_html=True
                )

    if prompt := st.chat_input("请下达分析指令（例如: 总结这些专利的技术路线）"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        if llm and retriever and df is not None:
            retrieved_docs = retriever.invoke(prompt)
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

            sources = []
            for doc in retrieved_docs:
                meta = doc.metadata
                row_idx = meta.get("row")
                pub_num = ""
                title = ""
                if row_idx is not None:
                    row_idx = int(row_idx)
                    if row_idx < len(df):
                        pub_num = df.iloc[row_idx].get("publication_number", "")
                        title = df.iloc[row_idx].get("title", "")
                if pub_num:
                    sources.append({"publication_number": pub_num, "title": title or "无标题"})
                if row_idx is not None:
                    st.session_state.highlight_indices.add(row_idx)

            llm.temperature = temperature
            llm.max_tokens = max_tokens

            suffix = f"\n\n{extra_instruction.strip()}\n\n专业建议:" if (extra_instruction and extra_instruction.strip()) else "\n\n专业建议:"
            template = role_instruction + """

检索到的专利上下文:
{context}

分析指令: {question}
""" + suffix

            chain = (
                {"context": lambda _: context_text, "question": RunnablePassthrough()}
                | ChatPromptTemplate.from_template(template)
                | llm
                | StrOutputParser()
            )

            with st.chat_message("assistant"):
                with st.spinner("DeepSeek 正在扫描专利库..."):
                    response = chain.invoke(prompt)
                    st.markdown(response)
                for s in sources:
                    st.markdown(
                        f'<div class="source-patent">检索来源: <a href="{google_patent_url(s["publication_number"])}" target="_blank">{s["publication_number"]}</a> — {s["title"]}</div>',
                        unsafe_allow_html=True
                    )

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.sources_map[len(st.session_state.messages) - 1] = sources

            st.rerun()
