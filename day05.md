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

## 2.开始day05的内容2026年10月9日21:09:24

1.安装tenacity这个包，先跟网页版ai了解相关知识，知道了tenacity是一个可以让程序更加健壮的库，在遇到异常时重试，暂时了解到的参数是，可以设定重试次数，和重试时间，和每次重试等待的时间。

2.参照deepseek的兼容openai的教程，成功返回对话。

3.定义prompt模板，tenacity因为网络原因官方网站进不去，所以问ai

4.消化一波知识，首先tenacity在函数外包@retry，他里边的参数分为重试策略，重试次数，重试时间，日志管理，异常抛出选项。

5.一些关于logging的内容，loggging包主要是用来设置日志级别。和搞一些日志参数。

6.故意填错api_key通过from None切断让他只显示我的报错信息。然后改回正确的api。

7.今天就到这里吧2026年10月9日22:20:56。

## 附录A:@retry的参数

| 参数名                 | 类型       | 默认值                        | 作用                                                         |
| ---------------------- | ---------- | ----------------------------- | ------------------------------------------------------------ |
| `sleep`                | Callable   | `tenacity.nap.sleep`          | 自定义睡眠函数，一般无需修改                                 |
| **stop**               | StopBaseT  | **stop_never**                | **停止重试的条件**（如最大次数、总时长），默认永不停止       |
| **wait**               | WaitBaseT  | **wait_none**                 | **每次重试前的等待策略**（如固定间隔、指数退避），默认不等待 |
| **retry**              | RetryBaseT | **retry_if_exception_type()** | **判断哪些异常触发重试**，默认对任何 `Exception` 都重试      |
| `before`               | Callable   | `before_nothing`              | 每次重试尝试**前**执行的回调                                 |
| `after`                | Callable   | `after_nothing`               | 每次重试尝试**后**执行的回调                                 |
| **before_sleep**       | Callable   | **None**                      | **等待前**执行的回调（常用于记录日志）                       |
| **reraise**            | bool       | **False**                     | 重试耗尽后，是否**抛出原始异常**。`False` 则抛出 `RetryError` |
| `retry_error_cls`      | Type       | `tenacity.RetryError`         | `reraise=False` 时抛出的异常类型                             |
| `retry_error_callback` | Callable   | `None`                        | 重试耗尽后的回调，可**自定义返回值**而非抛出异常             |

## 附录B:常见错误代码

| 类型             | 例子                         | 重试有用吗   | 该重试   |
| ---------------- | ---------------------------- | ------------ | -------- |
| **网络问题**     | `ConnectionError`、`Timeout` | ✅ 可能恢复   | **要**   |
| **限流**         | 429 Too Many Requests        | ✅ 等一会再试 | **要**   |
| **服务端错误**   | 500、502、503、504           | ✅ 可能恢复   | **要**   |
| **请求错误**     | 400 Bad Request              | ❌ 重试还是错 | **不要** |
| **认证失败**     | **401 Unauthorized**         | ❌ 重试还是错 | **不要** |
| **权限不足**     | 403 Forbidden                | ❌ 重试还是错 | **不要** |
| **资源不存在**   | 404 Not Found                | ❌ 重试还是错 | **不要** |
| **参数校验失败** | 422 Unprocessable            | ❌ 重试还是错 | **不要** |

**OpenAI SDK 的异常类型**：

| 异常                       | 对应 HTTP | 重试 |
| -------------------------- | --------- | ---- |
| `APIConnectionError`       | 连接问题  | ✅    |
| `APITimeoutError`          | 超时      | ✅    |
| `RateLimitError`           | **429**   | ✅    |
| `InternalServerError`      | **5xx**   | ✅    |
| `AuthenticationError`      | **401**   | ❌    |
| `PermissionDeniedError`    | **403**   | ❌    |
| `BadRequestError`          | **400**   | ❌    |
| `NotFoundError`            | **404**   | ❌    |
| `UnprocessableEntityError` | **422**   | ❌    |