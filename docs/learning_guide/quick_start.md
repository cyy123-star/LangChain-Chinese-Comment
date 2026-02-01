# LangChain快速入门教程

本教程将帮助您快速上手LangChain框架，通过实际示例展示如何使用LangChain构建基于大语言模型的应用程序。

## 环境准备

### 安装依赖

```bash
# 安装LangChain
pip install langchain

# 安装OpenAI依赖（用于示例）
pip install openai

# 安装其他常用依赖
pip install langchain-community langchain-core
```

### 配置API密钥

对于使用OpenAI模型的示例，您需要配置OpenAI API密钥：

```bash
# Windows
sets OPENAI_API_KEY=your-api-key

# macOS/Linux
export OPENAI_API_KEY=your-api-key
```

## 教程1：基础LLM调用

### 步骤1：导入必要的模块

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
```

### 步骤2：创建语言模型实例

```python
# 创建OpenAI模型实例
llm = OpenAI(temperature=0.7)
```

### 步骤3：创建提示模板

```python
# 创建提示模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="请写一篇关于 {topic} 的短文，大约200字。"
)
```

### 步骤4：生成文本

```python
# 格式化提示
formatted_prompt = prompt.format(topic="人工智能")

# 生成文本
result = llm(formatted_prompt)
print(result)
```

## 教程2：创建简单的对话机器人

### 步骤1：导入必要的模块

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
```

### 步骤2：创建聊天模型实例

```python
# 创建ChatOpenAI模型实例
chat_model = ChatOpenAI(temperature=0.7)
```

### 步骤3：构建消息历史

```python
# 构建消息历史
messages = [
    SystemMessage(content="你是一个 helpful 的助手，用中文回答问题。"),
    HumanMessage(content="你好，你是谁？"),
    AIMessage(content="你好！我是一个由OpenAI训练的人工智能助手，可以回答你的问题，提供信息，或者帮助你完成各种任务。请问有什么我可以帮助你的吗？")
]
```

### 步骤4：发送新消息

```python
# 添加新的人类消息
messages.append(HumanMessage(content="什么是LangChain？"))

# 生成回复
response = chat_model(messages)
print(response.content)

# 将回复添加到消息历史
messages.append(response)
```

## 教程3：使用LCEL构建链

### 步骤1：导入必要的模块

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StringOutputParser
from langchain_openai import OpenAI
from langchain_core.runnables import RunnableLambda
```

### 步骤2：创建组件

```python
# 创建LLM
llm = OpenAI(temperature=0.7)

# 创建提示模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="请写一篇关于 {topic} 的短文，大约200字。"
)

# 创建输出解析器
output_parser = StringOutputParser()

# 创建额外的处理步骤
uppercase_transform = RunnableLambda(lambda x: x.upper())
```

### 步骤3：使用LCEL构建链

```python
# 使用LCEL语法构建链
chain = (prompt | llm | output_parser | uppercase_transform)

# 执行链
result = chain.invoke({"topic": "人工智能"})
print(result)
```

## 教程4：构建问答系统

### 步骤1：导入必要的模块

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.runnables import RunnableLambda
```

### 步骤2：准备知识库

```python
# 简单的知识库
knowledge_base = ""
""
LangChain是一个用于开发基于大语言模型的应用程序的框架。
它提供了一系列工具和接口，帮助开发者快速构建复杂的LLM应用。
LangChain的核心功能包括：
1. 链（Chains）：将多个组件组合在一起
2. 代理（Agents）：让LLM自主决策和执行任务
3. 内存（Memory）：管理对话历史和状态
4. 工具（Tools）：扩展LLM的能力
5. 文档处理：处理和分析文档
""
"
```

### 步骤3：创建问答链

```python
# 创建LLM
llm = OpenAI(temperature=0)

# 创建提示模板
qa_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""
    基于以下上下文回答问题：
    
    {context}
    
    问题：{question}
    
    请用中文回答，不要添加任何引言或开场白。
    """
)

# 构建链
qa_chain = ({
    "question": RunnableLambda(lambda x: x),
    "context": RunnableLambda(lambda x: knowledge_base)
} | qa_prompt | llm)

# 测试问答
result = qa_chain.invoke("LangChain的核心功能有哪些？")
print(result)
```

## 教程5：使用工具和代理

### 步骤1：导入必要的模块

```python
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
import requests
```

### 步骤2：创建工具

