from pydantic import BaseModel, Field
from fastapi import FastAPI
from practice.rag.vectorstore import search
from practice.rag.llm import get_response,_get_stream_response
from typing import Iterable
from fastapi.sse import EventSourceResponse
from practice.rag.chunking import Metadata
from practice.rag.vectorstore import collection

class Citation(BaseModel):
    source_path:str = Field(description="引用的文件名")
    chnk_num:int = Field(description="引用的chunk编号")
    heading_path: str|None = Field(default=None,description="引用的标题路径")
    

class ChatRequest(BaseModel):
    question:str = Field(max_length=100,description="用户的问题")
    num:int = Field(default=3,gt=0,le=10,description="用户想返回的结果数量")
class ChatResponse(BaseModel):
    citations:list[Citation] = Field(description="引用的文档")
    answer:str|None =Field(default=None,description="模型的回复")

# Prompt 是契约的一部分：改了语料就必须改它。
# 这里只定义一次，一次性接口和流式接口共用，避免两处漂移。
SYSTEM_PROMPT = """你是企业售后知识库助手。请严格依据【知识库内容】回答用户问题。

规则：
1. 只使用【知识库内容】中的信息作答，不要引入外部常识，不要编造条款、时限或金额。
2. 【知识库内容】不足以回答时，直接回答“知识库中没有相关信息”，不要猜测。
3. 涉及期限、比例、金额、条件时按原文表述，不要改写数字。
4. 回答控制在 3 句话以内。

【知识库内容】
{context}"""


def buding_result(request:ChatRequest)->ChatResponse:
    result = search(collection,request.question,request.num)
    context = ""
    citations=[]
    if result:
        for item in result:
            context += f"{item['text']}\n"
            metadata= item["metadata"]
            citations.append(Citation(source_path=metadata["source_path"],chnk_num=metadata["chnk_num"],heading_path=metadata["heading_path"]))
        answer = get_response(system_prompt=SYSTEM_PROMPT.format(context=context),
                              user_prompt=request.question)
    else:
        answer = "没有相关上下文"
    return ChatResponse(citations=citations,answer=answer)
def buding_stream_result(request:ChatRequest)->Iterable[str]:
    result = search(collection,request.question,request.num)
    context = ""
    if result:
        for item in result:
            context += f"{item['text']}\n"
        answer = _get_stream_response(system_prompt=SYSTEM_PROMPT.format(context=context),
                              user_prompt=request.question)
        for i in answer:
            yield i

        
app = FastAPI()
@app.post("/chat")
def chat(request:ChatRequest)->ChatResponse:
    return buding_result(request)
@app.post("/chat/stream",response_class=EventSourceResponse)
def chat_stream(request:ChatRequest)->Iterable[str]:
    for i in buding_stream_result(request):
        yield i
