import os
import litellm

from ulib.utils.env_reader import read_deepseek_api_key

os.environ['DEEPSEEK_API_KEY'] = read_deepseek_api_key()

try:
    response = litellm.completion(
        # base_url="https://api.deepseek.com/v1",
        # api_key=read_deepseek_api_key(),
        model = "deepseek/deepseek-chat",
        messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ]
    )

    print(response.choices[0].message.content)

except Exception as e:
    print(f"发生错误: {e}")
