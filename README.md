# ⚖️ IPAgent-OS: Next-Gen Patent Analysis RAG System

# Simplified CHINESE(China)

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


# CHINESE（Hong Kong,China;  Macau,China; Taiwan,China)

IPAgent-OS 是一款基於檢索增強生成 (RAG) 技術的專利分析智能工作站。本項目 Fork 自 Matthew Shaxted 的原始 IPAgent，並在此基礎上進行了深度底層重構與算力適配，專為複雜技術方案的專利挖掘與比對而設計。

🚀 較原版之核心提升 (Key Improvements)

算力引擎全面解耦與本土化適配：

Embedding: 棄用昂貴的 OpenAI Embeddings，接入 矽基流動 (SiliconFlow) API。採用 BAAI/bge-m3 多語言模型進行高精度向量化，大幅降低雲端計算成本。

LLM: 核心推理引擎由 GPT-4 遷移至 DeepSeek-V3 (deepseek-chat)，在處理複雜技術權利要求時展現出極高的性價比與邏輯嚴密性。

現代化 LCEL 架構，完美適配開發環境：

徹底移除過時且易引發兼容性問題的 langchain.chains 模組。

全面採用 LangChain Expression Language (LCEL) 管道語法 (|) 重構 RAG 鏈。項目已完美兼容 Python 3.14 等前瞻性開發環境。

多核並行運算優化：

內置 01_unified_parser.py 統一解析器，利用 multiprocessing.Pool 壓榨多核處理器性能（特別針對 Apple Silicon 進行優化）。實現對 Clarivate TXT 與 USPTO XML 格式海量專利文件的併發秒級解析。

工作站級 GUI 交互體驗：

由單一命令行界面升級為基於 Streamlit 的雙欄 OS 介面。支援左側對話推理、右側 DataFrame 專利原文即時溯源對帳，並加入側欄參數自定義功能。

🛠️ 快速開始 (Quick Start)

1. 環境準備

推薦使用 Python 3.10 - 3.14 環境。

Bash

git clone https://github.com/iStoryOfSpring/IPAgent-OS.git

cd IPAgent-OS

pip install -r requirements.txt

2. 數據解析

將你的專利原始文件 (.txt 或 .xml) 放入 data/ 目錄，然後運行併發解析器：

Bash

python 01_unified_parser.py

此操作將在根目錄生成 parsed_data.csv。

3. 構建向量庫

確保你已配置矽基流動 (SiliconFlow) 的 API Key，然後運行：

Bash

python 02_create_vector.py

此操作將在 embeddings/ 目錄下生成 FAISS 本地索引。

4. 啟動可視化工作站

確保你已配置 DeepSeek API Key，運行主程式：

Bash

streamlit run chatbot.py

📜 許可證 (License)

本項目基於 MIT 許可證開源。詳情請參閱 LICENSE 文件。

🙏 致謝 (Acknowledgments)

感謝 [Matthew Shaxted] 提供的初始架構靈感。

感謝 LangChain, FAISS, DeepSeek, 以及 SiliconFlow 提供的基礎設施。


# Français(French)

IPAgent-OS est une station de travail intelligente d'analyse de brevets basée sur la technologie de Génération Augmentée par Récupération (RAG). Ce projet est un fork de l'IPAgent original de Matthew Shaxted, ayant subi une refonte structurelle profonde et une optimisation de la puissance de calcul, spécifiquement conçu pour l'extraction et la comparaison de brevets dans des domaines techniques complexes.

🚀 Améliorations clés par rapport à la version originale

Découplage complet et adaptation locale du moteur de calcul :

Embedding : Abandon des embeddings OpenAI coûteux au profit de l'API SiliconFlow. Utilisation du modèle multilingue haute précision BAAI/bge-m3 pour la vectorisation, réduisant ainsi considérablement les coûts de calcul cloud.

LLM : Migration du moteur d'inférence principal de GPT-4 vers DeepSeek-V3 (deepseek-chat), offrant un rapport performance/prix exceptionnel et une rigueur logique accrue lors du traitement de revendications techniques complexes.

Architecture LCEL moderne et compatibilité logicielle :

Suppression totale du module obsolète langchain.chains pour éviter les conflits de version.

Adoption complète de la syntaxe LangChain Expression Language (LCEL) (|) pour reconstruire les chaînes RAG. Le projet est parfaitement compatible avec les environnements de développement d'avant-garde comme Python 3.14.

Optimisation du calcul parallèle multi-cœur :

Intégration de l'analyseur unifié 01_unified_parser.py, utilisant multiprocessing.Pool pour maximiser les performances des processeurs multi-cœurs (optimisé spécifiquement pour Apple Silicon). Permet l'analyse simultanée et instantanée de volumes massifs de brevets aux formats Clarivate TXT et USPTO XML.

Interface utilisateur (GUI) de niveau station de travail :

Passage d'une simple interface en ligne de commande à une interface double colonne basée sur Streamlit. Elle permet l'inférence conversationnelle à gauche et la traçabilité immédiate des données sources via un DataFrame à droite, avec personnalisation des paramètres en barre latérale.

🛠️ Démarrage rapide (Quick Start)

1. Préparation de l'environnement

Environnement Python 3.10 - 3.14 recommandé.

Bash

#git clone https://github.com/iStoryOfSpring/IPAgent-OS.git

#cd IPAgent-OS

#pip install -r requirements.txt

2. Analyse des données

Placez vos fichiers originaux de brevets (.txt ou .xml) dans le dossier data/, puis lancez l'analyseur :

Bash

#python 01_unified_parser.py

Cette opération générera un fichier parsed_data.csv à la racine du projet.

3. Construction de la base vectorielle

Assurez-vous d'avoir configuré votre clé API SiliconFlow, puis lancez :

Bash

#python 02_create_vector.py

L'index local FAISS sera généré dans le répertoire embeddings/.

4. Lancement de la station de travail

Configurez votre clé API DeepSeek et lancez le programme principal :

Bash

#streamlit run chatbot.py

📜 Licence

Ce projet est sous licence MIT. Pour plus de détails, veuillez consulter le fichier LICENSE.

🙏 Remerciements

Merci à Matthew Shaxted pour l'inspiration de l'architecture initiale.

Merci à LangChain, FAISS, DeepSeek et SiliconFlow pour les infrastructures fournies.
