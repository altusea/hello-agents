from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from ulib.utils.env_reader import read_deepseek_api_key

## 为了更好的安全性，从 .env 文件加载环境变量
## from dotenv import load_dotenv
## load_dotenv()
## 确保你的 OPENAI_API_KEY 在 .env 文件中设置

## 初始化语言模型（推荐使用 ChatOpenAI）
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=1.3,
    api_key=read_deepseek_api_key(),
    base_url="https://api.deepseek.com/v1",
)

## --- 提示词 1：提取信息 ---
prompt_extract = ChatPromptTemplate.from_template("从以下文本中提取技术规格：\n\n{text_input}")

## --- 提示词 2：转换为 JSON ---
prompt_transform = ChatPromptTemplate.from_template(
    "将以下规格转换为 JSON 对象，使用 'cpu'、'memory' 和 'storage' 作为键：\n\n{specifications}"
)

## --- 利用 LCEL 构建处理链 ---
## StrOutputParser() 将 LLM 的消息输出转换为简单字符串。
extraction_chain = prompt_extract | llm | StrOutputParser()

## 完整的链将提取链的输出传递到转换提示词的 'specifications' 变量中。
full_chain = {"specifications": extraction_chain} | prompt_transform | llm | StrOutputParser()

## --- 运行链 ---
input_text = "新款笔记本电脑型号配备 3.5 GHz 八核处理器、16GB 内存和 1TB NVMe 固态硬盘。"

## 使用输入文本字典执行链。
final_result = full_chain.invoke({"text_input": input_text})

print("\n--- 最终 JSON 输出 ---")
print(final_result)
