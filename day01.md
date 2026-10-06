1.今天将我明文配置所用的api删掉了，重新创建了一个。

2.成功激活了cs-agent的venv。对git一筹莫展。选择用ai来获取到git的常用命令和使用方式。了解到了git是一个版本控制工具，支持时间回溯，多人协作。

3.现在正式使用了git，知道了代码上的时间戳是怎么来的。使用的命令是：git config --global user.name

4。通过再当前环境中初始化git init 和 创建了俩个新文件.env和.test11.txt和命令git statue来测试.gitignore的作用。

5.通过add和commit协同将除了gitignore忽略的文件都提交了一次命令为 git commit -m "尝试"

6.发现git add若上传了一个已有文件。git status并不会显示

7.创建分支后，更改t2.txt文件后，没有add就提交了，导致合并分支失败。

附录A

```cmd
git init 初始化   

.gitignore 忽略文件的配置文件

 git status 查看提交状态

git add 添加想要提交的内容

git commit -m “为提交操作命名”

git log --oneline 提交的操作

git switch -c <分支名> 创建分支

git switch <分支名>切换分支

git branch 分支列表
git branch -m main修改分支名

git merge <分支b> 合并分支
git remote add origin git@github.com:kzymc/study.git 关联新的仓库
git remote -v 确认仓库地址
git push -u origin main 推送
git rm --cached 文件名 删除仓库保留本地文件
git ls-files 查看已追踪的文件
```



8.ssh生成公钥和私钥

```cmd
1.ls -al ~/.ssh我用的 dir %USERPROFILE%\.ssh 查找密钥
2.ssh-keygen -t ed25519 -C "你的邮箱@example.com" 创建密钥
3.cat ~/.ssh/id_ed25519.pub 我用的 type %USERPROFILE%\.ssh\id_ed25519.pub 打开密钥文件夹复制公共密钥 ，手动粘贴到github的setting的ssh
4.git pull origin main --allow-unrelated-histories 合并远程历史
5.git push -u origin main 推送  origin后边跟的是 分支或主干名。 

```

9.[kzymc/GitDemo](https://github.com/kzymc/GitDemo)最后完成任务的地址。

10.查询官方的fastapi文档，完成了最后一个任务并将代码放到了day01.py里边。

```cmd
uvicorn day01:app --reload reload是自动重启，当你更改了代码后。fastapi相关。
```