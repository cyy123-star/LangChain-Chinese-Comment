# model_profile.py - 模型能力配置 (Model Profiles)

## 文件概述
`model_profile.py` 定义了用于描述聊天模型能力的类型规范。这些配置信息（Profiles）包含了模型的上下文窗口大小、多模态输入/输出支持情况以及是否支持工具调用等核心特征。这些元数据帮助 LangChain 及其上层组件（如 Agent 或 Chain）在运行时根据不同模型的特性自动调整行为。

---

## 导入依赖
- **`typing_extensions`**: 提供 `TypedDict` 支持。

---

## 类与函数详解

### 1. ModelProfile (TypedDict)
**功能描述**: 描述聊天模型能力的配置字典。该功能目前处于 **Beta** 阶段，其结构可能会发生变化。

#### 输入约束 (Input constraints)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `max_input_tokens` | `int` | 模型支持的最大上下文窗口大小（Token 数）。 |
| `image_inputs` | `bool` | 是否支持图像输入。 |
| `image_url_inputs` | `bool` | 是否支持通过 URL 传入图像。 |
| `pdf_inputs` | `bool` | 是否支持 PDF 输入。 |
| `audio_inputs` | `bool` | 是否支持音频输入。 |
| `video_inputs` | `bool` | 是否支持视频输入。 |
| `image_tool_message` | `bool` | 是否可以在工具消息（Tool Message）中包含图像。 |

#### 输出约束 (Output constraints)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `max_output_tokens` | `int` | 模型支持的最大输出 Token 数。 |
| `reasoning_output` | `bool` | 是否支持推理/思维链（Chain-of-thought）输出。 |
| `image_outputs` | `bool` | 模型是否能生成图像输出。 |
| `audio_outputs` | `bool` | 模型是否能生成音频输出。 |

#### 工具调用与结构化输出 (Tool calling & Structured output)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `tool_calling` | `bool` | 是否支持工具调用（Tool Calling）。 |
| `tool_choice` | `bool` | 是否支持强制指定工具（Tool Choice）。 |
| `structured_output` | `bool` | 是否支持原生的结构化输出功能。 |

---

### 2. ModelProfileRegistry
**功能描述**: 一个映射表，将模型标识符（如模型名称）映射到其对应的 `ModelProfile`。

---

## 核心逻辑解读
1. **类型安全性**: 使用 `TypedDict(total=False)` 定义，意味着所有字段都是可选的，开发者可以只提供模型已知的部分能力信息。
2. **能力感知**: 通过这些配置，LangChain 可以实现“先检查，后调用”。例如，如果一个 Agent 需要处理 PDF，它可以先检查所选模型 Profile 的 `pdf_inputs` 字段是否为 `True`。
3. **Beta 特性**: 文档中明确标注了 `!!! warning "Beta feature"`，提示开发者该接口尚未完全稳定。

---

## 使用示例
```python
from langchain_core.language_models.model_profile import ModelProfile

# 定义一个模型的 Profile
gpt_4o_profile: ModelProfile = {
    "max_input_tokens": 128000,
    "image_inputs": True,
    "tool_calling": True,
    "structured_output": True
}

# 检查模型是否支持图像
if gpt_4o_profile.get("image_inputs"):
    print("该模型可以处理图像")
```

---

## 注意事项
- **自动加载**: 在 `BaseChatModel` 初始化时，如果未显式提供 Profile，LangChain 会尝试从厂商包中自动加载可用的能力数据。
- **TODO 扩展**: 源码中包含多个 TODO，预示着未来将增加更多关于输入格式（如 bytes 或 base64）的详细描述。

---

## 内部调用关系
- **`BaseChatModel`**: 持有一个 `profile` 属性，用于描述当前模型实例的能力。
- **`LangSmith`**: 这些能力信息也可以作为元数据上传到追踪平台，辅助性能分析。

---

## 相关链接
- [LangChain 官方文档 - Multimodal](https://docs.langchain.com/oss/python/langchain/models#multimodal)
- [LangChain 官方文档 - Tool Calling](https://docs.langchain.com/oss/python/langchain/models#tool-calling)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
