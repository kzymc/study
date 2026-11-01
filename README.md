# practice · 企业文档问答（RAG）

一个从零手写的 RAG 问答链路：**Markdown/PDF 摄入 → 分块 → 向量化 → 检索 → LLM 生成 → API/UI**，
外加一套**自己设计的评测**（45 道题、5 种题型、按原文区间定义标准答案）。

技术栈：Python 3.13 · FastAPI · pydantic · Chroma · OpenAI SDK · tenacity · Streamlit · uv

---

## 数据流

```
data/original/*.md
      │
      ├─ rag/chunking.py      读文件 → 切块 → Metadata(源文件/块序号/标题路径/字符区间)
      │
      ├─ rag/vectorstore.py   get_embedding(bge-m3) → Chroma upsert(批量) ；search(query,k)
      │
      ├─ rag/llm.py           get_response() / _get_stream_response()  超时·分级重试·兜底
      │
      ├─ app/api.py           POST /chat（一次性）· POST /chat/stream（SSE 流式）
      │
      └─ app/ui.py            Streamlit 界面：流式输出 + 引用溯源 + 失败提示

eval/compare_chunking.py      独立脚本：三种分块策略的 Recall@k 对比
```

## 目录

```
practice/
├── NOTES.md              每日记录（含 AI 使用三行）
├── src/practice/
│   ├── rag/              RAG 链路，按数据流排序
│   │   ├── chunking.py       定长 / 按标题 / 按句子 三种分块 + Metadata 契约
│   │   ├── vectorstore.py    embedding + Chroma 入库与检索
│   │   └── llm.py            LLM 调用，超时/重试/异常兜底
│   ├── app/              对外接口
│   │   ├── api.py            FastAPI：/chat 与 /chat/stream（SSE）
│   │   └── ui.py             Streamlit
│   ├── eval/
│   │   └── compare_chunking.py   分块策略对比实验
│   ├── basics/           练手与实验（不进主链路，可删）
│   └── algorithm/        手撕算法
├── data/
│   ├── original/         语料：5 份售后政策
│   └── eval/questions.jsonl   45 道评测题
└── notes/                历史每日记录（day01.md ~ day08A.md）
```

## 跑起来

```powershell
# 0. 依赖（uv 管理）
uv sync

# 1. 配置
Copy-Item .env.example .env
# 填入 BGE_BASE_URL / BGE_API_KEY / BGE_MODEL / OPENAI_*

# 2. embedding 服务（OpenAI 兼容，默认 8005）
python server.py --port 8005

# 3. 后端
uvicorn practice.app.api:app --port 8001

# 4. 界面
streamlit run src/practice/app/ui.py
```

三步顺序不能反：**embedding(8005) → 后端(8001) → UI**。

> ⚠️ 必须在 `practice/` 根目录启动。`vectorstore.py` 和 `compare_chunking.py` 用的是相对路径
> （`./chroma_db` / `./chroma_db_test`），换个目录启动会静默新建一个空库。

## 评测

```powershell
python -m practice.eval.compare_chunking
```

方法要点：

- **标准答案用原文区间/章节名定义，不用 chunk id**——否则 chunk 策略一换，gold 就作废
- Recall 必须和**平均注入上下文字数**一起报，否则放大 k 就能刷分
- 必须包含**语料库里没有的问题**，用来测拒答准确率


