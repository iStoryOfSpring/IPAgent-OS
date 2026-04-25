import os
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from tqdm import tqdm

load_dotenv()

# --- 核心配置 ---
API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
EMBED_MODEL = os.getenv("SILICONFLOW_EMBED_MODEL", "BAAI/bge-m3")

if not API_KEY:
    raise ValueError("SILICONFLOW_API_KEY 未设置，请在 .env 文件中配置")

OUTDIR = 'embeddings'
PROCESS_DOC = 'parsed_data.csv'

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

def process_batch(batch_docs, embeddings_model, batch_idx):
    for attempt in range(3):
        try:
            texts = [doc.page_content for doc in batch_docs]
            embs = embeddings_model.embed_documents(texts)
            return batch_docs, embs
        except Exception as e:
            time.sleep(1)
    print(f"\n❌ 第 {batch_idx} 批次（{len(batch_docs)} 条）重试 3 次后依然失败，已跳过。")
    return None, None

def main():
    print(f"📂 正在加载数据: {PROCESS_DOC}...")
    loader = CSVLoader(file_path=PROCESS_DOC, encoding="utf-8")
    documents = loader.load()

    docs = documents
    print(f"✂️ 已将文档切分为 {len(docs)} 个片段")

    # 3. 初始化云端向量引擎
    embeddings = OpenAIEmbeddings(
        openai_api_key=API_KEY,
        openai_api_base=BASE_URL,
        model=EMBED_MODEL
    )

    # --- 提速核心 1：增加单批次数量与并发线程数 ---
    batch_size = 50       # 每次发给 API 的文本数量
    max_workers = 10      # 同时开启 10 个线程向云端要数据

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]
    
    all_valid_docs = []
    all_valid_embs = []

    print(f"🚀 正在开启 {max_workers} 个线程并发请求 API...")
    start_time = time.time()

    # 4. 通过多线程池并发拉取向量
    failed_count = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_batch, batch, embeddings, i): i for i, batch in enumerate(batches)}

        for future in tqdm(futures, total=len(batches), desc="云端计算进度"):
            b_docs, b_embs = future.result()
            if b_docs and b_embs:
                all_valid_docs.extend(b_docs)
                all_valid_embs.extend(b_embs)
            else:
                failed_count += 1

    if failed_count:
        print(f"⚠️ {failed_count} 个批次处理失败，共丢失 {failed_count * batch_size} 条数据")
    else:
        print("✅ 所有批次处理成功")

    api_end_time = time.time()
    print(f"⚡ API 请求完成，耗时: {api_end_time - start_time:.2f} 秒")

    # --- 提速核心 2：避免循环 I/O，一次性构建 FAISS 索引 ---
    print(f"📦 正在将 {len(all_valid_docs)} 条数据一次性写入向量库...")
    
    # 将文本和对应的向量打包
    text_list = [doc.page_content for doc in all_valid_docs]
    meta_list = [doc.metadata for doc in all_valid_docs]
    text_embeddings = list(zip(text_list, all_valid_embs))
    
    # 瞬间在内存中完成全量构建
    vectorstore = FAISS.from_embeddings(text_embeddings, embeddings, metadatas=meta_list)

    # 5. 保存本地索引
    save_path = os.path.join(OUTDIR, "patent_vector_db")
    vectorstore.save_local(save_path)
    
    print(f"✅ 成功！总耗时: {time.time() - start_time:.2f} 秒。向量库已保存至: {save_path}")

if __name__ == "__main__":
    main()