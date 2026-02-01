# langchain_core/__init__.py 中文注释

## 功能描述
`langchain_core` 模块定义了 LangChain 生态系统的基础抽象接口。它包含了核心组件的接口定义，如聊天模型、LLM、向量存储、检索器等，以及通用调用协议（Runnables）和组件组合语法。

**重要说明：** 此模块不包含任何第三方集成，依赖项被有意保持非常轻量。

## 模块导出内容

| 导出项 | 描述 |
|-------|------|
| `surface_langchain_beta_warnings` | 显示 LangChain Beta 版本警告 |
| `surface_langchain_deprecation_warnings` | 显示 LangChain 弃用警告 |
| `VERSION` | 版本号 |
| `__version__` | 版本号（与 VERSION 相同） |

## 使用示例

### 基本导入
```python
from langchain_core import *

# 查看版本
print(__version__)
```

### 检查警告
当使用 Beta 功能或已弃用功能时，系统会自动显示相应的警告信息。

## 注意事项
1. **轻量级依赖**：此模块设计为轻量级，不包含第三方集成
2. **核心接口**：所有 LangChain 核心组件的接口都在此定义
3. **版本管理**：通过 `__version__` 可以查看当前使用的版本
4. **警告机制**：模块会自动处理 Beta 功能和弃用功能的警告

## 模块结构
`langchain_core` 包含以下主要子模块：
- `_api`：API 相关功能
- `callbacks`：回调机制
- `documents`：文档处理
- `embeddings`：嵌入功能
- `language_models`：语言模型接口
- `messages`：消息处理
- `prompts`：提示模板
- `runnables`：通用调用协议
- `tools`：工具定义
- `utils`：工具函数

这些子模块共同构成了 LangChain 的核心功能体系，为上层应用提供了统一的接口和实现标准。