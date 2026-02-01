# LangChain Core Prompts 模块中文注释

## 模块概述

`prompts` 模块是 LangChain Core 的核心组件之一，提供了一套用于构建和管理提示词的工具。该模块允许开发者创建、格式化和管理各种类型的提示词，以优化语言模型的输出。

## 核心功能

- **提示词模板**：提供各种提示词模板，支持变量替换
- **聊天提示词**：支持构建基于消息的聊天提示词
- **少样本提示词**：支持少样本学习的提示词构建
- **字符串提示词**：支持基于字符串的简单提示词
- **格式验证**：提供提示词格式验证工具
- **动态加载**：支持从文件或其他来源加载提示词
- **多格式支持**：支持 Jinja2 等多种模板格式

## 主要组件

### 基础提示词模板

#### BasePromptTemplate

`BasePromptTemplate` 是所有提示词模板的基础抽象类，定义了提示词模板的通用接口。主要方法：
- `format`：格式化提示词
- `format_prompt`：格式化提示词并返回提示词对象
- `partial`：部分应用提示词变量
- `get_input_schema`：获取输入模式
- `get_output_schema`：获取输出模式

#### StringPromptTemplate

`StringPromptTemplate` 是基于字符串的提示词模板基类。

### 具体提示词模板

#### PromptTemplate

`PromptTemplate` 是最基本的提示词模板，基于字符串和变量替换。
- **属性**：`template`（模板字符串）、`input_variables`（输入变量）、`output_parser`（输出解析器）
- **用途**：用于创建简单的基于字符串的提示词

#### ChatPromptTemplate

`ChatPromptTemplate` 是专门用于聊天模型的提示词模板，基于消息列表。
- **属性**：`messages`（消息模板列表）、`input_variables`（输入变量）
- **用途**：用于创建基于消息的聊天提示词

#### DictPromptTemplate

`DictPromptTemplate` 是基于字典的提示词模板。
- **属性**：`template`（字典模板）、`input_variables`（输入变量）
- **用途**：用于创建基于字典的提示词

### 聊天消息提示词模板

#### AIMessagePromptTemplate

`AIMessagePromptTemplate` 是 AI 消息的提示词模板。
- **用途**：用于创建 AI 角色的消息模板

#### HumanMessagePromptTemplate

`HumanMessagePromptTemplate` 是人类消息的提示词模板。
- **用途**：用于创建人类角色的消息模板

#### SystemMessagePromptTemplate

`SystemMessagePromptTemplate` 是系统消息的提示词模板。
- **用途**：用于创建系统角色的消息模板

#### ChatMessagePromptTemplate

`ChatMessagePromptTemplate` 是自定义角色聊天消息的提示词模板。
- **属性**：`role`（角色）、`prompt`（提示词模板）
- **用途**：用于创建自定义角色的消息模板

#### MessagesPlaceholder

`MessagesPlaceholder` 是消息占位符，用于在聊天提示词中插入动态消息列表。
- **属性**：`variable_name`（变量名）
- **用途**：用于在聊天提示词中插入动态消息

### 少样本提示词模板

#### FewShotPromptTemplate

`FewShotPromptTemplate` 是少样本提示词模板，用于创建包含示例的提示词。
- **属性**：`examples`（示例列表）、`example_prompt`（示例提示词模板）、`suffix`（后缀）、`prefix`（前缀）
- **用途**：用于创建少样本学习的提示词

#### FewShotChatMessagePromptTemplate

`FewShotChatMessagePromptTemplate` 是少样本聊天消息提示词模板，用于创建包含示例的聊天提示词。
- **用途**：用于创建少样本学习的聊天提示词

#### FewShotPromptWithTemplates

`FewShotPromptWithTemplates` 是带模板的少样本提示词模板。
- **用途**：用于创建带模板的少样本学习提示词

### 工具函数

- **format_document**：格式化文档
- **aformat_document**：异步格式化文档
- **get_template_variables**：获取模板变量
- **check_valid_template**：检查模板是否有效
- **jinja2_formatter**：使用 Jinja2 格式化模板
- **validate_jinja2**：验证 Jinja2 模板
- **load_prompt**：加载提示词

