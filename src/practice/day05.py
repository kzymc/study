from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed,before_sleep_log
import logging

import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("OPENAI_BASE_URL")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=base_url)
system_prompt=""
user_prompt="你好"
log= logging.getLogger(__name__)
class myException(Exception):
    pass
@retry(stop =stop_after_attempt(3),wait=wait_fixed(2),before_sleep=before_sleep_log(log,logging.WARNING),reraise=True,)
def _get_response(system_prompt:str, user_prompt:str):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[  
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "disabled"}}
    )
    return response.choices[0].message.content
def get_response(system_prompt:str, user_prompt:str):
    try:
        response = _get_response(system_prompt, user_prompt)
        return response
    except Exception as e:
        raise myException(f"获取响应失败：{e}")from None
    
if __name__ == "__main__":
    response = get_response(system_prompt, user_prompt)
    print(response)
    pass
