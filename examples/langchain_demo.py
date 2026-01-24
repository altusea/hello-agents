"""
LangChain 基础示例
演示如何使用 LangChain 调用 LLM、构建 Prompt 和创建简单的 Chain
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()


def basic_llm_call():
    """基础 LLM 调用示例"""
    print("=" * 50)
    print("1. 基础 LLM 调用")
    print("=" * 50)

    # 创建 LLM 模型 (使用 DeepSeek API，兼容 OpenAI 接口)
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )

    # 调用模型
    messages = [
        SystemMessage(content="你是一个乐于助人的助手。"),
        HumanMessage(content="请用一句话介绍你自己。"),
    ]

    response = llm.invoke(messages)
    print(f"模型回复: {response.content}")
    print()


def chain_example():
    """使用 LCEL 构建 Chain 示例"""
    print("=" * 50)
    print("2. 使用 LCEL 构建 Chain")
    print("=" * 50)

    # 创建 LLM 模型
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )

    # 创建 Prompt 模板
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专业的翻译助手。"),
            ("human", "请将以下英文翻译成中文: {text}"),
        ]
    )

    # 创建输出解析器
    output_parser = StrOutputParser()

    # 使用 LCEL 构建 Chain
    chain = prompt | llm | output_parser

    # 调用 Chain
    result = chain.invoke({"text": "Hello, LangChain!"})
    print(f"翻译结果: {result}")
    print()


def streaming_example():
    """流式输出示例"""
    print("=" * 50)
    print("3. 流式输出示例")
    print("=" * 50)

    # 创建 LLM 模型
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "用3句话描述人工智能的发展趋势。"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    print("流式输出: ", end="", flush=True)
    for chunk in chain.stream({}):
        print(chunk, end="", flush=True)
    print("\n")


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("LangChain Demo")
    print("=" * 50 + "\n")

    basic_llm_call()
    chain_example()
    streaming_example()

    print("=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