## 动态导入机制

该模块使用了动态导入机制，通过 `__getattr__` 函数在运行时按需导入模块，提高了模块的加载效率。具体的动态导入映射如下：

| 组件名称 | 所在模块 |
|---------|----------|
| BasePromptTemplate | base |
| format_document | base |
| aformat_document | base |
| AIMessagePromptTemplate | chat |
| BaseChatPromptTemplate | chat |
| ChatMessagePromptTemplate | chat |
| ChatPromptTemplate | chat |
| DictPromptTemplate | dict |
| HumanMessagePromptTemplate | chat |
| MessagesPlaceholder | chat |
| SystemMessagePromptTemplate | chat |
| FewShotChatMessagePromptTemplate | few_shot |
| FewShotPromptTemplate | few_shot |
| FewShotPromptWithTemplates | few_shot_with_templates |
| load_prompt | loading |
| PromptTemplate | prompt |
| StringPromptTemplate | string |
| check_valid_template | string |
| get_template_variables | string |
| jinja2_formatter | string |
| validate_jinja2 | string |

## 使用示例

### 1. 使用基本提示词模板

```python
from langchain_core.prompts import PromptTemplate

# 创建基本提示词模板
prompt = PromptTemplate(
    template="你是一个{role}，请回答以下问题：{question}",
    input_variables=["role", "question"]
)

# 格式化提示词
formatted_prompt = prompt.format(role="老师", question="什么是人工智能？")
print(f"格式化后的提示词: {formatted_prompt}")

# 使用部分应用
partial_prompt = prompt.partial(role="专家")
partially_formatted = partial_prompt.format(question="什么是机器学习？")
print(f"部分格式化后的提示词: {partially_formatted}")
```

### 2. 使用聊天提示词模板

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)

# 创建系统消息模板
system_template = SystemMessagePromptTemplate.from_template(
    "你是一个{role}，请友好地回答用户的问题。"
)

# 创建人类消息模板
human_template = HumanMessagePromptTemplate.from_template(
    "{question}"
)

# 创建聊天提示词模板
chat_prompt = ChatPromptTemplate.from_messages([
    system_template,
    human_template
])

# 格式化聊天提示词
formatted_chat_prompt = chat_prompt.format(
    role="助手",
    question="北京有什么好玩的地方？"
)

print("格式化后的聊天提示词:")
for message in formatted_chat_prompt:
    print(f"{message.type}: {message.content}")
```

### 3. 使用消息占位符

```python
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage

# 创建聊天提示词模板，包含消息占位符
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手，帮助用户总结对话历史。"),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("请总结上面的对话")
])

# 准备对话历史
chat_history = [
    HumanMessage(content="你好，我想了解一下LangChain"),
    AIMessage(content="LangChain是一个用于构建基于语言模型的应用程序的框架。"),
    HumanMessage(content="它有哪些核心功能？"),
    AIMessage(content="LangChain的核心功能包括：1. 提示词管理 2. 文档加载 3. 向量存储 4. 链和代理 5. 回调系统等。")
]

# 格式化提示词
formatted_prompt = chat_prompt.format(chat_history=chat_history)

print("格式化后的提示词:")
for message in formatted_prompt:
    print(f"{message.type}: {message.content}")
```

### 4. 使用少样本提示词模板

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# 准备示例
examples = [
    {"input": "高兴", "output": "兴高采烈"},
    {"input": "悲伤", "output": "悲痛欲绝"},
    {"input": "愤怒", "output": "怒火中烧"},
]

# 创建示例提示词模板
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="输入: {input}\n输出: {output}"
)

# 创建少样本提示词模板
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请为每个输入词提供一个更生动的同义词：",
    suffix="输入: {input}\n输出:",
    input_variables=["input"]
)

# 格式化少样本提示词
formatted_prompt = few_shot_prompt.format(input="兴奋")
print("格式化后的少样本提示词:")
print(formatted_prompt)
```

