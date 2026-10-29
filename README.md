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

所有运行时路径（Chroma 库、`.env`）都基于 `practice.REPO_ROOT` 解析，**从任何目录启动都指向仓库根**，
不会因为你 `cd` 到了别的地方就静默新建一个空库。

## 评测

```powershell
python -m practice.eval.compare_chunking
```

方法要点：

- **标准答案用原文区间/章节名定义，不用 chunk id**——否则 chunk 策略一换，gold 就作废
- Recall 必须和**平均注入上下文字数**一起报，否则放大 k 就能刷分
- 必须包含**语料库里没有的问题**，用来测拒答准确率

## 已知限制（⚠️ 投递前应逐条修完或删除本节）

### ✅ 2026-10-29 已修

| 问题 | 修法 |
|---|---|
| `app/api.py` 的 system prompt 写着"关于乌合之众这本书"，与售后政策语料不符 | 抽成模块级 `SYSTEM_PROMPT`，一次性与流式接口共用；改成通用售后知识库指令，并加"库中没有就直说"的拒答规则 |
| `vectorstore.py` / `compare_chunking.py` 用 `"./chroma_db"` 相对路径 | 统一走 `practice.REPO_ROOT`（基于 `__file__`）。已验证：从 `D:\`、`practice\src\` 启动都不会在本地新建库 |
| `load_dotenv()` 依赖 CWD 向上查找 | 改为 `load_dotenv(REPO_ROOT / ".env")`，5 个模块统一 |

### 🔧 待办

| # | 问题 | 影响 | 处置 |
|---|---|---|---|
| 1 | `chunk_text2` 用 `current_heading[:level-1]` 对 **str** 做字符切片 | 得到 `">>七天无理由"` 这类**带前导 `>`、且父级标题丢失**的 `heading_path`，前缀还会混进正文 → 该策略的对比数字不可用 | 按 v2 计划**删除该函数**（分块对比交给 Dify，自研只留定长） |
| 2 | `chunk_text3` 的 `char_start` / `char_end` 从 **1** 开始 | 按区间还原原文会偏 1 个字符 | 改成 0 基 |
| 3 | 本地 embedding 服务启动脚本 `server.py` 缺失 | 链路断在第一步（`day04` 之后全部跑不起来） | 重写（约 40 行，OpenAI 兼容 `POST /v1/embeddings`） |

> 顺带记录一个已确认的正确项：`chunk_text1` 的 `char_start` 是 **0 基**（`char_start=i`），这块没问题。

## 开发规范

- 每天在 `NOTES.md` 记一条，含 **AI 使用三行**（让它做了什么 / 它哪错了 / 我怎么发现的）
- 写代码分三级：**L1 闭卷自己写**（核心逻辑、失败路径）· **L2 AI 写我审查**（胶水、样板）· **L3 直接抄**（配置模板，抄完必须跑通并改一处）
- 判据只有一条：**AI 写错了，我能不能发现？** 不能 → 必须自己写
