import os
from langchain_openai import OpenAIEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

# --- 核心配置：硅基流动方案 ---
# 1. 请去 https://siliconflow.cn/ 注册并获取 API KEY
API_KEY = "SILICONFLOW_API_KEY" 
BASE_URL = "https://api.siliconflow.cn/v1"
# 2. 模型选定为 bge-m3
EMBED_MODEL = "BAAI/bge-m3"

OUTDIR = 'embeddings'
PROCESS_DOC = 'parsed_data.csv'

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

def main():
    # 1. 轻量化加载数据
    print(f"📂 正在加载数据: {PROCESS_DOC}...")
    loader = CSVLoader(file_path=PROCESS_DOC, encoding="utf-8")
    documents = loader.load()

    # 2. 文本切片
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
    docs = text_splitter.split_documents(documents)
    print(f"✂️ 已将文档切分为 {len(docs)} 个片段")

    # 3. 初始化云端向量引擎
    embeddings = OpenAIEmbeddings(
        openai_api_key=API_KEY,
        openai_api_base=BASE_URL,
        model=EMBED_MODEL
    )

    # 4. 通过 API 批量构建向量库
    # API 模式下 batch_size 可以设大，减少网络往返次数
    batch_size = 30 
    vectorstore = None

    print(f"🌐 正在通过云端 API 进行向量化计算...")
    for i in tqdm(range(0, len(docs), batch_size), desc="云端计算进度"):
        batch_docs = docs[i : i + batch_size]
        try:
            if vectorstore is None:
                vectorstore = FAISS.from_documents(batch_docs, embeddings)
            else:
                vectorstore.add_documents(batch_docs)
        except Exception as e:
            print(f"\n❌ 第 {i} 批次出错: {e}")
            continue

    # 5. 保存本地索引
    save_path = os.path.join(OUTDIR, "patent_vector_db")
    vectorstore.save_local(save_path)
    print(f"\n✅ 成功！向量库已保存至: {save_path}")

if __name__ == "__main__":
    main()
