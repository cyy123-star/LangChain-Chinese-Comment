# libs\langchain\langchain_classic\agents\agent_toolkits\nasa\toolkit.py

`nasa/toolkit.py` 模块定义了 `NasaToolkit` 类，该类整合了多个用于访问 NASA 开放 API 的工具。

## 核心类

### `NasaToolkit`

`NasaToolkit` 继承自 `BaseToolkit`，旨在为代理提供一个统一的接口来查询 NASA 的海量数据资源。

#### 初始化参数

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `tools` | `List[BaseTool]` | 工具列表，通常通过 `NasaAPIWrapper` 生成。 |

#### 核心方法

##### `get_tools`

返回工具包中包含的所有工具。

```python
def get_tools(self) -> List[BaseTool]:
    """获取工具列表。"""
    return self.tools
```

#### 主要功能

- **搜索 NASA 库**: 允许代理搜索包含图像、音频和视频的 NASA 媒体库。
- **物理数据查询**: 获取有关行星、恒星和其他天体的物理属性数据。

## 动态导入机制

该文件使用了 `create_importer` 实现了动态属性查找。当开发者尝试从 `langchain_classic` 导入 `NasaToolkit` 时，系统会发出弃用警告，并自动重定向到 `langchain_community.agent_toolkits.nasa.toolkit`。

```python
DEPRECATED_LOOKUP = {"NasaToolkit": "langchain_community.agent_toolkits.nasa.toolkit"}

# 动态属性查找逻辑
_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    """动态获取属性。"""
    return _import_attribute(name)
```

## 迁移指南

由于该模块已被弃用，建议直接从 `langchain_community` 导入。确保已安装 `langchain-community`。

```bash
pip install langchain-community
```

```python
from langchain_community.agent_toolkits.nasa.toolkit import NasaToolkit
```

## 注意事项

- **API 限制**: 请遵守 NASA API 的速率限制政策。
- **多媒体处理**: 搜索结果通常返回多媒体文件的 URL 和元数据，代理需要能够解析这些信息。
- **安全性**: 如果使用需要 API Key 的特定端点，请确保通过环境变量（如 `NASA_API_KEY`）安全地管理凭据。

