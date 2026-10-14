## 收拾day05的遗留问题

2026年10月12日18:47:50

1.reasoing_effort和think。将extra_body={"thinking": {"type": "disabled"}}中的thinking由disabled转为enabled后发现他的response里多了一个reasoing_content和reasoing_tokens.

经过试验是可以发现extra_body中的thnking是开关，reasoing_effort是调思考强度的。

2.修了file中的l。将os.getenv()换成了os.environ[].

第一个方法只能读取，不存在返回none。

第二个方法可以赋值，删除，遍历。改变数据的操作只会对当前进程和子进程有效，不会影响环境变量。与第一不同的是不存在他会抛出KeyError。

3.我的embedding是本地服务并不是所有人都有的，所以我在笔记中说明了这点并提供了解决方法

4.为day05增加新的附录。休息2026年10月12日19:20:01。