```python
# 定义一个简单的天气工具
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 这里使用模拟数据，实际应用中可以调用真实的天气API
    weather_data = {
        "北京": "晴，25℃",
        "上海": "多云，23℃",
        "广州": "阴，28℃"
    }
    return weather_data.get(city, "未知城市")

# 创建工具
weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="获取指定城市的天气信息"
)
```

### 步骤3：创建代理链

```python
# 创建聊天模型
chat_model = ChatOpenAI(temperature=0)

# 创建代理提示模板
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手，需要时可以使用工具来获取信息。"),
    ("human", "{input}"),
    ("assistant", "思考：我需要使用工具来回答这个问题吗？"),
    ("human", "如果需要使用工具，请使用以下格式：\n工具调用：\n{{\"toolcall\": {{\"name\": \"工具名称\", \"args\": {{\"参数名\": \"参数值\"}}}}}\n如果不需要使用工具，请直接回答。")
])

# 构建代理链
def agent_logic(input_text):
    # 生成思考和工具调用
    response = chat_model(
        agent_prompt.format_messages(input=input_text)
    )
    
    # 检查是否需要工具调用
    if "工具调用：" in response.content:
        # 简单的工具调用解析
        import json
        tool_call = json.loads(response.content.split("工具调用：\n")[1])
        tool_name = tool_call["toolcall"]["name"]
        tool_args = tool_call["toolcall"]["args"]
        
        # 调用工具
        if tool_name == "get_weather":
            tool_result = get_weather(**tool_args)
            
            # 使用工具结果生成最终回答
            final_prompt = ChatPromptTemplate.from_messages([
                ("system", "你是一个助手，根据工具结果回答问题。"),
                ("human", "问题：{input}\n工具结果：{tool_result}")
            ])
            final_response = chat_model(
                final_prompt.format_messages(input=input_text, tool_result=tool_result)
            )
            return final_response.content
    
    # 直接回答
    return response.content

# 创建代理链
agent_chain = RunnableLambda(agent_logic)

# 测试代理
result = agent_chain.invoke("北京今天的天气怎么样？")
print(result)
```

## 教程6：使用内存管理对话历史

### 步骤1：导入必要的模块

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
```

### 步骤2：创建内存实例

```python
# 创建对话缓冲区内存
memory = ConversationBufferMemory(return_messages=True)
```

### 步骤3：创建聊天链

```python
# 创建聊天模型
chat_model = ChatOpenAI(temperature=0.7)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 helpful 的助手，用中文回答问题。"),
    ("human", "{input}")
])

# 构建链
def get_chat_history():
    return memory.load_memory_variables({}).get("history", [])

chat_chain = (
    RunnablePassthrough.assign(
        history=get_chat_history
    )
    | prompt
    | chat_model
)

# 处理回复并更新内存
def chat_with_memory(input_text):
    # 获取回复
    response = chat_chain.invoke({"input": input_text})
    
    # 更新内存
    memory.save_context(
        {"input": input_text},
        {"output": response.content}
    )
    
    return response.content
```

### 步骤4：测试对话

```python
# 第一次对话
response1 = chat_with_memory("你好，你是谁？")
print("助手:", response1)

# 第二次对话（应该记住之前的对话）
response2 = chat_with_memory("你能告诉我什么是人工智能吗？")
print("助手:", response2)

# 第三次对话（测试上下文理解）
response3 = chat_with_memory("它和你有什么关系？")
print("助手:", response3)
```

## 常见问题解决

### 1. API密钥错误

**问题**：`Error: No API key provided.`

**解决方案**：确保正确设置了API密钥环境变量。

### 2. 模块导入错误

**问题**：`ModuleNotFoundError: No module named 'langchain_openai'`

**解决方案**：安装缺少的模块：`pip install langchain-openai`

### 3. 超时错误

**问题**：`Request timed out`

**解决方案**：增加超时时间或检查网络连接。

## 下一步学习

1. **深入了解LCEL**：学习如何使用LangChain Expression Language构建更复杂的链
2. **探索代理类型**：了解不同类型的代理及其使用场景
3. **学习向量存储**：了解如何使用向量存储构建检索增强生成（RAG）系统
4. **构建完整应用**：尝试构建一个完整的基于LangChain的应用程序

## 参考资源

- [LangChain官方文档](https://python.langchain.com/docs/get_started/introduction)
- [LangChain GitHub仓库](https://github.com/langchain-ai/langchain)
- [LangChain中文注释项目](https://github.com/yourusername/langchain_code_comment)

---

通过本教程，您应该已经掌握了LangChain的基本使用方法，可以开始构建自己的基于大语言模型的应用程序了。祝您在LangChain的学习和应用过程中取得成功！