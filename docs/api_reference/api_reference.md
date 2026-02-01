# LangChain API参考手册

本文档提供了LangChain框架的核心API参考，按照模块组织，帮助开发者快速查找和理解各个组件的用法。

## 核心模块

### 1. langchain_core

`langchain_core` 是LangChain的核心模块，定义了框架的基础抽象和接口。

#### 1.1 messages 模块

**功能**：处理聊天消息的核心模块，支持多种消息类型和内容格式。

**主要组件**：

- `BaseMessage`：所有消息的基类
- `HumanMessage`：人类用户的消息
- `AIMessage`：AI生成的消息
- `SystemMessage`：系统指令消息
- `ChatMessage`：通用聊天消息
- `FunctionMessage`：函数调用结果消息
- `ToolMessage`：工具调用结果消息
- `ContentBlock`：内容块基类
- `TextContentBlock`：文本内容块
- `ImageContentBlock`：图片内容块

**工具函数**：

- `convert_to_messages`：转换为消息对象
- `convert_to_openai_messages`：转换为OpenAI消息格式
- `get_buffer_string`：获取消息缓冲区字符串
- `messages_to_dict`：将消息列表转换为字典列表
- `messages_from_dict`：从字典列表创建消息列表

#### 1.2 prompts 模块

**功能**：提供提示模板系统，用于构建和管理LLM的提示。

**主要组件**：

- `BasePromptTemplate`：所有提示模板的基类
- `PromptTemplate`：基础提示模板
- `ChatPromptTemplate`：聊天提示模板
- `FewShotPromptTemplate`：少样本提示模板
- `MessagePromptTemplate`：消息提示模板
- `StructuredPromptTemplate`：结构化提示模板

#### 1.3 runnables 模块

**功能**：定义了LangChain的核心执行机制，支持同步、异步、批处理和流式处理。

**主要组件**：

- `Runnable`：所有可运行对象的基类
- `RunnableLambda`：包装lambda函数的可运行对象
- `RunnableSequence`：可运行对象的序列组合
- `RunnableParallel`：并行执行多个可运行对象
- `RunnableBranch`：根据条件选择不同的可运行对象
- `RunnableWithFallbacks`：带fallback机制的可运行对象
- `RunnableWithMessageHistory`：带消息历史的可运行对象

**LCEL语法**：

```python
# 使用管道操作符合成链
chain = (runnable1 | runnable2 | runnable3)
```

#### 1.4 output_parsers 模块

**功能**：解析LLM的输出，转换为结构化数据。

**主要组件**：

- `BaseOutputParser`：所有输出解析器的基类
- `StringOutputParser`：字符串输出解析器
- `JsonOutputParser`：JSON输出解析器
- `ListOutputParser`：列表输出解析器
- `XmlOutputParser`：XML输出解析器

#### 1.5 embeddings 模块

**功能**：提供文本嵌入功能，将文本转换为向量表示。

**主要组件**：

- `Embeddings`：嵌入的基类
- `FakeEmbeddings`：用于测试的假嵌入

#### 1.6 documents 模块

**功能**：处理文档相关的功能，包括文档表示和转换。

**主要组件**：

- `Document`：文档的基本表示
- `BaseDocumentCompressor`：文档压缩器的基类

#### 1.7 language_models 模块

**功能**：定义语言模型的接口和基础实现。

**主要组件**：

- `BaseLanguageModel`：语言模型的基类
- `LLM`：文本生成语言模型
- `FakeLLM`：用于测试的假LLM

### 2. langchain_classic

`langchain_classic` 是LangChain的经典模块，提供了传统的LangChain功能和组件。

#### 2.1 agents 模块

**功能**：提供代理相关的功能，支持多种代理类型。

**主要组件**：

- `MRKLChain`：多步推理链
- `ReActChain`：推理和行动链
- `SelfAskWithSearchChain`：自我提问搜索链

#### 2.2 chains 模块

**功能**：提供各种链的实现，用于组合不同的组件。

**主要组件**：

