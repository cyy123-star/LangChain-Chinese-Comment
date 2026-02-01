# LangChain 关键函数和 API 解析

## 1. 核心执行协议 (Runnable)

### 1.1 Runnable 接口

`Runnable` 是LangChain的核心接口，定义了统一的执行协议。所有可执行组件都实现了这个接口，使得它们可以被组合、链式调用和并行执行。

#### 1.1.1 invoke 方法

```python
def invoke(self, input: Input, config: RunnableConfig | None = None, **kwargs: Any) -> Output:
    """转换单个输入为输出。

    参数:
        input: 输入数据
        config: 执行配置
        **kwargs: 额外的关键字参数

    返回:
        转换后的输出
    """
```

**使用场景**：适用于单个输入的同步执行，是最基本的执行方法。

**示例**：
```python
result = runnable.invoke({"question": "什么是LangChain？"})
```

#### 1.1.2 batch 方法

```python
def batch(self, inputs: list[Input], config: RunnableConfig | list[RunnableConfig] | None = None, *, return_exceptions: bool = False, **kwargs: Any | None) -> list[Output]:
    """批量处理多个输入。

    参数:
        inputs: 输入列表
        config: 执行配置或配置列表
        return_exceptions: 是否返回异常而不是抛出
        **kwargs: 额外的关键字参数

    返回:
        输出列表
    """
```

**使用场景**：适用于多个相似请求的批量处理，提高性能。

**示例**：
```python
results = runnable.batch([{"question": "什么是LangChain？"}, {"question": "LangChain的优势是什么？"}])
```

#### 1.1.3 stream 方法

```python
def stream(self, input: Input, config: RunnableConfig | None = None, **kwargs: Any | None) -> Iterator[Output]:
    """流式处理输出。

    参数:
        input: 输入数据
        config: 执行配置
        **kwargs: 额外的关键字参数

    返回:
        输出迭代器
    """
```

**使用场景**：适用于需要实时反馈的长响应，如聊天应用。

**示例**：
```python
for chunk in runnable.stream({"question": "写一篇关于人工智能的文章"}):
    print(chunk, end="", flush=True)
```

#### 1.1.4 ainvoke 方法

```python
async def ainvoke(self, input: Input, config: RunnableConfig | None = None, **kwargs: Any) -> Output:
    """异步转换单个输入为输出。

    参数:
        input: 输入数据
        config: 执行配置
        **kwargs: 额外的关键字参数

    返回:
        转换后的输出
    """
```

**使用场景**：适用于异步环境中的单个输入执行。

**示例**：
```python
result = await runnable.ainvoke({"question": "什么是LangChain？"})
```

#### 1.1.5 abatch 方法

```python
async def abatch(self, inputs: list[Input], config: RunnableConfig | list[RunnableConfig] | None = None, *, return_exceptions: bool = False, **kwargs: Any | None) -> list[Output]:
    """异步批量处理多个输入。

    参数:
        inputs: 输入列表
        config: 执行配置或配置列表
        return_exceptions: 是否返回异常而不是抛出
        **kwargs: 额外的关键字参数

    返回:
        输出列表
    """
```

**使用场景**：适用于异步环境中的批量处理。

**示例**：
```python
results = await runnable.abatch([{"question": "什么是LangChain？"}, {"question": "LangChain的优势是什么？"}])
```

#### 1.1.6 astream 方法

```python
async def astream(self, input: Input, config: RunnableConfig | None = None, **kwargs: Any | None) -> AsyncIterator[Output]:
    """异步流式处理输出。

    参数:
        input: 输入数据
        config: 执行配置
        **kwargs: 额外的关键字参数

    返回:
        异步输出迭代器
    """
```

**使用场景**：适用于异步环境中的流式输出。

**示例**：
```python
async for chunk in runnable.astream({"question": "写一篇关于人工智能的文章"}):
    print(chunk, end="", flush=True)
```

#### 1.1.7 astream_events 方法

