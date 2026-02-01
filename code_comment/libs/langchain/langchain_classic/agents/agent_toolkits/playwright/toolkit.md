# libs\langchain\langchain_classic\agents\agent_toolkits\playwright\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\playwright\toolkit.py` 文件的详细中文注释。该模块已被弃用，并重定向到 `langchain_community`。

## 功能描述

该模块定义了 `PlayWrightBrowserToolkit`，它是一个用于与 Playwright 浏览器交互的工具包。通过动态导入机制，它现在指向 `langchain_community.agent_toolkits.playwright.toolkit`。

## 弃用说明

该模块已被移动到 `langchain_community`。
- **原始导入路径**: `langchain_classic.agents.agent_toolkits.playwright.toolkit.PlayWrightBrowserToolkit`
- **建议导入路径**: `langchain_community.agent_toolkits.playwright.toolkit.PlayWrightBrowserToolkit`

## 主要类

### PlayWrightBrowserToolkit

用于 Playwright 交互的工具包，包含导航、点击、抓取等工具。

#### 初始化

```python
@classmethod
def from_browser_context(
    cls,
    browser_context: BrowserContext,
    sync: bool = True,
) -> PlayWrightBrowserToolkit:
```

#### 包含工具

该工具包通过 `get_tools()` 提供以下核心能力：
- `ClickTool`: 点击页面元素。
- `CurrentWebPageTool`: 获取当前页面 URL。
- `ExtractHyperlinksTool`: 提取页面超链接。
- `ExtractTextTool`: 提取页面文本。
- `GetElementsTool`: 获取页面元素。
- `NavigateTool`: 导航至指定 URL。
- `NavigateBackTool`: 后退。
- `SearchTool`: 在页面中搜索。

## 动态导入机制

模块使用 `create_importer` 实现动态加载，以确保向后兼容性并提供弃用警告。

```python
DEPRECATED_LOOKUP = {
    "PlayWrightBrowserToolkit": "langchain_community.agent_toolkits.playwright.toolkit",
}
```

## 注意事项

1. 建议开发者尽快迁移到 `langchain_community` 中的对应版本。
2. 使用此模块时会触发 `LangChainDeprecationWarning`。

