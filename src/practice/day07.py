

import json
from collections.abc import Iterator

import httpx
import streamlit as st
from pydantic import BaseModel, Field


class Citation(BaseModel):
    source_path:str = Field(description="引用的文件名")
    chnk_num:int = Field(description="引用的chunk编号")
    heading_path: str|None = Field(default=None,description="引用的标题路径")
BACKEND = "http://127.0.0.1:8001" 

st.set_page_config(page_title="知识库问答", page_icon="📚", layout="centered")
st.title("📚 知识库问答")
st.caption("Streamlit 最简 UI · 后端 FastAPI + 本地 bge + Chroma")

with st.sidebar:
    st.header("设置")
    stream_mode = st.toggle("流式输出（逐字）", value=True)
    top_k = st.slider("检索条数 top_k", 1, 10, 3)
    st.divider()
    st.caption(f"后端：`{BACKEND}`")
    st.caption("顺序：embedding(8005) → 后端(8001) → UI")

# ─────────────────────────────────────────────────────────────
# 【关键概念 1】Streamlit 每次交互都会从头重跑整个脚本。
# 所以任何要"记住"的东西（聊天历史）必须放进 st.session_state，
# 否则你一发消息，之前的历史就没了。
# ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


def render_message(msg: dict) -> None:
    """把一条消息画出来（含引用）。"""
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        cits = msg.get("citations") or []
        if cits:
            with st.expander(f"📎 {len(cits)} 条来源"):
                for i, c in enumerate(cits, 1):
                    st.markdown(f"**{i}.** {c}")


# 先把历史画出来（注意：必须放在处理新输入之前，否则会重复显示）
for m in st.session_state.messages:
    render_message(m)


# ─────────────────────────────────────────────────────────────
# 【关键概念 2】SSE 的解析
# 后端 yield 裸字符串 → FastAPI 会 JSON 编码 → 线上是  data: "你"（带引号）
# 若后端改用 ServerSentEvent(raw_data=...) → 线上是  data: 你（不带引号）
# 下面这个函数两种都能处理，所以你后端怎么改它都不会坏。
# ─────────────────────────────────────────────────────────────
def parse_sse_line(line: str) -> str | None:
    if not line.startswith("data:"):
        return None          # event: / id: / :注释 / 空行 —— 都跳过
    payload = line[5:].strip()
    if not payload:
        return None
    try:
        value = json.loads(payload)   # data: "你"  → 你
    except json.JSONDecodeError:
        value = payload              # data: 你    → 你
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def iter_stream(question: str) -> Iterator[str]:
    """
    流式：连后端 SSE，边收边吐。

    【关键概念 3】st.write_stream() 会直接消费这个生成器，
    一边收一边往页面写，最后返回拼好的完整字符串。
    你不需要自己管"逐字显示"的动画 —— 这就是 Streamlit 替你做掉的部分。
    """
    with httpx.Client(timeout=None) as client:   # 流式不能设总超时，否则长回答会被切断
        with client.stream(
            "POST", f"{BACKEND}/chat/stream",
            json={"question": question, "num": top_k},   
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                text = parse_sse_line(line)
                if text:
                    yield text


def fetch_once(question: str) -> tuple[str, list[str]]:
    """非流式：一次拿完整答案 + 引用。DAY 7 演示时这个更值钱，因为引用能显示出来。"""
    r = httpx.post(f"{BACKEND}/chat", json={"question": question, "num": top_k}, timeout=120)
    r.raise_for_status()
    data = r.json()                      
    answer = data.get("answer") or "没拿到答案"

    citations=[] 
    for item in data.get("citations") or []:
        source_path=item.get("source_path") or ""
        chnk_num = item.get("chnk_num") or 0
        heading_path = item.get("heading_path") or ""
        citations.append(Citation(source_path=source_path, chnk_num=chnk_num, heading_path=heading_path))
    return answer, citations


# ─────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────
if prompt := st.chat_input("问点什么…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            if stream_mode:
                answer = st.write_stream(iter_stream(prompt))
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                with st.spinner("检索 + 生成中…"):
                    answer, citations = fetch_once(prompt)
                st.markdown(answer)
                if citations:
                    with st.expander(f"📎 {len(citations)} 条来源"):
                        for i, c in enumerate(citations, 1):
                            st.markdown(f"**{i}.** {c}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "citations": citations}
                )

        # ─── 失败契约（UI 层）─────────────────────────────────
        # 后端没起的时候，给一条看得懂的提示，而不是一坨 traceback。
        # 面试官/同事第一次跑你的项目，90% 会撞到这里。
        except httpx.ConnectError:
            st.error(
                f"连不上后端 `{BACKEND}`。按顺序检查两个服务：\n\n"
                f"1. **embedding 服务**：`python server.py --port 8005`\n"
                f"2. **后端服务**：`uvicorn practice.day06A:app --port 8001`\n\n"
                f"（两个都起了还连不上，看后端终端有没有报错）"
            )
        except httpx.HTTPStatusError as e:
            st.error(f"后端返回 {e.response.status_code}：{e.response.text[:300]}")
