"""Bub 真实模型版：直接使用内置 Agent（SDK 方式）跑一个流式 turn。

与 minimal_echo.py 的区别：
    - minimal_echo.py 走 process_inbound 完整管线，并用插件覆盖 run_model 做回显；
    - 本示例跳过 outbound 渲染/分发，直接拿到内置 Agent 对象，调用它的
      run_stream() 消费流式事件，适合把 Bub 嵌进自己的服务或脚本里。

运行前需要配置模型与凭证（任选其一）：
    # 方式 A：显式指定
    export BUB_MODEL=deepseek:deepseek-chat
    export BUB_API_KEY=sk-xxxxxxxx

    # 方式 B：在仓库根目录放 .env，写入 provider 各自的 key
    #   DEEPSEEK_API_KEY=...
    #   OPENAI_API_KEY=...
    #   ANTHROPIC_API_KEY=...
    # 脚本会自动挑选第一个可用的 provider 并设置好 BUB_MODEL / BUB_API_KEY。

运行：
    uv run python bub_examples/agent_sdk.py
"""

import asyncio
import os

from bub import BubFramework
from bub.builtin.hook_impl import Agent
from dotenv import load_dotenv

# 说明：bub 0.4.4 的内置 Agent 位于 bub.builtin.hook_impl。
# 官方文档里的 bub.builtin.Agent(...)（带 tools/skill_dirs/tape_store 参数）
# 属于更新的源码分支，尚未在该发布版中提供；本示例按 0.4.4 的实际签名编写。

# 未显式设置 BUB_MODEL 时，按顺序探测已有 key 的 provider。
# 每项为：(BUB_MODEL 值, 读取的 key 环境变量, 可选的 BUB_API_BASE)
MODEL_PRESETS: list[tuple[str, str, str | None]] = [
    ("deepseek:deepseek-flash", "DEEPSEEK_API_KEY", "https://api.deepseek.com/v1"),
    ("openai:gpt-4o-mini", "OPENAI_API_KEY", None),
    ("anthropic:claude-sonnet-4-20250514", "ANTHROPIC_API_KEY", None),
    ("gemini:gemini-2.0-flash", "GEMINI_API_KEY", None),
    ("openrouter:openrouter/free", "OPENROUTER_API_KEY", None),
]


def configure_model() -> str:
    """确定本轮使用的模型，并把凭证桥接到 Bub 的 BUB_* 环境变量。

    Bub 通过 AgentSettings 读取配置，前缀为 BUB_（BUB_MODEL / BUB_API_KEY /
    BUB_API_BASE）。这些设置是进程级、在首次构造 BubFramework 时载入的，
    因此必须在创建 framework 之前设置好环境变量。
    """
    # 已有显式 BUB_* 配置时直接使用，不再探测。
    if os.getenv("BUB_MODEL"):
        model = os.environ["BUB_MODEL"]
        print(f"[configure_model] 使用已设置的 BUB_MODEL: {model}")
        return model

    for model, key_env, api_base in MODEL_PRESETS:
        key = os.getenv(key_env)
        if not key:
            continue
        os.environ["BUB_MODEL"] = model
        os.environ.setdefault("BUB_API_KEY", key)
        if api_base:
            os.environ.setdefault("BUB_API_BASE", api_base)
        print(f"[configure_model] 匹配到 {key_env}，使用 model: {model}")
        return model

    raise SystemExit(
        "未找到可用模型配置。请设置 BUB_MODEL 与 BUB_API_KEY，"
        "或在 .env 中提供 DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY 等。"
    )


async def main() -> None:
    # 从仓库根目录的 .env 载入 provider key（不存在也无妨）。
    load_dotenv()

    # 1) 先确定模型与凭证，再构造 framework（configure_model 会打印匹配到的模型）。
    configure_model()
    print()

    # 2) 装配运行时：load_hooks() 注册内置实现（含真实模型调用）及已安装插件。
    framework = BubFramework()
    framework.load_hooks()

    # 3) 直接持有内置 Agent。它负责真正的 agent loop：调用模型、执行工具、
    #    并在需要时继续多步推理。
    agent = Agent(framework)

    # 4) 构造入站消息。session_id 决定会话归并与 tape 归属。
    inbound = {
        "session_id": "sdk:demo",
        "channel": "sdk",
        "chat_id": "demo",
        "content": "用一句话解释 Bub 的 tape context 是什么。",
    }

    # 5) running() 是生命周期上下文，负责解析 tape store 等资源。
    async with framework.running():
        # 复刻 process_inbound 的前半段：解析 session、构建 state、构建 prompt。
        session_id = await framework.resolve_session(inbound)
        state = await framework.build_state(inbound, session_id)
        prompt = await framework.build_prompt(inbound, session_id, state)

        # 6) run_stream() 返回异步事件流：text / reasoning / tool_call /
        #    tool_result / usage / error / final。这里只打印增量文本。
        stream = await agent.run_stream(session_id=session_id, prompt=prompt, state=state)
        async for event in stream:
            if event.kind == "text":
                print(event.data.get("delta", ""), end="", flush=True)
            elif event.kind == "error":
                raise RuntimeError(str(event.data.get("message", "agent failed")))

    print()


if __name__ == "__main__":
    asyncio.run(main())
