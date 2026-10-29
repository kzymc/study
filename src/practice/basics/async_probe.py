from pydantic import BaseModel
from fastapi import FastAPI 
import time
import asyncio
from fastapi.sse import EventSourceResponse


class Metadata(BaseModel):
    source_path:str
    chnk_num:int
    text:str
    heading_path: str|None=None
    char_start:int|None=None
    char_end:int|None=None
app = FastAPI()
# @app.put("/metadata/{metadata_id}")
# def update_metadata(metadata_id:int,metadata:Metadata,q:str|None=None):
#     pass
class Test(BaseModel):
    question:str = "请完成任务1"
class Test2(BaseModel):
    answer:str = "任务1完成"
class Test3(BaseModel):
    stre:str = "power"
@app.get("/test",status_code=200)
def get_test(test:Test = Test(),test1:Test2 = Test2()):
    return test1

@app.post("/chat/{test_id}")
def create_test(test_id:int, test:Test = Test()):
    return {"test_id": test_id, "question": test.question}
@app.get("/test/stream",response_class=EventSourceResponse,)
async def stream():
    for i in Test3().stre:
        yield i



@app.get("/test/hs1")
def hs1():
    time.sleep(5)
    return {"type": "sync", "sleep": 5}
@app.get("/test/hs2")
async def hs2():
    await asyncio.sleep(5)
    return {"type": "async", "sleep": 5}

