1.将day01完成后你删除的文件同步到github。

2.先了解下isinstance，yield和from

isinstance（参数，类型）返回boolean

yield，创建生成器对象关键字，要想执行他需要next或for或from。

yield   from  函数。

ok写完第一个任务了，梳理一下学到的知识，yield item 每次调用会输出item

调用next（包含yaield的函数）来消费他每个next消费一次。next（函数）

for循环也可以消费。注意：yaield会更省内存，只有调用时才动然后等待下一次调用。

想法：将嵌套列表中的每个元素打印出来，需要知道for循环会返回迭代器将每个元素提取出来，在提取出来后若还是列表就继续调用自己，将这个列表作为一个新的参数传递给本身。若他不是列表就返回出来。

遇到的问题：在定义新列表时用了关键字list，后改成list1。next（参数）这样调用，不是item.next()调用。

3.写装饰器**一定要加 @wraps(func)**，否则会破坏原函数的元信息。

装饰器实现要不写嵌套函数，要不写类然后用_call_来实现。我写了用嵌套函数实现的方法。整个过程是先写外层函数，再写内层函数然后写开始，将需要计时的函数放在开始和结束中间，然后算出时间差，最后返回内层函数。

4.open（文件路径，模式），try except。得调encoding=utf-8，否则读不了中文文档。

5.分词降序排列现在用到的是sored，re和字典的组合。但是发现re.findall（“模式”，文本）分不了中文文字，正在考虑用jieba库。和python的collections库的Counter。

6.调用dict的.zip方法

7.创建类继承异常类，在一个类中调用这个异常类，用raise在类中主动抛出这个异常，用try，catch补获和处理他。若没有补获和处理的话程序会终止。

附录A（涉及的库和新知识）：

```python
import time   #时间库
from functools import wraps #wraps可以防止元数据被破坏
import re#正则表达式
import jieba#中文分词库
from collections import Counter #计数排序

func(*args,**kwargs)#*任意数量的位置参数，**任意数量的关键字参数 
yield #暂停函数等待下一次调用
yield from 可迭代对象 #将这个可迭代对象的值都逐个yield出来
time.time()#获取当前时间
@wraps#防止元数据被破坏
open（"",'',encoding='utf-8'）#按顺序两个参数文件名和模式我这里只用了‘r’这个模式读。这段代码需要包裹在with里，及时释放资源，还需要encoding='utf-8'，参数来读中文文档.
re.findall("","")，#按顺序两个参数分别为条件和字符串，返回一个列表，他可以将内容提取出来，找出所有匹配的部分。
re.fullmatch("","")#他和上边的参数一样，但他的作用是校验数据。这个是判断全部满足条件。
re.match("","")#这个是看开头是否满足条件。
jieba.cut("")和jieba.lcut("")#参数为字符串一个返回迭代器只能遍历一次，一个返回列表可以遍历很多次
raise#主动抛出异常
try catch#捕获并处理异常让程序不至于崩溃。
dict(zip(key:list,value:list))#将两个列表组合成一个字典。
```