### 5. 使用 Jinja2 模板

```python
from langchain_core.prompts import PromptTemplate

# 创建使用 Jinja2 语法的提示词模板
jinja2_prompt = PromptTemplate(
    template="你是一个{{ role }}，请回答以下问题：\n\n{% for question in questions %}\n{{ loop.index }}. {{ question }}\n{% endfor %}",
    input_variables=["role", "questions"]
)

# 格式化提示词
formatted_prompt = jinja2_prompt.format(
    role="老师",
    questions=["什么是人工智能？", "它有哪些应用？", "未来发展趋势如何？"]
)

print("格式化后的 Jinja2 提示词:")
print(formatted_prompt)
```

### 6. 加载提示词

```python
from langchain_core.prompts import load_prompt
import tempfile
import os

# 创建临时提示词文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    f.write('''{
        "_type": "prompt",
        "template": "你是一个{role}，请回答：{question}",
        "input_variables": ["role", "question"]
    }''')
    temp_file_name = f.name

try:
    # 加载提示词
    loaded_prompt = load_prompt(temp_file_name)
    
    # 使用加载的提示词
    formatted_prompt = loaded_prompt.format(
        role="专家",
        question="什么是 LangChain？"
    )
    
    print("加载的提示词格式化结果:")
    print(formatted_prompt)
finally:
    # 清理临时文件
    os.unlink(temp_file_name)
```

## 最佳实践

1. **选择合适的模板**：根据模型类型和需求选择合适的提示词模板

2. **变量命名**：使用清晰、描述性的变量名，提高模板的可读性

3. **模板分离**：将复杂的提示词模板分离到单独的文件中，便于管理

4. **少样本学习**：对于复杂任务，使用 `FewShotPromptTemplate` 提供示例

5. **部分应用**：对于重复使用的变量，使用 `partial` 方法部分应用

6. **输出解析**：为提示词模板配置适当的输出解析器，处理模型输出

7. **格式验证**：使用 `check_valid_template` 等工具验证模板格式

8. **性能考虑**：对于频繁使用的提示词，考虑缓存格式化结果

## 注意事项

1. **变量匹配**：确保格式化时提供所有必要的变量，否则会抛出异常

2. **模板语法**：注意不同模板格式的语法差异，如 Jinja2 和普通字符串模板

3. **消息顺序**：在聊天提示词中，消息的顺序很重要

4. **模板长度**：注意提示词模板的长度，避免超出模型的上下文窗口

5. **特殊字符**：处理模板中的特殊字符，避免格式化错误

6. **安全性**：对于用户提供的输入，注意模板注入等安全问题

7. **多语言支持**：考虑多语言环境下的提示词处理

## 代码优化建议

1. **类型提示**：为提示词相关的函数和方法添加明确的类型提示

2. **错误处理**：在提示词格式化中添加适当的错误处理

3. **模块化**：将复杂的提示词逻辑模块化，提高代码可维护性

4. **测试覆盖**：为提示词模板编写全面的测试

5. **文档完善**：为自定义的提示词模板添加详细的文档

6. **缓存机制**：实现提示词格式化结果的缓存，提高性能

7. **模板管理**：实现提示词模板的版本控制和管理

## 总结

`prompts` 模块是 LangChain Core 中处理提示词的核心组件，提供了：

- 丰富的提示词模板类型，支持不同场景
- 强大的格式化能力，支持变量替换和条件逻辑
- 灵活的少样本学习支持，提高模型性能
- 与聊天模型的无缝集成，支持基于消息的提示词
- 动态加载和管理提示词的能力

通过合理使用这些组件，开发者可以：
- 创建高效、精确的提示词
- 优化语言模型的输出质量
- 提高应用程序的可维护性
- 实现复杂的提示词逻辑
- 快速适应不同的模型和场景

该模块为 LangChain 应用程序提供了坚实的提示词管理基础，使开发者能够专注于业务逻辑而不是提示词的底层实现细节。