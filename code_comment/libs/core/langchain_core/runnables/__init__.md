# libs\core\langchain_core\runnables\__init__.py

该文件是 `runnables` 模块的入口点，负责导出 LangChain 表达式语言 (LCEL) 的核心组件、接口和实用工具。

## 文件概述

`__init__.py` 作为一个“桶文件”（Barrel File），统筹了 `runnables` 目录下的所有关键功能。它定义了 LangChain 最核心的 `Runnable` 协议及其各种实现类。为了优化导入性能，该模块采用了 PEP 562 风格的动态导入机制（`__getattr__`），只有在实际访问某个类或函数时才会从子模块中加载。

## 导入依赖

该文件内部使用了 `langchain_core._import_utils.import_attr` 来支持动态导入，避免了模块循环依赖和过早加载导致的启动缓慢问题。

## 导出的核心组件

| 组件名称 | 所属子模块 | 功能简述 |
| :--- | :--- | :--- |
| **基础协议** | | |
| `Runnable` | `base` | 所有可运行组件的基类，定义了 `invoke`, `batch`, `stream` 等标准接口。 |
| `RunnableSerializable` | `base` | 支持序列化的 Runnable 基类。 |
| **基础实现** | | |
| `RunnableSequence` | `base` | 将多个 Runnable 串联成链，前一个的输出作为后一个的输入（通过 `\|` 运算符创建）。 |
| `RunnableParallel` | `base` | 并行运行多个 Runnable，输入共享，输出为字典（通过 `dict` 或 `RunnableParallel` 创建）。 |
| `RunnableLambda` | `base` | 将普通的 Python 函数包装为 Runnable。 |
| `RunnableBinding` | `base` | 为 Runnable 绑定固定的参数或配置。 |
| **逻辑控制** | | |
| `RunnableBranch` | `branch` | 实现分支逻辑，根据条件选择不同的执行路径。 |
| `RunnableWithFallbacks` | `fallbacks` | 为 Runnable 提供回退机制，处理执行失败的情况。 |
| `RouterRunnable` | `router` | 根据输入中的键动态路由到不同的 Runnable。 |
| **状态与数据流** | | |
| `RunnablePassthrough` | `passthrough` | 透传输入数据，常用于在 Parallel 中添加额外字段。 |
| `RunnableAssign` | `passthrough` | 为输入字典分配新值的特殊透传器。 |
| `RunnableWithMessageHistory` | `history` | 自动管理聊天历史记录的封装器。 |
| **配置与实用工具** | | |
| `RunnableConfig` | `config` | 运行时配置对象（包含 tags, metadata, callbacks 等）。 |
| `AddableDict` | `utils` | 支持累加操作的字典，用于流式数据的聚合。 |
| `ConfigurableField` | `utils` | 定义可在运行时动态配置的字段。 |

## 核心逻辑

### 动态导入机制

文件并没有在顶层直接导入所有类，而是通过以下方式实现：
1. **`__all__`**: 定义了所有对外公开的符号列表。
2. **`_dynamic_imports`**: 一个字典，映射了公开符号与其所在的子模块名。
3. **`__getattr__(attr_name)`**: 当用户尝试导入 `__all__` 中的某个符号时，Python 会触发此函数，它会调用 `import_attr` 从对应的子模块中按需加载。

## 使用示例

```python
# 推荐的导入方式
from langchain_core.runnables import RunnableLambda, RunnableSequence, RunnableParallel

# 创建一个简单的 LCEL 链
chain = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2)
result = chain.invoke(1)  # (1 + 1) * 2 = 4
```

## 注意事项

- **类型提示**: 为了支持 IDE 的自动补全，文件使用了 `if TYPE_CHECKING` 块来导入所有符号。
- **性能优化**: 动态导入减少了 `import langchain_core` 时的初始开销。
- **扩展性**: 新增 Runnable 类型时，只需在对应的子模块实现，并在此文件的 `__all__` 和 `_dynamic_imports` 中注册即可。

## 相关链接

- [LangChain Expression Language (LCEL) 官方概念指南](https://python.langchain.com/docs/concepts/lcel/)
- [Runnable 接口规范](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/runnables/base.md)

***

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
