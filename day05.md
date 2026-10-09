## 1.先改day04的错误顺便为自己学习的时间计时2026年10月9日15:27:38

1.先将.gitignore中的.chroma_db/改为了chroma_db/,删掉了最后一行。

2.尝试用vs提交看他会根据忽略文件自动删除吗，结果不会。

尝试用命令行手动删除，成功删除。吃饭2026年10月9日15:42:09

回来了2026年10月9日17:29:38

3.修id生成，我选择用文件路径加块来修如下： ids=f"{chunk.source_path}_{chunk.chnk_num}"

4.更改heading_path为str，将第二次分类时加入标题的方法改为拼接字符串。解决重复存储text。

5.更改硬编码问题，其中发现os.gentenv()在没有读取到内容时会返回空，openai（...）.embeddings.creat(model,input)中的model参数不能是空。

6.在我本地的D:\embedder有包装好的向量化模型，通过venv进入虚拟环境后，再通过命令python server.py --port 8000来启动向量化模型。

7.重构了一下添加addDocument，让他可以批量更新内容和批量向量化，用bath_size来决定批量导入的大小，默认是20.

我将运行成功的部分截图保存为：D:\DSH\DSHprint\屏幕截图 2026-10-09 184559.jpg

8.休息一下2026年10月9日18:49:38



