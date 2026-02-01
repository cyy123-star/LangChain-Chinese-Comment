# langchain_core.example_selectors.base

`langchain_core.example_selectors.base` 模块定义了示例选择器（Example Selector）的核心抽象接口。示例选择器用于从一组示例中动态选择最合适的子集，以便将其包含在提示词（Prompt）中，通常用于少样本（Few-shot）学习场景。

## 文件概述

- **角色**: 示例选择器抽象定义模块。
- **主要职责**: 提供 `BaseExampleSelector` 基类，确立如何添加示例以及如何根据输入选择示例的标准接口。
- **所属模块**: `langchain_core.example_selectors`

## 导入依赖

- `abc`: 提供抽象基类支持。
- `typing`: 提供类型提示支持（如 `Any`, `list`, `dict`）。
- `langchain_core.runnables`: 导入 `run_in_executor` 用于实现异步支持。

## 类与函数详解

### 1. BaseExampleSelector (抽象基类)
- **功能描述**: 所有示例选择器的基类。它定义了管理示例库和执行选择逻辑的通用框架。
- **核心方法**:
  - `add_example(example)`: **抽象方法**。将一个新的示例（以字典形式）添加到选择器的内部存储中。
  - `aadd_example(example)`: 异步版本的 `add_example`。默认在线程池中运行同步方法。
  - `select_examples(input_variables)`: **抽象方法**。根据当前的输入变量，从存储中选择最相关的示例。
  - `aselect_examples(input_variables)`: 异步版本的 `select_examples`。默认在线程池中运行同步方法。

## 核心逻辑

- **少样本动态化**: 示例选择器的核心价值在于它允许根据用户的具体提问，动态地挑选最相似、最合适或长度最匹配的例子，而不是在提示词中硬编码固定的例子。
- **异步支持**: 所有的同步方法都有对应的异步版本，确保在异步流式处理中不会阻塞主线程。

## 使用示例

```python
from langchain_core.example_selectors.base import BaseExampleSelector

class CustomSelector(BaseExampleSelector):
    def __init__(self):
        self.examples = []
        
    def add_example(self, example: dict[str, str]) -> None:
        self.examples.append(example)
        
    def select_examples(self, input_variables: dict[str, str]) -> list[dict]:
        # 简单的选择逻辑：始终返回最后添加的一个示例
        return [self.examples[-1]] if self.examples else []

selector = CustomSelector()
selector.add_example({"input": "你好", "output": "Hello"})
selected = selector.select_examples({"input": "再见"})
print(selected) # [{'input': '你好', 'output': 'Hello'}]
```

## 注意事项

- **数据结构**: 示例通常以 `dict` 形式存在，键是提示词模板中预期的变量名，值是对应的内容。
- **存储实现**: 子类可以自由选择存储方式，如简单的内存列表、本地文件或向量数据库（Vector Store）。

## 内部调用关系

- **FewShotPromptTemplate**: 少样本提示词模板类会持有一个示例选择器实例，并在格式化提示词时调用其 `select_examples` 方法。

## 相关链接
- [LangChain 官方文档 - 示例选择器](https://python.langchain.com/docs/modules/model_io/prompts/example_selectors/)

---
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
