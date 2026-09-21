# yaield  from 生成器表达式,isinstance()
import time
from functools import wraps
import re
import jieba
from collections import Counter
list1 = [1,2,3,4,5,[7,8,9],[10,[11,12]]]
filename = "day1.md"
filename1 = "test.txt"
class MyException(Exception):
    time.time()
def timer(func):
    @wraps(func)
    
    def wrapper(*args,**kwargs):
        zong_time = 0
        start = time.time()
        print("开始运行")
        def inner():
            nonlocal zong_time
            yield from func(*args,**kwargs)
            end =time.time()
            zong_time += end-start
            print(f'{func.__name__}从创建到运行结束的时间为：{zong_time:.5f}秒')
            print("结束运行")
        return inner() 
    return wrapper


def generator(list1):
    for item in list1:
        if isinstance(item,list):
            yield from generator(item)
        else:
            print(item)
            yield item
            
@timer
def _generator(list1):
    yield from generator(list1)
def read_file(filename):
    try:
        with open(filename,'r',encoding='utf-8') as f:
            print("文件打开成功")

    except FileNotFoundError:
        print(f"文件{filename}不存在")
def paixu(filename):
    # count = {}
    words = []
    try:
        with open(filename,'r',encoding='utf-8') as f:
            # for word in re.findall(r"\w+",f.read().lower()):
            #     count[word] = count.get(word,0) + 1
            # sorted(count.items(),key=lambda x:x[1],reverse=True)
            tokens = jieba.cut(f.read())
            for i in tokens:
                english =re.findall(r"[a-zA-Z]+", i)
                if english:
                    words.extend(w.lower() for w in english)
                elif re.fullmatch(r"[\u4e00-\u9fff]+$", i):
                    words.append(i)
        return Counter(words).most_common()
    except FileNotFoundError:
        print(f"文件{filename}不存在")
def merge_dict(keys:list,values:list):
    return dict(zip(keys,values))

def test():
    raise MyException("这是一个测试异常")
    
if __name__ == '__main__':
    assert isinstance(list1,list)
    ge=_generator(list1)
    next(ge)
    for item in ge:
        pass
    ge=_generator(list1)
    for item in ge:
        pass
    # read_file(filename1)测试报错
    print(paixu(filename))
    print(merge_dict(["a","b","c"],[1,2,3]))
    print(merge_dict(["a","b","c",'d'],[1,2,3]))
    print(merge_dict(["a","b","a"],[1,2,3]))
    try:
        test()
    except MyException as e:
        print("捕获到的异常为",e)
