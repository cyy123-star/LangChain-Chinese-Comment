# libs\langchain\langchain_classic\agents\load_tools.py

此文档提供了 `libs\langchain\langchain_classic\agents\load_tools.py` 文件的详细中文注释。该模块定义了如何动态加载 LangChain 预定义的工具。

## 功能描述

该模块是工具加载系统的代理层。它本身不包含具体的工具加载逻辑，而是利用 `create_importer` 将请求转发到 `langchain_community`。

## 动态导入机制

### 1. 实现逻辑

```python
_importer = create_importer(
    __package__,
    fallback_module="langchain_community.agent_toolkits.load_tools",
)

def __getattr__(name: str) -> Any:
    return _importer(name)
```

- **create_importer**: 创建一个智能导入器。
- **fallback_module**: 指定当在当前包找不到目标属性时，应跳转到的目标模块：`langchain_community.agent_toolkits.load_tools`。
- **__getattr__**: Python 的特殊方法。当用户尝试访问模块中不存在的属性（如 `load_tools`）时，该方法会被触发，并由 `_importer` 完成实际的查找和加载。

### 2. 核心功能

该模块主要导出了以下（动态加载的）功能：
- `load_tools`: 最核心的工具加载函数。允许通过字符串名称（如 `"arxiv"`, `"terminal"`, `"human"`）快速实例化工具。
- `get_all_tool_names`: 获取所有支持的内置工具名称列表。

## 迁移与背景

- **解耦设计**: 将具体工具实现移动到 `langchain_community` 是 LangChain 0.1.0 架构调整的重要部分。
- **透明性**: 对于开发者而言，从 `langchain_classic.agents.load_tools` 导入 `load_tools` 仍然有效，但底层实际上是在运行社区包的代码。

## 使用建议

虽然旧路径仍然有效，但为了保持代码的现代性并减少动态查找开销，建议直接从社区包导入：
```python
from langchain_community.agent_toolkits.load_tools import load_tools
```

