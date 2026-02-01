# LangChain 使用示例和最佳实践

## 1. 基础使用示例

### 1.1 简单的 LLM 调用

**功能说明**：使用 LangChain 调用语言模型生成文本。

**代码示例**：

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# 创建提示模板
prompt = PromptTemplate(
    template="请写一篇关于 {topic} 的短文，长度约 200 字。",
    input_variables=["topic"]
)

# 创建模型实例
llm = OpenAI(
    model_name="text-davinci-003",
    temperature=0.7,
    max_tokens=300
)

# 创建链
chain = prompt | llm

# 执行链
result = chain.invoke({"topic": "人工智能的未来"})
print(result)
```

**最佳实践**：
- 根据任务类型选择合适的模型
- 调整 temperature 参数以平衡创造力和准确性
- 设置合理的 max_tokens 以控制输出长度

### 1.2 聊天模型使用

**功能说明**：使用聊天模型进行对话交互。

**代码示例**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# 创建聊天提示模板
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是一个友好的助手，能够回答各种问题。"),
    HumanMessage(content="{question}")
])

# 创建聊天模型实例
chat_model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7
)

# 创建链
chain = prompt | chat_model

# 执行链
result = chain.invoke({"question": "什么是 LangChain？"})
print(result.content)
```

**最佳实践**：
- 使用 SystemMessage 设置助手的角色和行为
- 对于多轮对话，保存对话历史并在每次调用时包含
- 使用流式输出提高用户体验

### 1.3 提示模板使用

**功能说明**：使用不同类型的提示模板构建复杂提示。

**代码示例**：

```python
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# 1. 基本提示模板
basic_prompt = PromptTemplate(
    template="{greeting}, {name}！今天过得怎么样？",
    input_variables=["greeting", "name"]
)

# 2. 聊天提示模板
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是一个专业的 {role}。"),
    HumanMessagePromptTemplate.from_template("{question}")
])

# 3. 少样本提示模板
examples = [
    {"input": "1 + 1", "output": "2"},
    {"input": "2 + 2", "output": "4"},
    {"input": "3 + 3", "output": "6"}
]

example_prompt = PromptTemplate(
    template="输入: {input}\n输出: {output}",
    input_variables=["input", "output"]
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="计算以下数学表达式:",
    suffix="输入: {input}\n输出:",
    input_variables=["input"]
)

# 使用示例
print("基本提示模板:")
print(basic_prompt.format(greeting="你好", name="张三"))

print("\n聊天提示模板:")
print(chat_prompt.format(role="程序员", question="如何使用 Python 函数？"))

print("\n少样本提示模板:")
print(few_shot_prompt.format(input="4 + 4"))
```

**最佳实践**：
- 根据任务类型选择合适的提示模板类型
- 使用少样本提示模板提供示例，帮助模型理解任务
- 对于复杂任务，使用结构化提示提高清晰度

## 2. 中级使用示例

### 2.1 文档处理和摘要

**功能说明**：加载文档并生成摘要。

**代码示例**：

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载文档
loader = TextLoader("docs/introduction.txt")
documents = loader.load()

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
document_chunks = text_splitter.split_documents(documents)

# 创建摘要提示模板
summary_prompt = PromptTemplate(
    template="请摘要以下文档内容，长度约 150 字：\n\n{document}",
    input_variables=["document"]
)

# 创建模型
llm = OpenAI(temperature=0.3)

# 创建链
chain = summary_prompt | llm

# 处理每个文档块
for i, chunk in enumerate(document_chunks):
    print(f"\n--- 文档块 {i+1} 摘要 ---")
    result = chain.invoke({"document": chunk.page_content})
    print(result)
```

**最佳实践**：
- 根据文档类型选择合适的加载器
- 优化分割策略以适应文档结构
- 对于长文档，考虑使用摘要链或映射-归约模式

### 2.2 检索增强生成 (RAG)

**功能说明**：从文档中检索相关信息并生成回答。

**代码示例**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载文档
loader = TextLoader("docs/introduction.txt")
documents = loader.load()

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
document_chunks = text_splitter.split_documents(documents)

# 创建嵌入
embeddings = OpenAIEmbeddings()

# 创建向量存储
vectorstore = Chroma.from_documents(
    documents=document_chunks,
    embedding=embeddings
)

# 创建检索器
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}  # 检索前 3 个最相关的文档
)

# 创建提示模板
rag_prompt = ChatPromptTemplate.from_template("""
你是一个专业的问答助手，请根据以下文档内容回答问题。

文档内容：
{context}

问题：
{question}

回答：
""")

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建 RAG 链
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | model
    | StrOutputParser()
)

# 执行链
result = rag_chain.invoke("LangChain 的主要功能是什么？")
print(result)
```

