# BaseLanguageModel (语言模型基类)

`BaseLanguageModel` 是 LangChain 中所有语言模型（LLM 和 ChatModel）的共同基类。它定义了模型如何与输入交互并产生输出的最底层标准。

## 核心继承关系

1. **`BaseLanguageModel`** (位于 `langchain_core`):
   - 所有的模型（无论是传统的文本补全 LLM 还是现代的消息对话模型）都必须继承自这个类。
   - 提供了统一的序列化和调用接口。

## 关键功能

- **统一调用**: 支持 `invoke`, `stream`, `batch` 等标准 Runnable 方法。
- **配置管理**: 支持通过 `.with_config()` 动态调整模型的 `temperature`, `stop` 序列等。
- **工具调用**: 现代对话模型通过继承此基类并扩展，支持 `bind_tools` 接口。

## 迁移指南

- **模块位置**: 该类已从 `langchain` 根目录迁移至 `langchain_core.language_models`。
- **推荐做法**: 在编写自定义模型或类型提示时，应始终引用 `langchain_core` 中的定义。

```python
from langchain_core.language_models import BaseLanguageModel

def my_function(model: BaseLanguageModel):
    # 无论传入的是 OpenAI 还是 Anthropic 模型，都能正常工作
    return model.invoke("Hello")
```
