from openai import OpenAI, APIConnectionError,APITimeoutError,RateLimitError,InternalServerError
from tenacity import retry, stop_after_attempt, wait_fixed,before_sleep_log,retry_if_exception_type
import logging

import os
from dotenv import load_dotenv
from typing import Iterable

load_dotenv()
ExceptionType =(APITimeoutError,APIConnectionError,RateLimitError,InternalServerError)
base_url = os.environ["OPENAI_BASE_URL"]
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key, base_url=base_url)
system_prompt=""
user_prompt="你好"
log= logging.getLogger(__name__)

class myException(Exception):
    pass
@retry(retry= retry_if_exception_type(ExceptionType),stop =stop_after_attempt(3),wait=wait_fixed(2),before_sleep=before_sleep_log(log,logging.WARNING),reraise=True,)
def _get_response(system_prompt:str, user_prompt:str,stream:bool=False)->str|None:
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[  
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        
        stream=False,
        reasoning_effort="medium",
        extra_body={"thinking": {"type": "enabled"}} ,
        
    )
    return response.choices[0].message.content

def _get_stream_response(system_prompt:str, user_prompt:str)->Iterable[str]:
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[  
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        
        stream=True,
        reasoning_effort="medium",
        extra_body={"thinking": {"type": "enabled"}} ,
        
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield(chunk.choices[0].delta.content) 
def get_response(system_prompt:str, user_prompt:str,stream:bool=False)->str|None:
    try:
        response = _get_response(system_prompt, user_prompt)
        return response
    except Exception as e:
        raise myException(f"获取响应失败：{e}")from None
    
if __name__ == "__main__":
    response = get_response(system_prompt, user_prompt)
    print(response)
    pass
