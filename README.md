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
> Forked from [Matthew Shaxted's original IPAgent](https://github.com/mattshax/ipagent) with deep architectural refactoring, modern LLM integration, and localized computing support.

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
- **LLM**: Core inference engine migrated from GPT-4 to **DeepSeek-V4** (`deepseek-v4-flash`), delivering exceptional cost-performance and logical rigor for complex technical claims.

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

### 2. Launch the Workstation (Integrated Workflow)

Place your raw patent files (`.txt` or `.xml`) in the `data/` directory, then start the Streamlit app directly:

```bash
streamlit run app/chatbot.py
```

The app provides an **all-in-one pipeline UI**:

1. **Enter API Keys** — Fill in DeepSeek and SiliconFlow keys in the password fields (session-only, never persisted)
2. **Step 1: Parse** — Click to run `01_unified_parser.py` with real-time progress bar and log output. Generates `parsed_data.csv`.
3. **Step 2: Vectorize** — Click to run `02_create_vector.py` and build the local FAISS index in `embeddings/`.
4. **Step 3: Enter Workstation** — Switch to the patent analysis chat interface.

> **No need to run `01_unified_parser.py` or `02_create_vector.py` manually** — the Streamlit UI handles the entire pipeline. If data and vector index already exist, a quick-skip button takes you straight to the chatbot.

---

## 📁 Project Structure

```
IPAgent-OS/
├── app/
│   └── chatbot.py          # Streamlit workstation (integrated pipeline + chat UI)
├── data/                   # Raw patent files (.txt / .xml)
├── embeddings/             # Local FAISS vector index
│   └── patent_vector_db/
├── 01_unified_parser.py    # Concurrent file parser (multi-core, called by UI)
├── 02_create_vector.py     # Vector store builder (called by UI)
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## 🔧 Configuration

No `.env` or configuration file needed. API keys are entered directly into the Streamlit UI on first launch (password-masked, session-only, never persisted to disk).

Required API keys:
- **DeepSeek API Key** — for LLM inference (`deepseek-reasoner`)
- **SiliconFlow API Key** — for vector embeddings (`BAAI/bge-m3`)

Get your free keys at [platform.deepseek.com](https://platform.deepseek.com/) and [cloud.siliconflow.cn](https://cloud.siliconflow.cn/).

---

## 📜 License

This project is open-source under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Matthew Shaxted** — for the original IPAgent architecture and inspiration.
- **LangChain**, **FAISS**, **DeepSeek**, and **SiliconFlow** — for providing essential infrastructure.
- All contributors and users of this project.



---

<br>
<hr>
<br>

<h1 id="简体中文">⚖️ IPAgent-OS：下一代专利分析 RAG 系统</h1>

> 基于检索增强生成（RAG）的专利分析智能工作站。  
> Fork 自 [Matthew Shaxted 的原始 IPAgent](https://github.com/mattshax/ipagent)，进行了深度底层重构与国产化算力适配。

---

## ✨ 核心提升

### 1. 算力引擎全面解耦与国产化替换

- **Embedding**：摒弃昂贵的 OpenAI Embeddings，接入 [硅基流动 (SiliconFlow)](https://siliconflow.cn/) API，采用 `BAAI/bge-m3` 多语言模型进行高精度向量化，大幅降低成本。
- **LLM**：核心推理引擎从 GPT-4 迁移至 **DeepSeek-V4** (`deepseek-v4-flash`)，处理复杂技术权利要求时兼具高性价比与逻辑严密性。

### 2. 现代化的 LCEL 架构

- 彻底移除老旧且易引发兼容性问题的 `langchain.chains` 模块。
- 全面采用 **LangChain Expression Language (LCEL)** 管道语法 (`|`) 重写 RAG 链，完美兼容 **Python 3.14** 等前瞻环境。

### 3. 多核并行优化

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

### 2. 启动工作站（一体化工作流）

将专利原始文件 (`.txt` / `.xml`) 放入 `data/` 目录，直接启动 Streamlit：

```bash
streamlit run app/chatbot.py
```

应用提供**全流程集成界面**：

1. **填写 API Key** — 在密码框中输入 DeepSeek 和 SiliconFlow 密钥（仅会话有效，不会泄露）
2. **Step 1：解析** — 点击执行 `01_unified_parser.py`，实时显示进度条和日志，生成 `parsed_data.csv`
3. **Step 2：向量化** — 点击执行 `02_create_vector.py`，构建 FAISS 本地索引
4. **Step 3：进入工作站** — 切换至专利分析对话界面

> **无需手动运行 `01_unified_parser.py` 或 `02_create_vector.py`** — Streamlit 界面自动完成整个流程。若已有数据，一键跳过至对话界面。

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

无需创建 `.env` 或任何配置文件。API 密钥在首次启动时直接填入 Streamlit 界面（密码框保护，仅会话有效，不会写入磁盘）。

需要的密钥：
- **DeepSeek API Key** — 用于 LLM 推理（`deepseek-reasoner`）
- **SiliconFlow API Key** — 用于向量嵌入（`BAAI/bge-m3`）

前往 [platform.deepseek.com](https://platform.deepseek.com/) 和 [cloud.siliconflow.cn](https://cloud.siliconflow.cn/) 免费获取。

---

## 📜 许可证

本项目基于 **MIT 许可证**开源。详见 [LICENSE](LICENSE)。

---

## 🙏 致谢

- **Matthew Shaxted** — 初始架构灵感与代码基础
- **LangChain**、**FAISS**、**DeepSeek**、**硅基流动** — 基础设施支持
- 所有贡献者与使用者

## 🥚 彩蛋

- **保留了一些bug**, 供大家自由探索。如有问题请**及时反馈**。
