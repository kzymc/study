"""practice —— 企业文档问答（RAG）。各子包职责见其 `__init__.py`：
`rag/`（链路）· `app/`（接口）· `eval/`（评测）· `basics/`（练手）· `algorithm/`（手撕）
"""

from pathlib import Path

# 仓库根目录（即 practice/ 本身）。
# 运行时产物（Chroma 库）一律基于它定位，不要用 "./chroma_db" 这类相对路径——
# 否则换一个目录启动就会静默新建一个空库，表现为"检索不到东西但不报错"。
REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    print("Hello from practice!")
