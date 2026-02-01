# NatBotChain (浏览器驱动链)

`NatBotChain` 旨在实现一个由 LLM 驱动的浏览器控制逻辑。它接收当前的 URL 和浏览器内容（通常是简化后的 HTML 或可访问性树），并根据预设的目标（Objective）生成下一个浏览器操作指令。

## 安全提示 (Security Note)

该工具包提供的代码可控制 Web 浏览器。浏览器可被用于访问：
- 任何 URL（包括内部网络 URL）
- 本地文件

在将此链暴露给最终用户时需格外小心。务必控制访问权限，并隔离运行此链的服务器网络。

## 核心类：NatBotChain

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `objective` | `str` | 赋予 NatBot 的目标任务。 |
| `llm_chain` | `Runnable` | 用于生成指令的底层逻辑链。 |
| `input_url_key` | `str` | 输入字典中 URL 的键名，默认为 `"url"`。 |
| `input_browser_content_key` | `str` | 输入字典中浏览器内容的键名，默认为 `"browser_content"`。 |
| `previous_command` | `str` | 上一次执行的指令，用于保持上下文。 |

### 执行逻辑 (`_call` 方法)

`NatBotChain` 的工作流程如下：

1.  **输入裁剪**: 为了适配 LLM 的上下文窗口，URL 会被裁剪到前 100 字符，浏览器内容会被裁剪到前 4500 字符。
2.  **指令生成**: 将目标、当前 URL、前一个指令和浏览器内容发送给 LLM。
3.  **状态更新**: 记录 LLM 生成的新指令为 `previous_command`。
4.  **输出**: 返回 LLM 建议的下一个浏览器指令。

#### 源码片段：核心调用
```python
def _call(
    self,
    inputs: dict[str, str],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    url = inputs[self.input_url_key]
    browser_content = inputs[self.input_browser_content_key]
    llm_cmd = self.llm_chain.invoke(
        {
            "objective": self.objective,
            "url": url[:100],
            "previous_command": self.previous_command,
            "browser_content": browser_content[:4500],
        },
        config={"callbacks": _run_manager.get_child()},
    )
    llm_cmd = llm_cmd.strip()
    self.previous_command = llm_cmd # 记录状态
    return {self.output_key: llm_cmd}
```

## 使用示例

```python
from langchain_openai import OpenAI
from langchain_classic.chains import NatBotChain

llm = OpenAI(temperature=0)
objective = "在 Google 上搜索有关 LangChain 的最新消息"
natbot = NatBotChain.from_llm(llm, objective)

# 模拟浏览器环境
cmd = natbot.execute("https://www.google.com", "<html>...浏览器简化内容...</html>")
print(f"建议的操作: {cmd}")
```

## 迁移建议

该类已被弃用，建议迁移到 `langchain_community.chains.natbot` 或使用更现代的工具包：
1.  **Playwright Toolkit**: 现代的浏览器自动化推荐使用 `langchain_community.agent_toolkits.PlaywrightBrowserToolkit`，它提供了更丰富的原子操作工具。
2.  **Multi-On Agent**: 专门为网页浏览和操作优化的第三方集成方案。
3.  **LangGraph**: 浏览器自动化通常涉及复杂的决策循环和错误恢复，使用 LangGraph 可以更好地管理浏览器的状态机。

