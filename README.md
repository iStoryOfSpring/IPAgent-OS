# ⚖️ IPAgent-OS: Next-Gen Patent Analysis RAG System

# CHINESE(Simplified)

IPAgent-OS 是一个基于检索增强生成 (RAG) 的专利分析智能工作站。本项目 Fork 自 [Matthew Shaxted 的原始 IPAgent](原项目链接)，并在其基础上进行了深度的底层重构与国产化算力适配，专为复杂技术方案的专利挖掘与比对而设计。

🚀 相较于原版的核心提升
1. 算力引擎全面解耦与国产化替换：
   - Embedding: 摒弃了昂贵的 OpenAI Embeddings，接入 [硅基流动 (SiliconFlow)](https://siliconflow.cn/) API，采用 `BAAI/bge-m3` 多语言模型进行高精度向量化，大幅降低云端计算成本。
   - LLM: 核心推理引擎从 GPT-4 迁移至 DeepSeek-V3 (deepseek-chat)，在处理复杂技术权利要求时展现出极高的性价比和逻辑严密性。
2. 现代化的 LCEL 架构适配极客环境：
   - 彻底移除了老旧且容易引发兼容性问题的 `langchain.chains` 模块。
   - 全面采用 LangChain Expression Language (LCEL) 管道语法 (`|`) 重写 RAG 链。这使得项目能够完美兼容 **Python 3.14** 等前瞻性开发环境。
3. 多核并行优化：
   - 编写了 `01_unified_parser.py` 统一解析器，利用 `multiprocessing.Pool` 榨干多核处理器（特别针对 Apple Silicon 优化），实现对 Clarivate TXT 和 USPTO XML 格式海量专利文件的并发秒级解析。
4. GUI 工作站级交互体验：
   - 从单一的命令行对话框升级为基于 Streamlit 的双栏 OS 界面。支持左侧对话推理、右侧 DataFrame 专利原文实时溯源对账，并加入侧边栏参数控制。

🛠️ 快速开始 (Quick Start)


1. 环境准备
推荐使用 Python 3.10 - 3.14 环境。

Bash:

#git clone [https://github.com/iStoryOfSpring/IPAgent-OS.git](https://github.com/iStoryOfSpring/IPAgent-OS.git)

#cd IPAgent-OS

#pip install -r requirements.txt

2. 数据解析

将你的专利原始文件 (.txt 或 .xml) 放入 data/ 目录，然后运行并发解析器：

Bash:

#python 01_unified_parser.py

这将在根目录生成 parsed_data.csv。

3. 构建向量库

确保你已配置硅基流动的 API 密钥，然后运行：

Bash:

#python 02_create_vector.py

这将在 embeddings/ 目录下生成 FAISS 本地索引。

4. 启动可视化工作站

确保你已配置 DeepSeek API 密钥，运行主程序：

Bash:

#streamlit run chatbot.py

📜 许可证 (License)

本项目基于 MIT 许可证开源。请参阅 LICENSE 文件了解详细信息。

🙏 致谢 (Acknowledgments)

感谢 [Matthew Shaxted] 提供的初始架构灵感。

感谢 LangChain, FAISS, DeepSeek, 以及 SiliconFlow 提供的基础设施。


# ENGLISH(United States)

IPAgent-OS
IPAgent-OS is an intelligent patent analysis workstation based on Retrieval-Augmented Generation (RAG). This project is forked from [Matthew Shaxted’s original IPAgent](Link to original project) and features a deep underlying refactor and adaptation for localized computing power. It is specifically designed for patent mining and comparison of complex technical solutions.

🚀 Key Improvements Over the Original
1. Decoupled Computing Engine & Localized Adaptation

Embedding: Replaced expensive OpenAI Embeddings with the SiliconFlow API. By utilizing the BAAI/bge-m3 multilingual model for high-precision vectorization, cloud computing costs have been significantly reduced.

LLM: The core inference engine has migrated from GPT-4 to DeepSeek-V3 (deepseek-chat), delivering exceptional cost-performance and logical rigor when processing intricate technical claims.

2. Modern LCEL Architecture for Geek Environments

Completely removed the legacy langchain.chains module, which was prone to compatibility issues.

Fully rewrote the RAG chains using LangChain Expression Language (LCEL) pipe syntax (|). This ensures the project is perfectly compatible with forward-looking development environments like Python 3.14.

3. Multi-core Parallel Optimization

Developed the 01_unified_parser.py unified parser. It leverages multiprocessing.Pool to maximize multi-core processor performance (specifically optimized for Apple Silicon), enabling second-level concurrent parsing of massive patent files in Clarivate TXT and USPTO XML formats.

4. Workstation-Grade GUI Experience

Upgraded from a basic CLI dialog to a Streamlit-based dual-pane OS interface. It supports real-time inference on the left and DataFrame-based patent source verification on the right, complemented by a sidebar for parameter control.

🛠️ Quick Start
1. Environment Setup

Recommended Environment: Python 3.10 - 3.14.

Bash:

#git clone https://github.com/iStoryOfSpring/IPAgent-OS.git

#cd IPAgent-OS

#pip install -r requirements.txt

2. Data Parsing

Place your raw patent files (.txt or .xml) into the data/ directory, then run the concurrent parser:

Bash:

#python 01_unified_parser.py

This will generate parsed_data.csv in the root directory.

3. Build Vector Store

Ensure you have configured your SiliconFlow API Key, then run:

Bash:

#python 02_create_vector.py

This will generate a local FAISS index in the embeddings/ directory.

4. Launch the Visual Workstation

Ensure you have configured your DeepSeek API Key, then run the main application:

Bash:

#streamlit run chatbot.py

📜 License

This project is open-source under the MIT License. Please refer to the LICENSE file for details.

🙏 Acknowledgments

Gratitude to Matthew Shaxted for the initial architectural inspiration.

Thanks to LangChain, FAISS, DeepSeek, and SiliconFlow for providing the essential infrastructure.
