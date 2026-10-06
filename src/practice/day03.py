from pypdf import PdfReader
import re
from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()
file_path_pdf=os.getenv("FILE_PATH_PDF")
file_path_md=os.getenv("FILE_PATH_MD")
def read_pdf(file_path,page=1):
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
    chnk_num:int
    text:str
    heading_path: list[str]|None=None
    char_start:int|None=None
    char_end:int|None=None
    
#已知文本大约9.4万个字，
def chunk_text1(text,file_path,chunk_size=1000,overlap=100,):
    chunks = []
    setup = chunk_size-overlap
    num=1
    for i in range(0,len(text),setup):
        chunk = text[i:i+chunk_size]
        if chunk:
            chunks.append(Metadata(source_path=file_path,char_start=i,char_end=min(i+chunk_size,len(text)),chnk_num=num,text=chunk))
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
            chunks.append(Metadata(source_path=file_path,heading_path=current_heading,chnk_num=num,text=current))
            num+=1
            
    for line in lines:
        m=re.match(rf"^(#{{1,{max_level}}})\s+(.*)$",line)#rf"^(#{{1,{max_level}}})\s+(.*)$"
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
def chunk_text3(text,file_path,lentext=1,chunk_size=1000):
    sentences=re.split(r"(?<=[.?!。！？])\s*",text)
    sentences=[sentence.strip() for sentence in sentences if sentence.strip()]
    chunks=[]
    chunk_text=""
    def flush():
        nonlocal chunk_text
        if chunk_text:
            chunks.append(Metadata(source_path=file_path,chnk_num=lentext,text=chunk_text))
            chunk_text=""
    for sentence in sentences:
        if len(chunk_text)+len(sentence)>chunk_size:
            flush()
            lentext+=1
        chunk_text+= sentence
        
    flush()
    return chunks
    

if __name__ == '__main__':
    # print(read_pdf(file_path_pdf,2))
    # print(chunk_text1(read_md(file_path_md),file_path_md)[0])
    print(chunk_text2(read_md(file_path_md),file_path_md)[5])
    # print(chunk_text3(read_md(file_path_md),file_path_md)[0])
    
