# libs\langchain\langchain_classic\agents\agent_toolkits\playwright\__init__.py

`playwright` 模块提供了用于网页浏览和自动化的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **PlayWrightBrowserToolkit**: 整合了网页导航、点击、输入、提取文本等功能的工具包。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.playwright import PlayWrightBrowserToolkit

# 推荐的导入方式
from langchain_community.agent_toolkits.playwright import PlayWrightBrowserToolkit
```

## 注意事项

- **环境依赖**: 使用此工具包需要安装 `playwright` 及其浏览器二进制文件（`playwright install`）。
- **异步支持**: Playwright 支持同步和异步模式。该工具包通常与相应的事件循环配合使用。
- **安全警告**: 代理可以通过浏览器访问外部网站。请确保在受控环境中运行，并注意隐私和安全风险。

