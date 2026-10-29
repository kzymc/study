"""RAG 链路 —— 按数据流顺序排列。

    文档 → chunking.py → vectorstore.py → （检索结果）→ llm.py → 回答

- `chunking.py`     读文件、切块、`Metadata` 契约（源文件/块序号/标题路径/字符区间）
- `vectorstore.py`  embedding + Chroma 入库（批量 upsert）+ `search(query, k)`
- `llm.py`          LLM 调用，含超时/分级重试/异常兜底，支持一次性与流式

⚠️ 依赖：`chunking` 无外部依赖；`vectorstore` 和 `llm` 需要 `.env` 里的
`BGE_BASE_URL` / `BGE_API_KEY` / `OPENAI_*`，否则在 import 阶段就会失败。
"""
