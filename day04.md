## 更改一下day03的错误。

1.测试时注释后忘取消，已更改

2.修改契约：将原有的Metadata中的title删除，创建了三个字段heading_path,char_start,char_end.char_num.

chunk_text3直接以块分不需要给标题什么的了。

3.重新设置了chun_text3的分块逻辑

4.删掉了re.match的第三个参数

5.取消了chun_text1的硬编码改用其他形式的。

6.解决了版权风险。

7.删掉了ai写的数据清洗代码。

8.将文件的硬编码放入了env里

9.小问题中只更正了day03相关的内容。其中chunk_text2中确实有只有标题的块。

## 开始day04的任务。

1.首先添加openai和chroma依赖。

2,用本地api来调用向量模型

3.在写入id / 文档 / 向量 / metadata，时只传入metadata组成的列表，因为metadata中有id有文档和metadata

4,在VS中开了类型检查后，原来我以为collection是一个集合，他的add功能是什么都可以加，但类型检查告诉我该传入的参数和数据类型。若是不按照包规定的方式传入数据，是否会导致意想不到的错误？

5.可以通过typing的@ovelop注解实现类的复用。

6.在持久化存储的时候，得防止重复创建数据库，重复存数据的情况。

7.在gitignore中加入我新创建的.chroma_db/.

8.尝试用vs自带的功能去上传github。

## 附录：



```python
#用到的库
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from practice.day03 import chunk_text1,file_path_md,read_md,Metadata
from typing import overload
from dataclasses import asdict
#chromadb的核心api
#持久化到本地
_chroma = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False),#这一行不知道有什么用
)
#集合
collection = _chroma.get_or_create_collection(
    name="my_kb",
    metadata={"hnsw:space": "cosine"},#hnsw:space距离度量方式
)
#入库
collection.add(...)          # id 重复会报错
collection.upsert(...)       # id 存在则覆盖
# 查询
collection.query(query_embeddings=[...], n_results=k, include=[...])#第一个参数需要向量查询的文字，第二个参数返回内容的数量，第三个参数返回的字段
# 按 id 取
collection.get(ids=[...])

# 统计
collection.count()

# 管理
_chroma.list_collections()
_chroma.delete_collection(name="my_kb")

```

| #    | 坑                                               | 报错 / 现象                                    | 解决                                        |
| ---- | ------------------------------------------------ | ---------------------------------------------- | ------------------------------------------- |
| 1    | 猜测用 `create_collection` 重复运行              | `Collection [my_kb] already exists`            | 改用 **get_or_create_collection**           |
| 2    | 以为每次运行会重建 `chroma_db`                   | 数据一直在，报 already exists                  | **PersistentClient 是"有就复用"**，不是重建 |
| 3    | `ids` 传了 int                                   | 类型检查报"int 不可分配给 str"                 | 用f-string将int拼接成字符串。               |
| 4    | `metadatas` 传 `list[Metadata]`（dataclass）     | 类型检查报"Metadata 与 chromadb Metadata 不同" | **用 asdict() 转成 list[dict]**             |
| 5    | metadata 里有 `list` 值（如 `title: list[str]`） | Chroma 不接受嵌套列表                          | **转成字符串** f                            |
| 6    | `results["documents"]` 类型是 `Optional`         | 类型检查报"None 不可下标"                      | 加判断语句，在为空时结束这个函数。          |
| 7    | 以为 `QueryResult` 是对象                        | 用 `.documents` 报错                           | **看源代码发现他继承了字典类所以他是字典**  |