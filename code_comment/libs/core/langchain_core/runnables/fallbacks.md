# RunnableWithFallbacks 详解

## 文件概述
`RunnableWithFallbacks` 是 LangChain 中用于增强链条（Chain）鲁棒性的重要组件。它允许为某个 `Runnable` 对象配置一组“备选方案”（Fallbacks）。当主 `Runnable` 执行失败（抛出特定异常）时，系统会自动按顺序尝试备选方案，直到有一个成功执行或全部失败。

这在调用不稳定或高延迟的外部 API（如 LLM 提供商）时非常有用。

---

## 导入依赖
- `asyncio`: 用于支持异步操作。
- `Runnable`, `RunnableSerializable`: 核心运行单元接口。
- `RunnableConfig`, `ensure_config`, `patch_config`: 运行时配置管理。
- `CallbackManager`, `AsyncCallbackManager`: 回调系统，用于追踪执行过程。
- `set_config_context`, `coro_with_context`: 上下文管理器，确保异步操作中配置的一致性。

---

## 类与函数详解

### `RunnableWithFallbacks` 类
该类继承自 `RunnableSerializable`，实现了自动容错机制。

#### 核心属性
| 属性名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `runnable` | `Runnable` | 首先尝试运行的主对象。 |
| `fallbacks` | `Sequence[Runnable]` | 备选方案序列，按顺序尝试。 |
| `exceptions_to_handle` | `tuple` | 需要触发回退的异常类型，默认为 `(Exception,)`。 |
| `exception_key` | `str | None` | 如果指定，捕获的异常将被注入到备选方案的输入字典中。 |

#### 核心方法 `invoke` / `ainvoke`
**核心逻辑**
1. **输入验证**：如果设置了 `exception_key`，输入必须是字典类型。
2. **启动追踪**：触发 `on_chain_start` 回调。
3. **循环尝试**：
   - 遍历 `runnable` 及其 `fallbacks` 序列。
   - 在 `try-except` 块中执行当前 `Runnable`。
   - 如果发生 `exceptions_to_handle` 中的异常，记录错误并继续尝试下一个。
   - 如果发生非预期的 `BaseException`，直接抛出并触发错误回调。
   - 如果成功，触发 `on_chain_end` 并返回结果。
4. **全盘失败**：如果所有尝试都抛出了异常，最终抛出第一个捕获到的错误。

#### 批量处理 `batch` / `abatch`
支持对一组输入进行带有回退机制的批量处理。它会智能地跟踪哪些输入执行成功，哪些需要尝试下一个备选方案，从而最大化处理效率。

#### 流式处理 `stream` / `astream`
支持流式输出的回退。逻辑是尝试连接到第一个能成功生成首个数据块（Chunk）的 `Runnable`。

---

## 使用示例

### 1. 模型级别的回退
```python
from langchain_core.chat_models.openai import ChatOpenAI
from langchain_core.chat_models.anthropic import ChatAnthropic

# 优先使用 Anthropic，如果失败（如额度不足或超时）则切换到 OpenAI
model = ChatAnthropic(model="claude-3-haiku").with_fallbacks(
    [ChatOpenAI(model="gpt-3.5-turbo")]
)

response = model.invoke("你好")
```

### 2. 带有异常注入的回退
```python
from langchain_core.runnables import RunnableLambda

def primary_logic(x):
    raise ValueError("Primary failed!")

def backup_logic(x):
    # x 中会包含 'error' 键，值为捕获到的 ValueError
    return f"Recovered from error: {x['error']}"

# 使用 .with_fallbacks 快捷方式创建
chain = RunnableLambda(primary_logic).with_fallbacks(
    [RunnableLambda(backup_logic)],
    exception_key="error"
)

print(chain.invoke({"input": "test"}))
```

---

## 注意事项
- **异常过滤**：默认只处理 `Exception`。如果需要处理特定错误（如 API 速率限制），请通过 `exceptions_to_handle` 明确指定。
- **性能开销**：回退机制涉及到多次尝试。如果主方案频繁失败，整体响应时间会显著增加。
- **副作用**：如果 `Runnable` 包含有副作用的操作（如数据库写入），请注意回退可能会导致操作重复或状态不一致。
- **输入要求**：当使用 `exception_key` 时，所有相关的 `Runnable` 必须接受字典作为输入。

---

## 内部调用关系
- **与 `with_fallbacks` 关系**：大多数 `Runnable` 对象都内置了 `with_fallbacks` 方法，它是实例化 `RunnableWithFallbacks` 的便捷途径。
- **与回调系统关系**：在尝试每个备选方案时，会通过 `run_manager.get_child()` 创建子运行（Child Run），使得在日志中可以清晰看到失败的尝试和最终成功的路径。

---

## 相关链接
- [LangChain 官方指南 - Fallbacks](https://python.langchain.com/docs/expression_language/how_to/fallbacks)
- [源码引用: base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/base.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
