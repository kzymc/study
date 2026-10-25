day07收尾：

1.修了缩进，和测试用例，发现list.sort()会返回NONE所以不能return list.sort()得先list.sort()然后再return list

2.那两张图在md中可以渲染不知道在其他地方为什不行了。我看了下github，github也没有渲染出来。github报错为：Unable to render rich display，但是我用了加速器他有显示出来了。在https://mermaid-live-editor.com/zh/里我也成功渲染出来了。所以语法没问题。我把github的生成的图片照片放到photo里边了。

3.改掉了直接导入后端Citation模型的方法，来源格式不用修改，因为我记得第二种分块方式按标题分他会传入一个heading_path,所以我在前边的buding_result（）中为heading_path赋了值。端口报错信息也改成了8005.

4.导出了。

5,我又看了那个开源项目的几个地方，可能是我原先让ai改之后，导致类型约束乱了，但我忘了改了哪些部分，和他们的原来的代码是什么，所以就这样吧。