```python
async def astream_events(self, input: Any, config: RunnableConfig | None = None, *, version: Literal["v1", "v2"] = "v2", include_names: Sequence[str] | None = None, include_types: Sequence[str] | None = None, include_tags: Sequence[str] | None = None, exclude_names: Sequence[str] | None = None, exclude_types: Sequence[str] | None = None, exclude_tags: Sequence[str] | None = None, **kwargs: Any) -> AsyncIterator[StreamEvent]:
    """生成事件流。

    参数:
        input: 输入数据
        config: 执行配置
        version: 事件格式版本
        include_names: 包含的组件名称
        include_types: 包含的事件类型
        include_tags: 包含的标签
        exclude_names: 排除的组件名称
        exclude_types: 排除的事件类型
        exclude_tags: 排除的标签
        **kwargs: 额外的关键字参数

    返回:
        事件异步迭代器
    """
```

**使用场景**：适用于需要监控执行过程的场景，如调试和监控。

**示例**：
```python
async for event in runnable.astream_events({"question": "什么是LangChain？"}, version="v2"):
    print(event)
```

### 1.2 组合操作

#### 1.2.1 __or__ 操作符

```python
def __or__(self, other: Runnable[Any, Other] | Callable[[Iterator[Any]], Iterator[Other]] | Callable[[AsyncIterator[Any]], AsyncIterator[Other]] | Callable[[Any], Other] | Mapping[str, Runnable[Any, Other] | Callable[[Any], Other] | Any]) -> RunnableSerializable[Input, Other]:
    """Runnable "or" 操作符，用于创建顺序执行的链。

    参数:
        other: 另一个Runnable或可调用对象

    返回:
        组合后的Runnable
    """
```

**使用场景**：适用于创建顺序执行的链，是最常用的组合方式。

**示例**：
```python
chain = prompt | model | output_parser
```

#### 1.2.2 pipe 方法

```python
def pipe(self, *others: Runnable[Any, Other] | Callable[[Any], Other], name: str | None = None) -> RunnableSerializable[Input, Other]:
    """管道Runnable对象，创建顺序执行的链。

    参数:
        *others: 其他Runnable或可调用对象
        name: 链的名称

    返回:
        组合后的Runnable
    """
```

**使用场景**：适用于创建顺序执行的链，与 `|` 操作符类似。

**示例**：
```python
chain = prompt.pipe(model).pipe(output_parser)
```

#### 1.2.3 assign 方法

```python
def assign(self, **kwargs: Runnable[dict[str, Any], Any] | Callable[[dict[str, Any]], Any] | Mapping[str, Runnable[dict[str, Any], Any] | Callable[[dict[str, Any]], Any]]) -> RunnableSerializable[Any, Any]:
    """向输出字典添加新字段。

    参数:
        **kwargs: 字段名到Runnable或可调用对象的映射

    返回:
        带有新字段的Runnable
    """
```

**使用场景**：适用于向输出字典添加新字段，常用于RAG系统中添加额外信息。

**示例**：
```python
chain = retriever | RunnableAssign({"summary": lambda x: summarize(x["documents"])})
```

#### 1.2.4 pick 方法

```python
def pick(self, keys: str | list[str]) -> RunnableSerializable[Any, Any]:
    """从输出字典中选择特定键。

    参数:
        keys: 要选择的键或键列表

    返回:
        只包含选定键的Runnable
    """
```

**使用场景**：适用于从输出字典中选择特定键，简化输出结构。

**示例**：
```python
chain = runnable | RunnablePick("result")
```

## 2. 提示模板系统

### 2.1 ChatPromptTemplate

```python
class ChatPromptTemplate(BasePromptTemplate):
    """聊天提示模板，用于构建聊天模型的提示。

    方法:
        from_messages(messages): 从消息列表创建聊天提示模板
        format_prompt(**kwargs): 格式化提示
        format_messages(**kwargs): 格式化消息
    """
```

**使用场景**：适用于构建聊天模型的提示，是最常用的提示模板类型。

**示例**：
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 helpful 的助手。"),
    ("human", "{question}")
])
```

### 2.2 PromptTemplate

```python
class PromptTemplate(BasePromptTemplate):
    """基本提示模板，用于构建文本模型的提示。

    方法:
        from_template(template): 从模板字符串创建提示模板
        format(**kwargs): 格式化提示
    """
