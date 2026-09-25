from pypdf import PdfReader
import re
from dataclasses import dataclass
file_path_pdf="d:/DSH/DSHprint/乌合之众：大众心理研究（畅销125年纪念版）.pdf"
file_path_md="D:/DSH/DSHprint/practice/aipyda/乌合之众_第一卷起.md"
def read_pdf(file_path,page=1):
    txt =""
    i=0
    with PdfReader(file_path)as pdf:
        txt=pdf.pages[page].extract_text()

    return txt
def read_md(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        content=f.read()
    return content
@dataclass
class Metadata:
    source_path:str
    title:str
    chnk_num:int
    text:str
#已知文本大约9.4万个字，
def chunk_text1(text,file_path,chunk_size=1000,overlap=100,):
    chunks = []
    setup = chunk_size-overlap
    num=1
    for i in range(0,len(text),setup):
        chunk = text[i:i+chunk_size]
        if chunk:
            chunks.append(Metadata(source_path=file_path,title=f'现在是第%d到%d的块'%(i,i+1000),chnk_num=num,text=chunk))
            num+=1
    return chunks
def chunk_text2(text,file_path,max_level =2):
    chunks = []
    lines =text.splitlines()
    current_heading = []
    current_content = []
    num=1
    def flush():
        if current_heading or current_content:
            nonlocal num
            current=">".join(current_heading)+"\n"+"\n".join(current_content).strip()
            chunks.append(Metadata(source_path=file_path,title=current_heading,chnk_num=num,text=current))
            num+=1
            
    for line in lines:
        m=re.match(rf"^(#{{1,{max_level}}})\s+(.*)$",line,max_level)#rf"^(#{{1,{max_level}}})\s+(.*)$"
        if m:
            flush()
            level=len(m.group(1))
            title=m.group(2).strip()
            current_heading = current_heading[:level -1]
            current_heading.append(title)
            current_content = []
        else:
            current_content.append(line.strip())
    flush()
    return chunks
def chun_text3(text,file_path,lentext=1,):
    sentences=re.split(r"(?<=[.?!。！？])\s*",text)
    sentences=[sentence.strip() for sentence in sentences if sentence.strip()]
    chunks=[]
    for sentence in sentences:
        chunks.append(Metadata(source_path=file_path,title=f'现在是第{lentext}个句子',chnk_num=lentext,text=sentence))
        lentext+=1
    return chunks
    

if __name__ == '__main__':
    print(read_pdf(file_path_pdf,2))
    # print(chunk_text1(read_md(file_path_md),file_path_md)[0])
    # print(chunk_text2(read_md(file_path_md),file_path_md)[0])
    # print(chun_text3(read_md(file_path_md),file_path_md)[0])
    
