"""对外接口 —— 把 rag/ 暴露成人能用的东西。

- `api.py`  FastAPI：`POST /chat`（一次性）+ `POST /chat/stream`（SSE 流式）
- `ui.py`   Streamlit：消费上面前端，带失败提示与状态面板

启动顺序：embedding 服务(8005) → api(8001) → ui(8501)
"""
