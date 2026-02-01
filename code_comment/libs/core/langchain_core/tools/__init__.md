# langchain_core.tools

## 文件概述
**langchain_core.tools** 是 LangChain 核心库中工具模块的入口。它通过统一的接口导出了所有与工具（Tools）相关的核心组件，包括基类、装饰器、工厂函数和渲染器。该模块采用了动态导入机制，以提高包的加载速度。

---

## 导入依赖
| 依赖项 | 来源 | 作用 |
| :--- | :--- | :--- |
| `import_attr` | `langchain_core._import_utils` | 实现属性的动态按需加载。 |

---

## 核心组件导览
本模块通过 `__all__` 导出了以下关键组件，按功能分类如下：

### 1. 核心基类
- **`BaseTool`**: 所有工具的抽象基类，定义了统一的调用接口。
- **`BaseToolkit`**: 工具箱基类，用于组合多个相关的工具。

### 2. 具体工具实现
- **`Tool`**: 简单的单输入工具封装类。
- **`StructuredTool`**: 支持多参数输入的复杂工具封装类。

### 3. 工具创建与装饰器
- **`tool`**: 创建工具的首选装饰器，支持同步和异步函数。
- **`convert_runnable_to_tool`**: 将任意 `Runnable` 对象转换为工具。
- **`create_retriever_tool`**: 专门用于将检索器（Retriever）转换为工具的工厂函数。

### 4. 工具渲染器
- **`render_text_description`**: 将工具列表渲染为纯文本名称和描述。
- **`render_text_description_and_args`**: 将工具列表渲染为包含详细参数架构的文本。

### 5. 异常与类型
- **`ToolException`**: 工具执行过程中抛出的标准异常。
- **`ArgsSchema`**: 工具输入参数架构的类型定义。

---

## 核心逻辑
- **动态导入**: 模块定义了一个内部字典 `_dynamic_imports`，映射了导出的属性名与其所在的子模块。
- **`__getattr__`**: 当访问模块属性时，如果属性尚未加载，会通过 `import_attr` 动态从子模块中导入并缓存到全局命名空间中。
- **`__dir__`**: 确保 IDE 和 `dir()` 函数能够正确列出所有导出的公共属性。

---

## 使用示例
```python
# 推荐的导入方式
from langchain_core.tools import tool, BaseTool, create_retriever_tool

# 使用装饰器定义工具
@tool
def my_custom_tool(query: str) -> str:
    """Do something useful."""
    return "Result"

# 检查类型
print(isinstance(my_custom_tool, BaseTool)) # True
```

---

## 注意事项
- **按需导入**: 由于采用了动态导入，只有在真正使用某个组件时，其所在的子模块才会被加载。这减少了初始化时的开销。
- **一致性**: 开发者应优先从 `langchain_core.tools` 导入常用组件，而不是直接从子模块（如 `langchain_core.tools.base`）导入，以保持代码的简洁和一致性。

---

## 相关链接
- [langchain_core.tools.base](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/base.md)
- [langchain_core.tools.convert](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/convert.md)
- [langchain_core.tools.simple](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/simple.md)
- [langchain_core.tools.structured](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/structured.md)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