```

**使用场景**：适用于构建文本模型的提示，如传统的LLM。

**示例**：
```python
prompt = PromptTemplate.from_template("回答以下问题: {question}")
```

### 2.3 FewShotPromptTemplate

```python
class FewShotPromptTemplate(BasePromptTemplate):
    """少样本提示模板，用于提供示例。

    方法:
        from_examples(examples, example_prompt, prefix, suffix, input_variables): 从示例创建少样本提示模板
    """
```

**使用场景**：适用于需要提供示例的复杂任务，如代码生成、格式转换等。

**示例**：
```python
prompt = FewShotPromptTemplate.from_examples(
    examples=[
        {"input": "1 + 1", "output": "2"},
        {"input": "2 + 2", "output": "4"}
    ],
    example_prompt=PromptTemplate.from_template("输入: {input}\n输出: {output}"),
    prefix="计算以下数学表达式:",
    suffix="输入: {input}\n输出:",
    input_variables=["input"]
)
```

## 3. 语言模型

### 3.1 ChatOpenAI

```python
class ChatOpenAI(BaseChatModel):
    """OpenAI的聊天模型集成。

    参数:
        model_name: 模型名称，如 "gpt-3.5-turbo", "gpt-4"
        temperature: 生成温度，控制输出的随机性
        max_tokens: 最大生成token数
        api_key: OpenAI API密钥
        organization: OpenAI组织ID

    方法:
        invoke(input, config=None, **kwargs): 执行模型
        stream(input, config=None, **kwargs): 流式执行模型
    """
```

**使用场景**：适用于需要使用OpenAI聊天模型的场景，如对话、问答等。

**示例**：
```python
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
result = model.invoke([HumanMessage(content="什么是LangChain？")])
```

### 3.2 OpenAI

```python
class OpenAI(LLM):
    """OpenAI的文本模型集成。

    参数:
        model_name: 模型名称，如 "text-davinci-003"
        temperature: 生成温度，控制输出的随机性
        max_tokens: 最大生成token数
        api_key: OpenAI API密钥
        organization: OpenAI组织ID

    方法:
        invoke(input, config=None, **kwargs): 执行模型
        stream(input, config=None, **kwargs): 流式执行模型
    """
```

**使用场景**：适用于需要使用OpenAI文本模型的场景，如文本生成、摘要等。

**示例**：
```python
model = OpenAI(model_name="text-davinci-003", temperature=0.7)
result = model.invoke("写一篇关于人工智能的文章")
```

## 4. 文档处理

### 4.1 TextLoader

```python
class TextLoader(BaseLoader):
    """文本文件加载器。

    参数:
        file_path: 文件路径
        encoding: 文件编码
        autodetect_encoding: 是否自动检测编码

    方法:
        load(): 加载文档
    """
```

**使用场景**：适用于加载文本文件，如.txt文件。

**示例**：
```python
loader = TextLoader("docs/introduction.txt")
documents = loader.load()
```

### 4.2 PyPDFLoader

```python
class PyPDFLoader(BaseLoader):
    """PDF文件加载器。

    参数:
        file_path: 文件路径
        password: PDF密码

    方法:
        load(): 加载文档
    """
```

**使用场景**：适用于加载PDF文件，如手册、报告等。

**示例**：
```python
loader = PyPDFLoader("docs/manual.pdf")
documents = loader.load()
```

### 4.3 RecursiveCharacterTextSplitter

```python
class RecursiveCharacterTextSplitter(TextSplitter):
    """递归字符文本分割器，用于将文本分割成块。

    参数:
        chunk_size: 块大小
        chunk_overlap: 块重叠大小
        length_function: 长度计算函数
        separators: 分隔符列表

    方法:
        split_text(text): 分割文本
        split_documents(documents): 分割文档
    """
```

**使用场景**：适用于将长文本分割成块，是最常用的文本分割器。

**示例**：
```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
document_chunks = text_splitter.split_documents(documents)
```

## 5. 向量存储和检索

### 5.1 Chroma

```python
class Chroma(VectorStore):
    """Chroma向量数据库集成。

    参数:
        collection_name: 集合名称
        embedding_function: 嵌入函数
        persist_directory: 持久化目录

    方法:
        from_documents(documents, embedding, collection_name=None, persist_directory=None): 从文档创建Chroma实例
        add_documents(documents): 添加文档
        similarity_search(query, k=4): 相似性搜索
        as_retriever(search_kwargs=None): 创建检索器
    """
