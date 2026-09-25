from pypdf import PdfReader
with PdfReader('d:\DSH\DSHprint\乌合之众：大众心理研究（畅销125年纪念版）.pdf')as pdf:
    print("------------------迭代对象输出内容------------------")
    page=pdf.pages[1]
    print(page.extract_text())
    it=iter(pdf.pages)
    print("------------------迭代器输出内容------------------")
    print(next(it))
    print(next(it).extract_text())

with open('day02.md','r',encoding='utf-8') as f:
    content=f.read()
    print(content)