- `LLMChain`：基础LLM链
- `ConversationChain`：对话链
- `LLMMathChain`：数学计算链
- `QAWithSourcesChain`：带来源的问答链
- `VectorDBQA`：向量数据库问答链

#### 2.3 llms 模块

**功能**：集成各种语言模型。

**主要组件**：

- `OpenAI`：OpenAI模型
- `Anthropic`：Anthropic模型
- `Cohere`：Cohere模型
- `HuggingFaceHub`：Hugging Face模型
- `LlamaCpp`：本地Llama模型

#### 2.4 memory 模块

**功能**：提供内存管理功能，用于存储和检索对话历史。

**主要组件**：

- `BaseMemory`：内存的基类
- `SimpleMemory`：简单内存
- `ConversationBufferMemory`：对话缓冲区内存
- `ConversationSummaryMemory`：对话摘要内存
- `ConversationBufferWindowMemory`：对话缓冲区窗口内存

#### 2.5 tools 模块

**功能**：定义和管理工具，用于扩展LLM的能力。

**主要组件**：

- `BaseTool`：工具的基类
- `Tool`：基础工具实现
- `StructuredTool`：结构化工具

### 3. langchain_v1

`langchain_v1` 是LangChain的1.x版本模块，提供了简化的结构和核心功能。

**主要组件**：

- `agents`：代理相关功能
- `chat_models`：聊天模型
- `embeddings`：嵌入功能
- `messages`：消息处理

## API使用示例

### 1. 使用messages模块

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 创建消息
messages = [
    SystemMessage(content="你是一个 helpful 的助手"),
    HumanMessage(content="你好，今天天气怎么样？"),
    AIMessage(content="今天天气很好，阳光明媚！")
]

# 转换为OpenAI格式
from langchain_core.messages import convert_to_openai_messages
openai_messages = convert_to_openai_messages(messages)
print(openai_messages)
```

### 2. 使用prompts模块

```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# 创建基础提示模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="请写一篇关于 {topic} 的短文。"
)

# 格式化提示
formatted_prompt = prompt.format(topic="人工智能")
print(formatted_prompt)

# 创建聊天提示模板
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 helpful 的助手"),
    ("human", "你好，{topic} 是什么？")
])

# 格式化聊天提示
formatted_chat_prompt = chat_prompt.format_messages(topic="人工智能")
print(formatted_chat_prompt)
```

### 3. 使用runnables模块

```python
from langchain_core.runnables import RunnableLambda, RunnableSequence

# 创建可运行对象
runnable1 = RunnableLambda(lambda x: x + 1)
runnable2 = RunnableLambda(lambda x: x * 2)

# 创建序列
sequence = RunnableSequence(runnable1, runnable2)

# 执行
result = sequence.invoke(5)
print(result)  # 输出: 12

# 使用LCEL语法
from langchain_core.runnables import RunnableLambda

chain = (RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2))
result = chain.invoke(5)
print(result)  # 输出: 12
```

### 4. 使用output_parsers模块

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

# 创建JSON输出解析器
parser = JsonOutputParser()

# 创建提示模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="请生成关于 {topic} 的JSON数据，包含名称和描述字段。\n{format_instructions}",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# 格式化提示
formatted_prompt = prompt.format(topic="人工智能")
print(formatted_prompt)

# 解析输出
# 假设LLM输出: {"name": "人工智能", "description": "人工制造的智能系统"}
output = '{"name": "人工智能", "description": "人工制造的智能系统"}'
parsed_output = parser.parse(output)
print(parsed_output)
```

## 最佳实践

1. **模块导入**：从正确的模块路径导入所需组件
2. **参数验证**：使用类型提示和参数验证确保输入正确
3. **错误处理**：使用try-except捕获和处理可能的错误
4. **性能优化**：对于大批量处理，使用批处理方法
5. **内存管理**：合理使用内存组件，避免内存泄漏
6. **流式处理**：对于需要实时反馈的场景，使用流式处理

## 版本兼容性

- **langchain_core**：核心功能，稳定版本
- **langchain_classic**：经典功能，向后兼容
- **langchain_v1**：1.x版本，简化结构

请根据项目需求选择合适的模块和版本。