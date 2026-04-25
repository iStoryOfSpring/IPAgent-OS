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

# --- 方案 A: Clarivate TXT 格式解析逻辑 ---
def parse_clarivate_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 每一篇专利通常以 PN (Patent Number) 开始，或者根据 FN 分隔
    records = content.split('PT P\n') # 根据 TXT 特有的起始标识符分割
    data = []
    
    for rec in records:
        if not rec.strip(): continue
        
        # 提取核心字段
        pn = re.search(r'PN (.*?)\n', rec)
        ti = re.search(r'TI (.*?)\n[A-Z]{2} ', rec, re.S)
        ab = re.search(r'AB (.*?)\n[A-Z]{2} ', rec, re.S)
        
        # 新增：提取发表时间 (PD)、发明人 (AU)、申请人/机构 (AE)
        pd_match = re.search(r'PD (.*?)\n', rec)
        au_match = re.search(r'AU (.*?)\n', rec)
        ae_match = re.search(r'AE (.*?)\n', rec)

        # 清洗发表时间 (提取形如 "25 Jan 2019" 的日期)
        pub_date = ""
        if pd_match:
            date_search = re.search(r'(\d{1,2}\s+[a-zA-Z]{3}\s+\d{4})', pd_match.group(1))
            if date_search:
                pub_date = date_search.group(1)
            else:
                # 兼容处理：如果没有匹配到标准英文日期，取 PD 行的第二段字符串
                parts = pd_match.group(1).split()
                pub_date = parts[1] if len(parts) > 1 else pd_match.group(1)

        if pn and ti and ab:
            data.append({
                'publication_number': pn.group(1).strip(),
                'title': ti.group(1).replace('\n', ' ').strip(),
                'abstract': ab.group(1).replace('\n', ' ').strip(),
                'publication_date': pub_date,
                'inventor': au_match.group(1).strip() if au_match else "",
                'assignee': ae_match.group(1).strip() if ae_match else ""
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
        
        # 新增：提取 XML 中的日期以对齐 CSV 字段
        pub_ref = p.find('publication-reference')
        pub_date = ""
        if pub_ref:
            date_tag = pub_ref.find('date')
            if date_tag:
                pub_date = date_tag.get_text(strip=True)
        
        if pn and ti and ab:
            data.append({
                'publication_number': pn,
                'title': ti.get_text(strip=True),
                'abstract': ab.get_text(strip=True),
                'publication_date': pub_date,
                'inventor': "", # 暂不提取，保持字典键一致性
                'assignee': ""  # 暂不提取，保持字典键一致性
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

    print(f"🚀 检测到 {len(target_files)} 个文件，正在启动并行解析...")
    
    # 利用多核性能
    all_results = []
    with Pool(processes=cpu_count()) as pool:
        # 使用 tqdm 显示进度条
        for result in tqdm(pool.imap_unordered(process_single_file, target_files), total=len(target_files)):
            all_results.extend(result)

    # 保存结果
    df = pd.DataFrame(all_results)
    if not df.empty:
        # 清洗数据：去除换行符，防止 CSV 错位
        df = df.replace(r'\n', ' ', regex=True)
        # 优化：改为 utf-8-sig 以防止在 Windows 环境下 Excel 打开乱码
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"✅ 解析完成！共处理 {len(df)} 篇专利，已保存至 {OUTPUT_FILE}")
    else:
        print("⚠️ 未能提取到任何有效的专利数据。")

if __name__ == "__main__":
    main()