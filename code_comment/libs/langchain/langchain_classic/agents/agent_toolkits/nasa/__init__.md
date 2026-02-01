# libs\langchain\langchain_classic\agents\agent_toolkits\nasa\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\nasa\__init__.py` 文件的详细中文注释。该模块是 NASA 工具包的入口点。

## 功能描述

该模块负责 NASA 工具包的相关功能实现。它提供了一组用于访问 NASA 开放 API 的工具，允许代理执行以下操作：
- **媒体搜索**: 搜索 NASA 的图像和视频库。
- **元数据查询**: 获取特定任务、卫星或科学数据的元数据。
- **科学数据访问**: 访问包括地球科学、天体物理学等领域的公开数据。

## 主要组件

- **`NasaToolkit`**: 核心组件，封装了一系列与 NASA API 交互的工具。

## 弃用说明

⚠️ **注意**: 该模块已被标记为弃用，并已迁移到 `langchain_community` 包中。

- **弃用原因**: LangChain 正在将第三方集成迁移到独立的包中，以减少核心库的体积并提高维护效率。
- **建议操作**: 使用 `langchain_community.agent_toolkits.nasa` 代替。

## 核心逻辑

该文件使用 `create_importer` 实现了动态导入机制。这种模式允许在保持向后兼容性的同时，引导用户转向新的包结构。

```python
DEPRECATED_LOOKUP = {
    "NasaToolkit": "langchain_community.agent_toolkits.nasa.toolkit",
}

# 动态属性查找
_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

### 关键映射

| 类名 | 迁移目标路径 |
| :--- | :--- |
| `NasaToolkit` | `langchain_community.agent_toolkits.nasa.toolkit` |

## 迁移指南

建议尽快更新导入语句：

```python
# 旧写法 (不推荐)
from langchain.agents.agent_toolkits.nasa import NasaToolkit

# 新写法 (推荐)
from langchain_community.agent_toolkits.nasa import NasaToolkit
```

