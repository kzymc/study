更改一下day03的错误。

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