```

**使用场景**：适用于需要向量存储和相似性搜索的场景，如RAG系统。

**示例**：
```python
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()
```

### 5.2 FAISS

```python
class FAISS(VectorStore):
    """FAISS向量数据库集成。

    参数:
        index: FAISS索引
        embedding_function: 嵌入函数
        texts: 文本列表
        metadatas: 元数据列表

    方法:
        from_documents(documents, embedding): 从文档创建FAISS实例
        add_documents(documents): 添加文档
        similarity_search(query, k=4): 相似性搜索
        as_retriever(search_kwargs=None): 创建检索器
        save_local(folder_path): 保存到本地
        load_local(folder_path, embedding): 从本地加载
    """
```

**使用场景**：适用于需要高性能向量搜索的场景，如大规模文档检索。

**示例**：
```python
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("vectorstore")
```

## 6. 智能代理

### 6.1 create_openai_functions_agent

```python
def create_openai_functions_agent(llm: BaseLanguageModel, tools: Sequence[BaseTool], prompt: BasePromptTemplate) -> Agent:
    """创建OpenAI函数调用代理。

    参数:
        llm: 语言模型
        tools: 工具列表
        prompt: 提示模板

    返回:
        代理实例
    """
```

**使用场景**：适用于创建使用OpenAI函数调用功能的代理，是最常用的代理创建方法。

**示例**：
```python
agent = create_openai_functions_agent(model, tools, prompt)
```

### 6.2 AgentExecutor

```python
class AgentExecutor(Runnable):
    """代理执行器，负责运行代理。

    参数:
        agent: 代理实例
        tools: 工具列表
        verbose: 是否显示详细信息
        return_only_outputs: 是否只返回输出
        max_iterations: 最大迭代次数
        max_execution_time: 最大执行时间
        early_stopping_method: 早停方法
        memory: 内存实例

    方法:
        invoke(input, config=None, **kwargs): 执行代理
    """
```

**使用场景**：适用于运行代理，是代理执行的核心组件。

**示例**：
```python
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = executor.invoke({"input": "2023年世界杯冠军是谁？"})
```

### 6.3 tool 装饰器

```python
def tool(func: Callable) -> BaseTool:
    """工具装饰器，用于将函数转换为工具。

    参数:
        func: 要转换的函数

    返回:
        工具实例
    """
```

**使用场景**：适用于创建工具，是最常用的工具创建方法。

**示例**：
```python
@tool
def search(query: str) -> str:
    """搜索网络获取信息"""
    return f"搜索结果：关于 {query} 的信息"
```

## 7. 内存管理

### 7.1 ConversationBufferMemory

```python
class ConversationBufferMemory(BaseMemory):
    """简单的对话缓冲区内存。

    参数:
        memory_key: 内存键名
        return_messages: 是否返回消息对象
        output_key: 输出键名
        input_key: 输入键名

    方法:
        load_memory_variables(inputs): 加载内存变量
        save_context(inputs, outputs): 保存上下文
        clear(): 清空内存
    """
```

**使用场景**：适用于简单的对话记忆，保存整个对话历史。

**示例**：
```python
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
```

### 7.2 ConversationSummaryMemory

```python
class ConversationSummaryMemory(BaseMemory):
    """对话摘要内存，保存对话摘要。

    参数:
        llm: 语言模型，用于生成摘要
        memory_key: 内存键名
        return_messages: 是否返回消息对象
        output_key: 输出键名
        input_key: 输入键名
        summary_prompt: 摘要提示模板

    方法:
        load_memory_variables(inputs): 加载内存变量
        save_context(inputs, outputs): 保存上下文
        clear(): 清空内存
    """
```

**使用场景**：适用于长对话，通过摘要减少内存使用。

**示例**：
```python
memory = ConversationSummaryMemory(llm=model, memory_key="chat_history", return_messages=True)
```

## 8. 输出解析器

### 8.1 StrOutputParser

```python
class StrOutputParser(Runnable):
    """字符串输出解析器，将模型输出转换为字符串。

    方法:
        invoke(input, config=None, **kwargs): 解析输出
    """
