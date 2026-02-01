# image.py

## 文件概述
`image.py` 模块定义了 `ImagePromptTemplate` 类，专门用于处理多模态模型中的图像提示词。它允许开发者像处理文本模板一样处理图像 URL，支持通过变量动态生成图像地址或设置图像识别的详细程度（Detail）。

---

## 导入依赖
- `pydantic`: 用于数据验证和属性定义。
- `langchain_core.prompt_values`: 导入 `ImagePromptValue` 和 `ImageURL` 类型，定义格式化后的输出结构。
- `langchain_core.prompts.string`: 复用字符串模板的格式化映射。
- `langchain_core.runnables`: 提供异步执行工具。

---

## 类与函数详解

### 1. `ImagePromptTemplate` (类)
多模态模型的图像提示词模板。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `template` | `dict` | `{}` | 否 | 图像配置模板字典，通常包含 `url` 和 `detail` 的模板字符串。 |
| `template_format` | `PromptTemplateFormat` | `"f-string"` | 否 | 模板语法格式（如 f-string）。 |

#### 核心方法
- `__init__`: 初始化方法。会检查 `input_variables` 是否包含保留字 `url`、`path` 或 `detail`，如果包含则抛出错误。
- `format`: **核心逻辑实现**。
    - 对 `template` 字典中的字符串值进行格式化。
    - 优先从传入的 `kwargs` 中获取 `url` 和 `detail`，若无则从格式化后的模板中获取。
    - **安全性检查**：禁止使用 `path` 加载本地图像（出于安全考虑，自 0.3.15 版本起已移除此功能）。
    - 返回一个符合 `ImageURL` 结构的字典：`{"url": "...", "detail": "..."}`。
- `format_prompt` / `aformat_prompt`: 将格式化结果包装为 `ImagePromptValue`。

#### 使用示例
```python
from langchain_core.prompts import ImagePromptTemplate

# 定义一个动态图像模板
prompt = ImagePromptTemplate(
    input_variables=["image_id"],
    template={"url": "https://example.com/images/{image_id}.jpg", "detail": "high"}
)

# 格式化并获取结果
image_url_dict = prompt.format(image_id="123")
print(image_url_dict) 
# 输出: {'url': 'https://example.com/images/123.jpg', 'detail': 'high'}
```

---

## 安全性设计
- **路径限制**：明确禁止使用 `path` 关键字加载本地文件，防止潜在的本地文件读取漏洞。所有图像必须通过可验证的 `url` 提供。
- **关键字保护**：在初始化时限制 `input_variables` 的命名，避免用户定义的变量与系统核心字段（`url`, `detail`）冲突。

---

## 内部调用关系
- **继承体系**: `ImagePromptTemplate` 继承自 `BasePromptTemplate[ImageURL]`。
- **依赖关系**: 依赖 `langchain_core.prompts.string` 中的格式化引擎。

---

## 相关链接
- [LangChain 官方文档 - Multimodal Prompts](https://python.langchain.com/docs/modules/model_io/prompts/multimodal/)
- [OpenAI 官方文档 - Vision detail parameter](https://platform.openai.com/docs/guides/vision/low-or-high-fidelity-image-understanding)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
