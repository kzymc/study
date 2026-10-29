#新建测试数据库
#调用方法将测试数据插入数据库
import chromadb
from chromadb.config import Settings
from practice.day04 import addDocument,search
from practice.day03 import chunk_text1,chunk_text2,chunk_text3,read_md
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
from chromadb.api.models.Collection import Collection

load_dotenv()
md=os.environ["FILE_PATH_MD"]
name =["my_kb","my_kb2","my_kb3"]
json_path=os.environ["JSON_PATH"]
pos1=0
pos2=0
pos3=0


def load_json(json_path:Path)->list[dict]:
    json_data=[]
    with open(json_path,"r",encoding="utf-8") as f:

        for line in f:
            line=line.strip()
            if line:
                json_data.append(json.loads(line))
    return json_data
def pd_serch(collection:Collection,json_data:list[dict],pos:int =0,k:int=5,token_number: int=0):
    #{"id":"Q01","type":"exact","answerable":true,"question":"七天无理由退货的 7 天从什么时候开始算？签收当天算吗？",
    # "gold":[["01-退货退款政策.md","七天无理由退货适用范围"]],"keywords":["签收次日","0 点","自然日"]}
    for j in json_data:
        gold=j["gold"]
        question=j["question"]
        gold_source_path=gold[0][0]
        gold_key=gold[0][1]
        cg =False
        for i in search(collection,question,k=k):
            metadata=i.get("metadata")
            text=i.get("text")
            if text:
                token_number+=len(text)
            if metadata:
                source_path=metadata.get("source_path")
                if source_path:
                    if (source_path in gold_source_path) and (gold_key in text):
                        logging.info(f"测试通过")
                        if not cg:
                            pos+=1
                            cg=True
                        
                    else:
                        logging.warning(f"测试失败")
    return pos,token_number                    
    




if __name__ == '__main__':
    _chroma =chromadb.PersistentClient(path="./chroma_db_test",
                                   settings=Settings(anonymized_telemetry=False))
    collection = _chroma.get_or_create_collection(name=name[0],
                                        metadata={"hnsw:space": "cosine"})
    collection2=_chroma.get_or_create_collection(name=name[1],
                                        metadata={"hnsw:space": "cosine"})
    collection3=_chroma.get_or_create_collection(name=name[2],
                                        metadata={"hnsw:space": "cosine"})
   
    for path in Path(md).rglob("*.md"):
        content,path_name=read_md(path)
        chunk=chunk_text1(content,path_name,chunk_size=300,overlap=30)
        chunk1=chunk_text2(content,path_name)
        chunk2=chunk_text3(content,path_name,chunk_size=300)
        addDocument(collection,chunks=chunk)
        addDocument(collection2,chunks=chunk1)
        addDocument(collection3,chunks=chunk2)
    num =35
    json_data= load_json(Path(json_path))[:num]

    k =5
    result1=pd_serch(collection,json_data,k=k)
    result2=pd_serch(collection2,json_data,k=k)
    result3=pd_serch(collection3,json_data,k=k)

    pos1,token_number1=result1
    pos2,token_number2=result2
    pos3,token_number3=result3
    
    call1=pos1/num
    call2=pos2/num
    call3=pos3/num
    
    print("----------------------------------------")
    print("策略         成功数     Recall@ 平均每 平均每题的字符数")
    print(f"定长加重叠    {pos1}        {call1:.4f}    {k}     {token_number1/num:.1f}")
    print(f"按标题       {pos2}        {call2:.4f}    {k}     {token_number2/num:.1f}")
    print(f"按句子       {pos3}        {call3:.4f}    {k}     {token_number3/num:.1f}")

    