**最佳实践**：
- 选择合适的向量存储以适应规模和性能需求
- 优化检索参数以提高相关性
- 设计有效的提示模板以引导模型使用检索到的信息

### 2.3 智能代理

**功能说明**：创建能够使用工具的智能代理。

**代码示例**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor

# 定义工具
@tool
def search(query: str) -> str:
    """搜索网络获取关于特定主题的最新信息"""
    # 这里是模拟搜索结果
    return f"搜索结果：关于 '{query}' 的最新信息显示，这是一个重要的主题，有很多相关内容。"

@tool
def calculate(expression: str) -> str:
    """计算数学表达式的结果"""
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"

# 创建工具列表
tools = [search, calculate]

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一个智能助手，能够使用工具来帮助用户解决问题。\n" 
        "请根据用户的问题，选择合适的工具来获取信息或执行计算。\n" 
        "如果需要使用工具，请使用正确的工具名称和参数。\n" 
        "请保持回答简洁明了，直接提供用户需要的信息。"
    ),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])

# 创建模型
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

# 创建代理
agent = create_openai_functions_agent(model, tools, prompt)

# 创建代理执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_only_outputs=True
)

# 执行代理
result = agent_executor.invoke({
    "input": "2023 年世界杯冠军是谁？另外，请计算 12345 乘以 67890 的结果。"
})

print("\n代理回答：")
print(result["output"])
```

**最佳实践**：
- 为工具提供清晰详细的描述
- 设计有效的提示模板以引导代理行为
- 设置合理的最大迭代次数以防止无限循环

## 3. 高级使用示例

### 3.1 多代理协作

**功能说明**：创建多个专业代理并让它们协作完成复杂任务。

**代码示例**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory

# 定义工具
@tool
def research_topic(topic: str) -> str:
    """研究特定主题的详细信息"""
    return f"关于 '{topic}' 的研究结果：这是一个重要的主题，包含很多详细信息。"

@tool
def write_report(topic: str, research: str) -> str:
    """根据研究结果撰写报告"""
    return f"基于研究结果，我已经撰写了关于 '{topic}' 的详细报告。"

@tool
def edit_report(report: str) -> str:
    """编辑和优化报告内容"""
    return f"我已经编辑和优化了报告，使其更加清晰和专业。"

# 创建研究代理
research_tools = [research_topic]
research_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的研究人员，擅长收集和整理信息。"),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])

# 创建写作代理
writing_tools = [write_report]
writing_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的作家，擅长撰写清晰、专业的报告。"),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])

# 创建编辑代理
editing_tools = [edit_report]
editing_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的编辑，擅长优化和改进文档。"),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])

# 创建模型
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

# 创建代理
research_agent = create_openai_functions_agent(model, research_tools, research_prompt)
writing_agent = create_openai_functions_agent(model, writing_tools, writing_prompt)
editing_agent = create_openai_functions_agent(model, editing_tools, editing_prompt)

# 创建代理执行器
research_executor = AgentExecutor(
    agent=research_agent,
    tools=research_tools,
    verbose=True,
    return_only_outputs=True
)

writing_executor = AgentExecutor(
    agent=writing_agent,
    tools=writing_tools,
    verbose=True,
    return_only_outputs=True
)

editing_executor = AgentExecutor(
    agent=editing_agent,
    tools=editing_tools,
    verbose=True,
    return_only_outputs=True
)

# 执行多代理协作流程
topic = "人工智能在医疗领域的应用"

# 1. 研究阶段
print("=== 研究阶段 ===")
research_result = research_executor.invoke({"input": f"请研究 '{topic}' 的最新发展和应用案例。"})
research_content = research_result["output"]
print(research_content)

# 2. 写作阶段
print("\n=== 写作阶段 ===")
writing_result = writing_executor.invoke({"input": f"请根据以下研究结果撰写一份关于 '{topic}' 的报告：\n{research_content}"})
report_content = writing_result["output"]
print(report_content)

# 3. 编辑阶段
print("\n=== 编辑阶段 ===")
editing_result = editing_executor.invoke({"input": f"请编辑和优化以下报告：\n{report_content}"})
final_report = editing_result["output"]
print(final_report)

print("\n=== 最终报告 ===")
print(final_report)
```

**最佳实践**：
- 为每个代理定义明确的角色和职责
- 设计有效的代理间通信机制
- 实现错误处理和回退策略