```

**使用场景**：适用于将模型输出转换为字符串，是最常用的输出解析器。

**示例**：
```python
output_parser = StrOutputParser()
result = output_parser.invoke(model_output)
```

### 8.2 JsonOutputParser

```python
class JsonOutputParser(Runnable):
    """JSON输出解析器，将模型输出转换为JSON。

    参数:
        pydantic_object: Pydantic模型类，用于验证输出

    方法:
        invoke(input, config=None, **kwargs): 解析输出
        get_format_instructions(): 获取格式说明
    """
```

**使用场景**：适用于需要JSON格式输出的场景，如结构化数据提取。

**示例**：
```python
class Answer(BaseModel):
    answer: str
    confidence: float

parser = JsonOutputParser(pydantic_object=Answer)
prompt = PromptTemplate(template="回答问题并提供置信度：{question}\n{format_instructions}", input_variables=["question"], partial_variables={"format_instructions": parser.get_format_instructions()})
```

## 9. 配置和扩展

### 9.1 with_config 方法

```python
def with_config(self, config: RunnableConfig) -> RunnableSerializable[Input, Output]:
    """为组件添加配置。

    参数:
        config: 执行配置

    返回:
        带有配置的Runnable
    """
```

**使用场景**：适用于为组件添加配置，如运行名称、标签等。

**示例**：
```python
runnable = runnable.with_config({"run_name": "MyRunnable", "tags": ["production"]})
```

### 9.2 configurable_fields 方法

```python
def configurable_fields(self, **kwargs: AnyConfigurableField) -> RunnableSerializable[Input, Output]:
    """标记可配置字段。

    参数:
        **kwargs: 字段名到可配置字段的映射

    返回:
        带有可配置字段的Runnable
    """
```

**使用场景**：适用于标记可配置字段，允许在运行时修改组件行为。

**示例**：
```python
runnable = runnable.configurable_fields(
    temperature=ConfigurableField(id="temperature", name="Temperature", description="生成温度", default=0.7)
)
```

## 10. 实用工具

### 10.1 RunnableLambda

```python
class RunnableLambda(Runnable):
    """包装普通函数为Runnable。

    参数:
        func: 要包装的函数
        name: 名称

    方法:
        invoke(input, config=None, **kwargs): 执行函数
    """
```

**使用场景**：适用于将普通函数转换为Runnable，是最常用的Runnable创建方法。

**示例**：
```python
runnable = RunnableLambda(lambda x: x + 1)
```

### 10.2 RunnableParallel

```python
class RunnableParallel(Runnable):
    """并行执行多个Runnable。

    参数:
        steps: Runnable映射

    方法:
        invoke(input, config=None, **kwargs): 执行Runnable
    """
```

**使用场景**：适用于并行执行多个Runnable，提高性能。

**示例**：
```python
parallel = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain
)
```

### 10.3 RunnablePassthrough

```python
class RunnablePassthrough(Runnable):
    """透传输入的Runnable。

    方法:
        invoke(input, config=None, **kwargs): 透传输入
    """
```

**使用场景**：适用于透传输入，常用于链中保持输入不变。

**示例**：
```python
chain = {"question": RunnablePassthrough()} | prompt | model
```

## 11. 总结

LangChain提供了丰富的函数和API，使得构建LLM应用变得更加简单和灵活。本文档涵盖了LangChain中最常用和最重要的函数和API，包括核心执行协议、提示模板系统、语言模型集成、文档处理、向量存储和检索、智能代理、内存管理、输出解析器、配置和扩展以及实用工具等方面。

通过掌握这些函数和API，开发者可以：

- 构建各种类型的LLM应用，从简单的问答系统到复杂的智能代理
- 充分利用LangChain的模块化设计，快速组合和扩展功能
- 优化应用性能，提高用户体验
- 实现复杂的业务逻辑，满足各种需求

随着LangChain的不断发展，这些函数和API也在不断完善和扩展。开发者应该关注LangChain的官方文档和更新，以获取最新的信息和最佳实践。
