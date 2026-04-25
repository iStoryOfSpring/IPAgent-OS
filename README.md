<div align="center">

# ⚖️ IPAgent-OS

**Next-Gen Patent Analysis RAG System**

[![Python](https://img.shields.io/badge/Python-3.10_–_3.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-339933?logo=langchain)](https://langchain.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-6554C0)](https://github.com/facebookresearch/faiss)
[![Streamlit](https://img.shields.io/badge/Streamlit-Workstation-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/iStoryOfSpring/IPAgent-OS/pulls)

English | [简体中文](#简体中文)

</div>

> A patent analysis intelligent workstation built on Retrieval-Augmented Generation (RAG).  
> Forked from [Matthew Shaxted's original IPAgent](https://github.com/mdshxt/IPAgent) with deep architectural refactoring, modern LLM integration, and localized computing support.

---

## 📋 Table of Contents

- [✨ Key Improvements](#-key-improvements)
- [🛠️ Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🔧 Configuration](#-configuration)
- [📜 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📝 Changelog](#-changelog)

---

## ✨ Key Improvements

### 1. Decoupled Computing Engine & Localized Adaptation

- **Embedding**: Replaced expensive OpenAI Embeddings with [SiliconFlow](https://siliconflow.cn/) API, using the `BAAI/bge-m3` multilingual model for high-precision vectorization at a fraction of the cost.
- **LLM**: Core inference engine migrated from GPT-4 to **DeepSeek-V3** (`deepseek-chat`), delivering exceptional cost-performance and logical rigor for complex technical claims.

### 2. Modern LCEL Architecture

- Completely removed the legacy `langchain.chains` module (prone to compatibility issues).
- Fully rewrote RAG chains using **LangChain Expression Language (LCEL)** pipe syntax (`|`), ensuring compatibility with forward-looking environments like **Python 3.14**.

### 3. Multi-core Parallel Optimization (Apple Silicon)

- Developed `01_unified_parser.py` — a unified parser leveraging `multiprocessing.Pool` to maximize multi-core performance.
- Specifically optimized for **Apple Silicon (M-series chips)**, enabling second-level concurrent parsing of massive patent files in Clarivate TXT and USPTO XML formats.

### 4. Workstation-Grade GUI Experience

- Upgraded from a basic CLI dialog to a **dual-pane Streamlit OS-like interface**.
  - **Left panel**: Conversational inference
  - **Right panel**: DataFrame-based patent source verification
  - **Sidebar**: Flexible parameter controls

---

## 🛠️ Quick Start

### Prerequisites

- Python **3.10 – 3.14**
- API keys for [SiliconFlow](https://cloud.siliconflow.cn/) and [DeepSeek](https://platform.deepseek.com/)

### 1. Clone & Install

```bash
git clone https://github.com/iStoryOfSpring/IPAgent-OS.git
cd IPAgent-OS
pip install -r requirements.txt
```

### 2. Data Parsing

Place your raw patent files (`.txt` or `.xml`) in the `data/` directory, then run the concurrent parser:

```bash
python 01_unified_parser.py
```

This generates `parsed_data.csv` in the project root.

### 3. Build Vector Store

Configure your SiliconFlow API key (see [Configuration](#-configuration)), then:

```bash
python 02_create_vector.py
```

This generates a local FAISS index in the `embeddings/` directory.

### 4. Launch the Workstation

Configure your DeepSeek API key, then:

```bash
streamlit run app/chatbot.py
```

---

## 📁 Project Structure

```
IPAgent-OS/
├── app/
│   └── chatbot.py          # Streamlit workstation entry point
├── data/                   # Raw patent files (.txt / .xml)
├── embeddings/             # Local FAISS vector index
│   └── patent_vector_db/
├── 01_unified_parser.py    # Concurrent file parser (multi-core)
├── 02_create_vector.py     # Vector store builder
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## 🔧 Configuration

Set the following environment variables or add them to a `.env` file in the project root:

```bash
# Required: SiliconFlow API (for embeddings)
SILICONFLOW_API_KEY=sk-your-key-here

# Required: DeepSeek API (for LLM inference)
DEEPSEEK_API_KEY=sk-your-key-here
```

---

## 📜 License

This project is open-source under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Matthew Shaxted** — for the original IPAgent architecture and inspiration.
- **LangChain**, **FAISS**, **DeepSeek**, and **SiliconFlow** — for providing essential infrastructure.
- All contributors and users of this project.

---

## 📝 Changelog

### 2025-04-25
- Unified parser rewrite: `01_unified_parser.py` with `multiprocessing.Pool` for concurrent JSON/TXT/XML parsing
- Full LCEL migration: removed legacy `langchain.chains`, adopted `|` pipeline syntax
- Embedding migration: OpenAI → SiliconFlow (`BAAI/bge-m3`)
- LLM migration: GPT-4 → DeepSeek-V3 (`deepseek-chat`)
- GUI overhaul: CLI → Streamlit dual-pane workstation with sidebar controls
- Project restructuring: modular `app/` layout, removed deprecated modules

---

<br>
<hr>
<br>

<h1 id="简体中文">⚖️ IPAgent-OS：下一代专利分析 RAG 系统</h1>

> 基于检索增强生成（RAG）的专利分析智能工作站。  
> Fork 自 [Matthew Shaxted 的原始 IPAgent](https://github.com/mdshxt/IPAgent)，进行了深度底层重构与国产化算力适配。

---

## ✨ 核心提升

### 1. 算力引擎全面解耦与国产化替换

- **Embedding**：摒弃昂贵的 OpenAI Embeddings，接入 [硅基流动 (SiliconFlow)](https://siliconflow.cn/) API，采用 `BAAI/bge-m3` 多语言模型进行高精度向量化，大幅降低成本。
- **LLM**：核心推理引擎从 GPT-4 迁移至 **DeepSeek-V3** (`deepseek-chat`)，处理复杂技术权利要求时兼具高性价比与逻辑严密性。

### 2. 现代化的 LCEL 架构

- 彻底移除老旧且易引发兼容性问题的 `langchain.chains` 模块。
- 全面采用 **LangChain Expression Language (LCEL)** 管道语法 (`|`) 重写 RAG 链，完美兼容 **Python 3.14** 等前瞻环境。

### 3. M4 芯片与多核并行优化

- 编写 `01_unified_parser.py` 统一解析器，利用 `multiprocessing.Pool` 榨干多核处理器。
- 实现海量 Clarivate TXT / USPTO XML 专利文件的并发秒级解析。

### 4. 工作站级 GUI 交互体验

- 从命令行对话框升级为 **Streamlit 双栏 OS 界面**。
  - **左栏**：对话推理
  - **右栏**：DataFrame 专利原文实时溯源对账
  - **侧边栏**：灵活的参数控制

---

## 🛠️ 快速开始

### 环境要求

- Python **3.10 – 3.14**
- [硅基流动](https://cloud.siliconflow.cn/) 与 [DeepSeek](https://platform.deepseek.com/) 的 API 密钥

### 1. 克隆与安装

```bash
git clone https://github.com/iStoryOfSpring/IPAgent-OS.git
cd IPAgent-OS
pip install -r requirements.txt
```

### 2. 数据解析

将专利原始文件 (`.txt` / `.xml`) 放入 `data/` 目录，运行并发解析器：

```bash
python 01_unified_parser.py
```

将在根目录生成 `parsed_data.csv`。

### 3. 构建向量库

配置硅基流动 API 密钥后运行：

```bash
python 02_create_vector.py
```

将在 `embeddings/` 目录下生成 FAISS 本地索引。

### 4. 启动可视化工作站

配置 DeepSeek API 密钥后运行：

```bash
streamlit run app/chatbot.py
```

---

## 📁 项目结构

```
IPAgent-OS/
├── app/
│   └── chatbot.py          # Streamlit 工作站入口
├── data/                   # 原始专利文件 (.txt / .xml)
├── embeddings/             # FAISS 向量索引
│   └── patent_vector_db/
├── 01_unified_parser.py    # 并发文件解析器（多核）
├── 02_create_vector.py     # 向量库构建器
├── requirements.txt        # Python 依赖
├── LICENSE                 # MIT 许可证
└── README.md               # 本文件
```

---

## 🔧 配置

在项目根目录设置以下环境变量或创建 `.env` 文件：

```bash
# 必填：硅基流动 API（用于词嵌入）
SILICONFLOW_API_KEY=sk-your-key-here

# 必填：DeepSeek API（用于 LLM 推理）
DEEPSEEK_API_KEY=sk-your-key-here
```

---

## 📜 许可证

本项目基于 **MIT 许可证**开源。详见 [LICENSE](LICENSE)。

---

## 🙏 致谢

- **Matthew Shaxted** — 初始架构灵感与代码基础
- **LangChain**、**FAISS**、**DeepSeek**、**硅基流动** — 基础设施支持
- 所有贡献者与使用者

---