### 3.2 复杂工作流

**功能说明**：构建包含多个步骤的复杂工作流。

**代码示例**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建提示模板
topic_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个创意顾问，擅长生成有趣的讨论主题。"),
    ("human", "请为 {audience} 生成 3 个关于 {category} 的讨论主题。")
])

outline_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个内容策划师，擅长为主题创建详细大纲。"),
    ("human", "请为以下主题创建一个详细的讨论大纲：{topic}")
])

content_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业作家，擅长根据大纲撰写内容。"),
    ("human", "请根据以下大纲撰写详细内容：{outline}")
])

# 创建链
topic_chain = topic_prompt | model | StrOutputParser()
outline_chain = outline_prompt | model | StrOutputParser()
content_chain = content_prompt | model | StrOutputParser()

# 创建并行链以生成多个主题
parallel_topics = RunnableParallel(
    topic1=RunnableSequence(lambda x: {"audience": x["audience"], "category": x["category"]}) | topic_chain,
    topic2=RunnableSequence(lambda x: {"audience": x["audience"], "category": x["category"]}) | topic_chain,
    topic3=RunnableSequence(lambda x: {"audience": x["audience"], "category": x["category"]}) | topic_chain
)

# 创建完整工作流
workflow = RunnableSequence(
    # 1. 生成主题
    parallel_topics,
    # 2. 为每个主题创建大纲
    lambda topics: {
        "outline1": outline_chain.invoke({"topic": topics["topic1"]}),
        "outline2": outline_chain.invoke({"topic": topics["topic2"]}),
        "outline3": outline_chain.invoke({"topic": topics["topic3"]})
    },
    # 3. 为每个大纲生成内容
    lambda outlines: {
        "content1": content_chain.invoke({"outline": outlines["outline1"]}),
        "content2": content_chain.invoke({"outline": outlines["outline2"]}),
        "content3": content_chain.invoke({"outline": outlines["outline3"]})
    }
)

# 执行工作流
result = workflow.invoke({
    "audience": "数据科学家",
    "category": "机器学习"
})

# 输出结果
for i in range(1, 4):
    print(f"\n--- 内容 {i} ---")
    print(result[f"content{i}"])
```

**最佳实践**：
- 使用 RunnableParallel 并行执行独立任务
- 使用 RunnableSequence 构建顺序工作流
- 设计清晰的数据传递机制

## 4. 最佳实践

### 4.1 性能优化

**批处理**

**功能说明**：使用批处理提高多个相似请求的处理效率。

**代码示例**：

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# 创建提示模板
prompt = PromptTemplate(
    template="请为 {product} 生成一句简短的广告语。",
    input_variables=["product"]
)

# 创建模型
llm = OpenAI(temperature=0.7)

# 创建链
chain = prompt | llm

# 批量处理多个请求
products = ["智能手机", "笔记本电脑", "智能手表", "平板电脑"]
inputs = [{"product": product} for product in products]

# 执行批处理
results = chain.batch(inputs)

# 输出结果
for product, result in zip(products, results):
    print(f"\n{product}: {result.strip()}")
```

**流式输出**

**功能说明**：使用流式输出提高用户体验。

**代码示例**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的作家，擅长撰写详细的文章。"),
    ("human", "请写一篇关于 {topic} 的详细文章，长度约 500 字。")
])

# 创建模型
model = ChatOpenAI(temperature=0.7)

# 创建链
chain = prompt | model

# 执行流式输出
print("正在生成文章...\n")
for chunk in chain.stream({"topic": "人工智能的伦理问题"}):
    if hasattr(chunk, 'content') and chunk.content:
        print(chunk.content, end="", flush=True)
```

### 4.2 提示工程

**结构化提示**

**功能说明**：使用结构化提示提高模型理解和输出质量。

**代码示例**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 创建结构化提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的产品评论家，擅长分析产品的优缺点。\n" 
     "请按照以下结构分析产品：\n" 
     "1. 产品概述\n" 
     "2. 优点（至少 3 点）\n" 
     "3. 缺点（至少 2 点）\n" 
     "4. 改进建议\n" 
     "5. 总体评价"),
    ("human", "请分析 {product}。")
])

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建链
chain = prompt | model | StrOutputParser()

# 执行链
result = chain.invoke({"product": "最新款智能手机"})
print(result)
```

**少样本提示**

**功能说明**：使用少样本提示帮助模型理解复杂任务。

**代码示例**：

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import OpenAI

