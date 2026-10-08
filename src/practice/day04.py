import chromadb
from chromadb.config import Settings
from openai import OpenAI
from practice.day03 import chunk_text1,file_path_md,read_md,Metadata
from typing import overload
from dataclasses import asdict
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-",#本地服务
)

@overload
def get_embedding(query:str)->list[float]:
    pass
@overload
def get_embedding(query:list[str])->list[list[float]]:
    pass

def get_embedding(query:str|list[str]):
    resp =client.embeddings.create(
        model="bge-m3",
        input=query,
    )
    vecs=[item.embedding for item in resp.data]
    
    return vecs[0] if isinstance(query,str) else vecs
#chromadb的初始化，和创建collection
_chroma =chromadb.PersistentClient(path="./chroma_db",
                                   settings=Settings(anonymized_telemetry=False))
collection = _chroma.get_or_create_collection(name="my_kb",
                                       metadata={"hnsw:space": "cosine"})

def addDocument(chunks:list[Metadata]):
    for chunk in chunks:
        document=chunk.text
        ids=f"my_kb{chunk.chnk_num}"
        metadatas =asdict(chunk)
        embeddings = get_embedding(document)
        collection.upsert(
            documents=document,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )
        print(f"写入{ids}条,当前总数{collection.count()}")

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
