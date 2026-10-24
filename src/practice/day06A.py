from pydantic import BaseModel, Field
from fastapi import FastAPI
from practice.day04 import search
from practice.day05 import get_response,_get_stream_response
from typing import Iterable
from fastapi.sse import EventSourceResponse
from practice.day03 import Metadata

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

def buding_result(request:ChatRequest)->ChatResponse:
    result = search(request.question,request.num)
    context = ""
    citations=[]
    if result:
        for item in result:
            context += f"{item['text']}\n"
            metadata= item["metadata"]
            citations.append(Citation(source_path=metadata["source_path"],chnk_num=metadata["chnk_num"]))
        answer = get_response(system_prompt=f"请你根据知识库回答问题，知识库的内容是关于乌合之众这本书的部分与用户问题相关的内容，若只是库给的不够你判断问题就说不知道，上下文：{context}",
                              user_prompt=request.question)
    else:
        answer = "没有相关上下文"
    return ChatResponse(citations=citations,answer=answer)
def buding_stream_result(request:ChatRequest)->Iterable[str]:
    result = search(request.question,request.num)
    context = ""
    if result:
        for item in result:
            context += f"{item['text']}\n"
        answer = _get_stream_response(system_prompt=f"请你根据知识库回答问题，知识库的内容是关于乌合之众这本书的部分与用户问题相关的内容，若只是库给的不够你判断问题就说不知道，上下文：{context}",
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