# 示例
examples = [
    {
        "input": "将 '我喜欢编程' 翻译成英语",
        "output": "I like programming"
    },
    {
        "input": "将 '今天天气很好' 翻译成英语",
        "output": "The weather is nice today"
    },
    {
        "input": "将 '我想吃苹果' 翻译成英语",
        "output": "I want to eat an apple"
    }
]

# 创建示例提示模板
example_prompt = PromptTemplate(
    template="输入: {input}\n输出: {output}",
    input_variables=["input", "output"]
)

# 创建少样本提示模板
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请按照示例将中文翻译成英语：",
    suffix="输入: {input}\n输出:",
    input_variables=["input"]
)

# 创建模型
llm = OpenAI(temperature=0.0)

# 创建链
chain = prompt | llm

# 执行链
result = chain.invoke({"input": "将 '我爱学习 LangChain' 翻译成英语"})
print(result)
```

### 4.3 错误处理

**重试机制**

**功能说明**：使用重试机制处理临时故障。

**代码示例**：

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.runnables import RunnableLambda

# 创建模型
llm = OpenAI(temperature=0.7)

# 创建提示模板
prompt = PromptTemplate(
    template="请写一篇关于 {topic} 的短文。",
    input_variables=["topic"]
)

# 创建带重试的链
chain = prompt | llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

# 执行链
result = chain.invoke({"topic": "人工智能的未来"})
print(result)
```

**异常处理**

**功能说明**：使用异常处理提高系统可靠性。

**代码示例**：

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# 创建模型
llm = OpenAI(temperature=0.7)

# 创建提示模板
prompt = PromptTemplate(
    template="请写一篇关于 {topic} 的短文。",
    input_variables=["topic"]
)

# 创建链
chain = prompt | llm

# 执行链并处理异常
try:
    result = chain.invoke({"topic": "人工智能的未来"})
    print(result)
except Exception as e:
    print(f"发生错误: {str(e)}")
    # 提供备用响应
    print("系统暂时无法生成内容，请稍后再试。")
```

### 4.4 部署和监控

**使用 LangSmith**

**功能说明**：使用 LangSmith 监控和评估 LLM 应用。

**代码示例**：

```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 设置 LangSmith 环境变量
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的助手，能够回答各种问题。"),
    ("human", "{question}")
])

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建链
chain = prompt | model

# 执行链
result = chain.invoke({"question": "什么是 LangChain？"})
print(result.content)

# 现在可以在 LangSmith 中查看执行情况
print("\n执行详情已发送到 LangSmith，请登录查看。")
```

**日志记录**

**功能说明**：实现详细的日志记录。

**代码示例**：

```python
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StdOutCallbackHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的助手。"),
    ("human", "{question}")
])

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建链
chain = prompt | model

# 执行链并记录日志
logger.info("开始执行链")
try:
    result = chain.invoke(
        {"question": "什么是 LangChain？"},
        config={"callbacks": [StdOutCallbackHandler()]}
    )
    logger.info("链执行成功")
    print("\n模型回答:")
    print(result.content)
except Exception as e:
    logger.error(f"链执行失败: {str(e)}")
    print(f"错误: {str(e)}")
```

## 5. 常见场景解决方案

### 5.1 问答系统

**功能说明**：构建基于文档的问答系统。

**解决方案**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载文档
loader = PyPDFLoader("docs/manual.pdf")
documents = loader.load()

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
document_chunks = text_splitter.split_documents(documents)

# 创建嵌入
embeddings = OpenAIEmbeddings()

# 创建向量存储
vectorstore = FAISS.from_documents(
    documents=document_chunks,
    embedding=embeddings
)

# 保存向量存储
vectorstore.save_local("vectorstore")

# 加载向量存储
# vectorstore = FAISS.load_local("vectorstore", embeddings)

# 创建检索器
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的问答助手，能够根据提供的文档回答问题。\n" 
     "请严格根据文档内容回答问题，不要添加文档中没有的信息。\n" 
     "如果文档中没有相关信息，请明确说明。"),
    ("human", "文档内容：\n{context}\n\n问题：{question}")
])

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建链
chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)

# 测试问答
questions = [
    "产品的主要功能是什么？",
    "如何安装和配置产品？",
    "产品的系统要求是什么？",
    "如何 troubleshooting 常见问题？"
]

for question in questions:
    print(f"\n=== 问题: {question} ===")
    result = chain.invoke(question)
    print(result)
```

### 5.2 内容生成

**功能说明**：构建内容生成系统。

**解决方案**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 创建模型
model = ChatOpenAI(temperature=0.7)

# 创建提示模板
title_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个创意作家，擅长生成吸引人的标题。"),
    ("human", "请为关于 {topic} 的文章生成 5 个吸引人的标题。")
])

