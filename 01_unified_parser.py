import os
import re
import pandas as pd
import glob
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# --- 配置参数 ---
INPUT_DIR = 'data'
OUTPUT_FILE = 'parsed_data.csv'
MAX_ENTRIES_PER_FILE = 5000  # 每个文件最多处理的条数

# --- 方案 A: Clarivate TXT 格式解析逻辑 ---
def parse_clarivate_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 每一篇专利通常以 PN (Patent Number) 开始，或者根据 FN 分隔
    records = content.split('PT P\n') # 根据 TXT 特有的起始标识符分割
    data = []
    
    for rec in records:
        if not rec.strip(): continue
        # 提取编号、标题、摘要
        pn = re.search(r'PN (.*?)\n', rec)
        ti = re.search(r'TI (.*?)\n[A-Z]{2} ', rec, re.S)
        ab = re.search(r'AB (.*?)\n[A-Z]{2} ', rec, re.S)
        
        if pn and ti and ab:
            data.append({
                'publication_number': pn.group(1).strip(),
                'title': ti.group(1).replace('\n', ' ').strip(),
                'abstract': ab.group(1).replace('\n', ' ').strip()
            })
    return data

# --- 方案 B: USPTO XML 格式解析逻辑 ---
def parse_uspto_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # USPTO XML 通常在一个文件里包含多个 <us-patent-grant>
    soup = BeautifulSoup(content, 'lxml-xml')
    patents = soup.find_all('us-patent-grant')
    data = []
    
    for p in patents:
        # 只提取实用新型专利 (Utility)
        app_type = p.find('application-reference')
        if app_type and app_type.get('appl-type') != 'utility':
            continue
            
        pn = p.get('file', '').split('-')[0]
        ti = p.find('invention-title')
        ab = p.find('abstract')
        
        if pn and ti and ab:
            data.append({
                'publication_number': pn,
                'title': ti.get_text(strip=True),
                'abstract': ab.get_text(strip=True)
            })
    return data

# --- 并行处理包装函数 ---
def process_single_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.xml':
        return parse_uspto_xml(file_path)
    elif ext == '.txt':
        return parse_clarivate_txt(file_path)
    return []

def main():
    # 自动扫描 data 目录
    all_files = glob.glob(os.path.join(INPUT_DIR, '*.*'))
    target_files = [f for f in all_files if f.endswith(('.xml', '.txt'))]
    
    if not target_files:
        print(f"❌ 在 {INPUT_DIR} 文件夹中未找到 XML 或 TXT 文件！")
        return

    print(f"🚀 检测到 {len(target_files)} 个文件，正在启动 M4 多核并行解析...")
    
    # 利用 M4 的多核性能
    all_results = []
    with Pool(processes=cpu_count()) as pool:
        # 使用 tqdm 显示进度条
        for result in tqdm(pool.imap_unordered(process_single_file, target_files), total=len(target_files)):
            all_results.extend(result)

    # 保存结果
    df = pd.DataFrame(all_results)
    if not df.empty:
        # 清洗数据：去除换行符，防止 CSV 错位
        df = df.replace(r'\n', ' ', regex=True).replace(r',', ' ', regex=True)
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"✅ 解析完成！共处理 {len(df)} 篇专利，已保存至 {OUTPUT_FILE}")
    else:
        print("⚠️ 未能提取到任何有效的专利数据。")

if __name__ == "__main__":
    main()