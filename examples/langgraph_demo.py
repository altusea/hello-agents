"""
LangGraph 基础示例
演示如何使用 LangGraph 构建有状态的工作流
"""

import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

# 加载环境变量
load_dotenv()


# 1. 定义状态
class AgentState(TypedDict):
    """定义工作流的状态"""

    messages: Annotated[list[str], "消息历史"]
    step: str  # 当前步骤


# 2. 定义节点函数
def node_a(state: AgentState) -> AgentState:
    """第一个节点: 生成问题"""
    print(f"[Node A] 生成问题... step={state.get('step', 'start')}")
    return {"messages": state["messages"] + ["问题: 什么是 LangGraph?"], "step": "node_a"}


def node_b(state: AgentState) -> AgentState:
    """第二个节点: 调用 LLM 回答"""
    print("[Node B] 调用 LLM 回答...")
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )
    response = llm.invoke(state["messages"][-1])
    return {"messages": state["messages"] + [f"回答: {response.content}"], "step": "node_b"}


def router(state: AgentState) -> str:
    """路由函数: 决定下一步走向"""
    # 第一轮结束后结束
    if state["step"] == "node_b":
        return "end"
    return "end"


def main():
    """构建并运行 LangGraph 工作流"""
    print("\n" + "=" * 50)
    print("LangGraph Demo")
    print("=" * 50 + "\n")

    # 3. 创建图
    workflow = StateGraph(AgentState)

    # 4. 添加节点
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)

    # 5. 设置边 (流程)
    workflow.set_entry_point("node_a")
    workflow.add_edge("node_a", "node_b")
    workflow.add_edge("node_b", END)

    # 6. 编译图
    app = workflow.compile()

    # 7. 运行工作流
    initial_state = {"messages": [], "step": "start"}

    print("开始运行 LangGraph 工作流...\n")
    result = app.invoke(initial_state)

    print("\n" + "=" * 50)
    print("工作流结果:")
    print("=" * 50)
    for msg in result["messages"]:
        print(f"  - {msg}")


if __name__ == "__main__":
    main()