outline_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个内容策划师，擅长为文章创建详细大纲。"),
    ("human", "请为标题为 '{title}' 的文章创建详细大纲。")
])

content_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的作家，擅长根据大纲撰写详细的文章。"),
    ("human", "请根据以下大纲撰写详细的文章，长度约 800 字：\n{outline}")
])

# 创建链
title_chain = title_prompt | model | StrOutputParser()
outline_chain = outline_prompt | model | StrOutputParser()
content_chain = content_prompt | model | StrOutputParser()

# 执行内容生成流程
topic = "远程工作的未来"

print("=== 生成标题 ===")
titles = title_chain.invoke({"topic": topic})
print(titles)

# 选择一个标题
selected_title = titles.split("\n")[0].strip().lstrip("1. ").lstrip("-")
print(f"\n=== 选定标题 ===")
print(selected_title)

print("\n=== 生成大纲 ===")
outline = outline_chain.invoke({"title": selected_title})
print(outline)

print("\n=== 生成内容 ===")
content = content_chain.invoke({"outline": outline})
print(content)

print("\n=== 最终文章 ===")
print(f"# {selected_title}")
print(content)
```

### 5.3 数据分析

**功能说明**：使用 LLM 分析和解释数据。

**解决方案**：

```python
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 创建示例数据
data = {
    "产品": ["产品 A", "产品 B", "产品 C", "产品 D", "产品 E"],
    "销售额": [120000, 95000, 150000, 80000, 110000],
    "销售量": [1200, 950, 1500, 800, 1100],
    "地区": ["华东", "华北", "华南", "西南", "东北"]
}

df = pd.DataFrame(data)

# 将数据转换为字符串
data_str = df.to_string()

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建提示模板
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数据分析专家，擅长分析销售数据并提供洞察。"),
    ("human", "请分析以下销售数据，提供详细的分析报告，包括：\n" 
     "1. 总体销售情况\n" 
     "2. 各产品销售表现\n" 
     "3. 地区销售分布\n" 
     "4. 销售趋势和洞察\n" 
     "5. 改进建议\n\n" 
     "数据：\n{data}")
])

# 创建链
chain = analysis_prompt | model | StrOutputParser()

# 执行链
result = chain.invoke({"data": data_str})
print("=== 数据分析报告 ===")
print(result)
```

### 5.4 代码生成

**功能说明**：使用 LLM 生成和优化代码。

**解决方案**：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 创建模型
model = ChatOpenAI(temperature=0.3)

# 创建提示模板
code_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的 Python 程序员，擅长编写清晰、高效的代码。\n" 
     "请提供完整的代码，并添加适当的注释。\n" 
     "确保代码能够正确运行，并且符合 Python 最佳实践。"),
    ("human", "请编写一个 Python 函数，用于 {task}。\n" 
     "要求：\n{requirements}")
])

test_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的测试工程师，擅长为 Python 代码编写测试用例。"),
    ("human", "请为以下 Python 代码编写详细的测试用例：\n{code}")
])

# 创建链
code_chain = code_prompt | model | StrOutputParser()
test_chain = test_prompt | model | StrOutputParser()

# 执行代码生成
result = code_chain.invoke({
    "task": "计算斐波那契数列",
    "requirements": "\n".join([
        "1. 函数应该接受一个整数 n，返回第 n 个斐波那契数",
        "2. 实现递归和迭代两种方法",
        "3. 添加输入验证",
        "4. 包含详细的文档字符串"
    ])
})

print("=== 生成的代码 ===")
print(result)

# 生成测试用例
test_result = test_chain.invoke({"code": result})
print("\n=== 生成的测试用例 ===")
print(test_result)
```

## 6. 总结

LangChain 提供了丰富的工具和组件，使得构建 LLM 应用变得更加简单和灵活。通过本文档的示例和最佳实践，您应该能够：

1. **快速入门**：使用基础示例快速上手 LangChain
2. **构建复杂应用**：使用中级和高级示例构建更复杂的应用
3. **优化性能**：应用最佳实践提高应用性能和可靠性
4. **解决常见问题**：使用常见场景解决方案处理各种应用场景

**持续学习建议**：

- 关注 LangChain 的最新更新和功能
- 参与 LangChain 社区，学习和分享经验
- 尝试构建不同类型的应用，积累实践经验
- 关注提示工程和 LLM 技术的最新发展

通过不断学习和实践，您将能够充分利用 LangChain 的能力，构建创新的 LLM 应用，为用户创造价值。