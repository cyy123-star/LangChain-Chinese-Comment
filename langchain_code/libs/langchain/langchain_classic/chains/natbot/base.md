# NatBotChain (Deprecated)

`NatBotChain` 旨在实现一个由 LLM 驱动的浏览器控制链。它接收网页内容（HTML 简化版）和用户的目标，生成控制浏览器的指令。

> **警告**: 该类自 v0.2.13 起已弃用。请从 `langchain_community.chains.natbot` 导入。

## 核心功能

NatBot 的核心是将浏览器交互建模为一个循环：
1. **感知**: 获取当前页面的简化 HTML/文本内容。
2. **决策**: LLM 根据当前页面状态和最终目标，决定下一步操作（如：点击、输入、滚动）。
3. **执行**: 执行生成的指令（通常通过 Playwright 或 Selenium）。

## 核心参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `objective` | `str` | 用户希望 NatBot 完成的任务目标（如：“在淘宝上买一顶帽子”）。 |
| `llm_chain` | `Runnable` | 核心决策链，负责根据页面内容生成控制指令。 |
| `input_browser_content_key` | `str` | 输入字典中存放浏览器页面内容的键，默认为 `"browser_content"`。 |

## 安全提示 (Security Note)

**重要**: 该链具有控制 Web 浏览器的能力，存在显著的安全风险：
- **SSRF 风险**: 浏览器可能被诱导访问内网地址或敏感本地文件。
- **操作风险**: 如果没有适当的沙箱环境，可能会执行非预期的点击或提交。
- **隔离建议**: 建议在隔离的网络环境和独立的服务器容器中运行 NatBot。

## 示例

```python
from langchain_community.chains.natbot import NatBotChain
from langchain_openai import OpenAI

model = OpenAI(temperature=0.5)
natbot = NatBotChain.from_llm(llm=model, objective="查找 LangChain 的 GitHub 地址")

# 在实际循环中调用
# response = natbot.run(browser_content="<html>...</html>", url="https://www.google.com")
```

## 现代替代方案

建议使用 **Multi-modal Agents** 或 **Playwright Toolkit**。现代的智能体可以使用视觉模型（如 GPT-4o）直接观察页面截图，并结合 Playwright 工具集进行更精准的交互。
