"""最小可运行的 Bub 示例：在宿主进程中嵌入 runtime，并用 echo 覆盖模型阶段。

运行方式（无需任何 API 凭证）：

    uv run python bub_examples/minimal_echo.py

Bub 的核心概念：
    1. Bub 是「钩子驱动」的 agent runtime，一个 turn（轮次）的每个阶段都是一个
       pluggy hook。内置实现和外部插件都注册在同一组 hook 上。
    2. 内置 hook 先注册，外部插件后注册；运行后注册者优先（later wins）。
       因此只要在管线装配之后再注册自己的实现，就能覆盖某个阶段，而无需 fork runtime。
    3. 一个 turn 的管线固定为：
           resolve_session -> load_state -> build_prompt -> run_model
                                                              ↓
                       dispatch_outbound <- render_outbound <- save_state
       本示例只替换其中的 build_prompt 与 run_model 两步，其余（会话解析、状态保存、
       出站渲染与分发）仍复用内置实现。
"""

import asyncio

from bub import BubFramework, hookimpl

# content_of 是 Bub 从任意 Envelope（dict / dataclass / pydantic / 属性对象）中
# 安全读取正文的辅助函数，避免代码与某一种传输层 schema 强耦合。
from bub.envelope import content_of


class EchoPlugin:
    """把「构造 prompt」和「调用模型」两步替换成确定性的回显。

    一个插件就是「任意带有 @hookimpl 装饰方法的对象」，不要求继承特定基类。
    hook 方法名必须与 BubHookSpecs 中的声明一致，参数按名字注入。
    """

    # build_prompt 是 firstresult hook：按优先级依次调用，第一个返回非 None 的实现胜出。
    # 这里直接返回入站消息正文，作为本轮的 prompt。
    @hookimpl
    def build_prompt(self, message, session_id, state) -> str:
        return content_of(message)

    # run_model 同样是 firstresult hook，用于替换真正的模型调用。
    # 返回的字符串就是本轮模型输出；不会发生任何网络请求。
    @hookimpl
    def run_model(self, prompt, session_id, state) -> str:
        text = prompt if isinstance(prompt, str) else str(prompt)
        return f"[echo:{session_id}] {text}"


async def main() -> None:
    # 1) 构造 framework。构造时会快照当前工作目录作为 workspace，
    #    并加载 ~/.bub/config.yml（不存在也可）。
    framework = BubFramework()

    # 2) 载入 hook，顺序很关键：
    #    - 先注册内置实现（builtin）
    #    - 再扫描并注册 "bub" entry-point 组中的已安装插件
    framework.load_hooks()

    # 3) 在管线装配完成之后注册自定义插件，使其在插件管理器中排在最后，
    #    从而覆盖内置的 build_prompt / run_model。
    #    注意：bub 0.4.4 的 pluggy 管理器是私有属性 _plugin_manager；
    #    正式打包的插件应改用 pyproject 的 [project.entry-points."bub"] 注册。
    framework._plugin_manager.register(EchoPlugin(), name="echo")

    # 4) 构造一条入站 Envelope（这里用最普通的 dict）。
    #    session_id 决定会话与 tape 的归属，复用同一 id 即继续同一段对话。
    inbound = {
        "session_id": "embedded:demo",
        "channel": "embedded",
        "chat_id": "demo",
        "content": "hello from a host process",
    }

    # 5) framework.running() 是生命周期上下文：它会解析 tape store 等与生命周期绑定的
    #    hook。长驻服务应只在启动时进入一次，而不是每轮都进入。
    async with framework.running():
        # 6) process_inbound 跑完整个 turn 管线，返回 TurnResult
        #    （含 model_output、state、outbounds）。
        result = await framework.process_inbound(inbound)

    # 7) outbounds 是已渲染好的出站消息（此处为 ChannelMessage 对象），
    #    仍用 content_of 读取正文。本示例未绑定 channel router，因此只打印。
    for outbound in result.outbounds:
        print(content_of(outbound))


# 直接作为脚本运行时启动事件循环。
if __name__ == "__main__":
    asyncio.run(main())
