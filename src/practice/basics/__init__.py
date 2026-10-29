"""Python 手感与实验台 —— 不进主链路，随时可以删。

这些文件不是 RAG 流水线的一部分，是"练手/验证"留下的：

- `health.py`         第一个 FastAPI：`GET /health` 返回 `{"ok": true}`
- `python_drills.py`  生成器 / 装饰器 / 异常 / 词频统计
- `pdf_probe.py`      pypdf 的 pages 迭代行为验证
- `async_probe.py`    同步阻塞 vs async 的并发实测（`/test/hs1` vs `/test/hs2`）
"""
