import chromadb
from chromadb.config import Settings
from openai import OpenAI
from practice.day03 import chunk_text1,file_path_md,read_md,Metadata
from typing import overload
from dataclasses import asdict
from dotenv import load_dotenv
from chromadb.api.types import Embeddings
from typing import cast
load_dotenv()
import os

client = OpenAI(
    base_url=os.getenv("BGE_BASE_URL"),
    api_key=os.getenv("BGE_API_KEY"),
)

@overload
def get_embedding(query:str)->list[float]:
    pass
@overload
def get_embedding(query:list[str])->list[list[float]]:
    pass

def get_embedding(query:str|list[str]):
    
    model=os.getenv("BGE_MODEL","bge-m3")
    resp =client.embeddings.create(
        model=model,
        input=query,
    )
    vecs=[item.embedding for item in resp.data]
    
    return vecs[0] if isinstance(query,str) else vecs
#chromadb的初始化，和创建collection
_chroma =chromadb.PersistentClient(path="./chroma_db",
                                   settings=Settings(anonymized_telemetry=False))
collection = _chroma.get_or_create_collection(name="my_kb",
                                       metadata={"hnsw:space": "cosine"})

def addDocument(chunks:list[Metadata],batch_size:int=20):
    documents=[]
    ids=[]
    metadatas=[]
    embeddings=[]
    def flush():
        nonlocal documents,ids,metadatas,embeddings
        if documents:
            embeddings = get_embedding(documents)
            collection.upsert(
                documents=documents,
                embeddings=cast(Embeddings,embeddings),
                ids=ids,
                metadatas=metadatas,
            )
            print(f"已添加{len(documents)}条文档现在总共有{collection.count()}条文档")
            documents=[]
            ids=[]
            metadatas=[]
            embeddings=[]        
    for chunk in chunks:
        documents.append(chunk.text)
        ids.append(f"{chunk.source_path}_{chunk.chnk_num}")
        metadatas.append({k: v for k, v in asdict(chunk).items() if k != "text"})
        if len(documents) >= batch_size:
            flush()
    flush()
    


def search(query: str, k: int = 3):
    # 1. 查询文本转向量
    query_vec = get_embedding(query)

    # 2. 检索
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    documents=results["documents"]
    metadatas=results["metadatas"]
    distances=results["distances"]
    if not documents or not metadatas or not distances:
        return print("未检索到相关文档")
    hits =[]
    for doc, meta, dist in zip(
        documents[0],
        metadatas[0],
        distances[0],
    ):
        hits.append({
            "text": doc,
            "metadata": meta,
            "distance": dist,
            "similarity": 1 - dist,     # 余弦距离 → 相似度
        })
    return hits
if __name__ == '__main__':
    chunks=chunk_text1(read_md(file_path_md),file_path_md)
    addDocument(chunks)
    print(search("乌合之众讲了什么"))
