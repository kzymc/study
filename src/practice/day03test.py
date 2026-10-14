from pypdf import PdfReader
import os
from dotenv import load_dotenv
load_dotenv()
with PdfReader(os.environ["FILE_PATH_PDF"]) as pdf:
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


