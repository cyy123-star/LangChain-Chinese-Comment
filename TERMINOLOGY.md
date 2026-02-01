# LangChain 中英术语对照表

为了确保文档翻译的一致性与专业性，本项目统一使用以下术语对照表。在编写注释和文档时，请优先参考本表。

## 核心概念

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Chain | 链 | LangChain 的核心概念，代表一系列组件的调用序列 |
| Agent | 智能体 / 代理 | 能够根据任务选择并调用工具的实体 |
| Tool | 工具 | 智能体可以调用的功能模块 |
| Memory | 记忆 | 用于存储和检索对话历史的组件 |
| Prompt | 提示词 | 输入给大模型的指令或文本 |
| Prompt Template | 提示词模板 | 带有变量的提示词结构 |
| LLM (Large Language Model) | 大语言模型 | 如 GPT-4, Llama, Claude 等模型 |
| Chat Model | 聊天模型 | 专门用于对话格式的模型 |
| Document | 文档 | 包含文本和元数据的数据结构 |
| Loader | 加载器 | 用于将外部数据转换为 Document 的组件 |
| Splitter | 分割器 | 将长文档拆分为块（Chunk）的组件 |
| Vector Store | 向量数据库 | 存储和检索向量嵌入的系统 |
| Embedding | 嵌入 / 向量化 | 将文本转换为数值向量的过程 |
| Retriever | 检索器 | 根据查询获取相关文档的组件 |
| Output Parser | 输出解析器 | 将模型输出转换为结构化数据的组件 |
| Runnable | 可运行对象 | LangChain 表达式语言 (LCEL) 中的基本单元 |
| Callback | 回调 | 在处理过程中触发的事件处理机制 |
| Tracer | 追踪器 | 用于监控和记录处理流程的工具 |
| LCEL (LangChain Expression Language) | LangChain 表达式语言 | 用于构建复杂链的声明式语言 |
| Message | 消息 | 对话中的基本单元 |
| Message History | 消息历史 | 存储对话消息序列的组件 |

## 消息类型

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| System Message | 系统消息 | 定义 AI 助手行为的指令消息 |
| Human Message | 人类消息 / 用户消息 | 用户输入的消息 |
| AI Message | AI 消息 / 助手消息 | AI 助手的回复消息 |
| Tool Message | 工具消息 | 工具执行结果的返回消息 |
| Function Message | 函数消息 | 函数调用结果的返回消息（已弃用） |

## 架构与设计模式

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Schema | 模式 / 架构 | 定义数据结构或接口的规范 |
| Base Class | 基类 | 抽象定义的父类 |
| Interface | 接口 | 定义行为规范的协议 |
| Decorator | 装饰器 | 用于修改函数或类行为的 Python 特性 |
| Middleware | 中间件 | 在请求处理流程中插入的处理层 |
| Pipeline | 管道 | 数据处理的线性流程 |
| DAG (Directed Acyclic Graph) | 有向无环图 | 用于表示链式结构的图结构 |
| Node | 节点 | 图中的处理单元 |
| Edge | 边 | 连接节点的数据流 |
| State | 状态 | 在状态机或图中维护的数据 |
| Graph | 图 | 由节点和边组成的结构 |

## 版本与状态标记

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Deprecated | 已弃用 | 不再推荐使用，未来可能删除的功能 |
| Beta | 测试版 | 处于实验阶段的功能 |
| Alpha | 内测版 | 早期开发阶段的功能 |
| Stable | 稳定版 | 已正式发布的功能 |
| Legacy | 遗留 | 旧版本保留下来的功能 |
| Obsolete | 已淘汰 | 完全不再使用的功能 |

## 开发相关

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Import | 导入 | 引入外部模块或包 |
| Module | 模块 | Python 中的代码组织单元 |
| Package | 包 | 包含多个模块的目录 |
| Namespace | 命名空间 | 避免命名冲突的作用域 |
| Type Hint | 类型提示 | Python 的类型注解 |
| Generic | 泛型 | 支持多种类型的抽象类型 |
| Async / Await | 异步 / 等待 | 异步编程关键字 |
| Coroutine | 协程 | 异步执行的函数 |
| Iterator | 迭代器 | 支持遍历的对象 |
| Generator | 生成器 | 支持惰性求值的迭代器 |
| Context Manager | 上下文管理器 | 使用 `with` 语句管理资源 |
| Exception | 异常 | 程序运行时的错误 |
| Stack Trace | 堆栈跟踪 | 错误发生时的调用链 |

## 模型相关

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Token | 词元 | 模型处理的最小文本单位 |
| Tokenizer | 分词器 | 将文本转换为词元的工具 |
| Context Window | 上下文窗口 | 模型能处理的最大词元数 |
| Temperature | 温度 | 控制模型输出随机性的参数 |
| Top-p / Nucleus Sampling | 核采样 | 一种采样策略 |
| Top-k | Top-k 采样 | 限制候选词数量的采样策略 |
| Stop Sequence | 停止序列 | 模型生成停止的标记 |
| Max Tokens | 最大词元数 | 模型生成的最大长度限制 |
| Streaming | 流式传输 | 逐字返回模型输出的方式 |
| Function Calling | 函数调用 | 模型调用外部函数的能力 |
| JSON Mode | JSON 模式 | 强制模型输出 JSON 格式的模式 |
| System Prompt | 系统提示词 | 定义模型行为的指令 |
| Few-shot | 少样本 | 提供少量示例的学习方式 |
| Zero-shot | 零样本 | 不提供示例的学习方式 |

## 向量与检索

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Vector | 向量 | 高维空间中的数值表示 |
| Similarity | 相似度 | 向量之间的接近程度 |
| Cosine Similarity | 余弦相似度 | 常用的向量相似度度量 |
| Euclidean Distance | 欧几里得距离 | 向量间的直线距离 |
| Dot Product | 点积 | 向量的内积运算 |
| Index | 索引 | 加速向量检索的数据结构 |
| Approximate Search | 近似搜索 | 牺牲精度换取速度的搜索 |
| Exact Search | 精确搜索 | 返回最准确结果的搜索 |
| Metadata | 元数据 | 与文档关联的附加信息 |
| Chunk | 块 / 片段 | 文档分割后的小段 |
| Chunk Size | 块大小 | 每个片段的最大长度 |
| Chunk Overlap | 块重叠 | 相邻片段的重叠长度 |
| Reranking | 重排序 | 对初步检索结果再次排序 |
| Hybrid Search | 混合搜索 | 结合多种搜索策略的方法 |

## 智能体相关

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Action | 动作 | 智能体执行的操作 |
| Observation | 观察 | 智能体从环境获取的信息 |
| Thought | 思考 | 智能体的推理过程 |
| Planning | 规划 | 智能体制定行动策略的过程 |
| ReAct | 推理与行动 | 结合推理和行动的智能体框架 |
| Tool Selection | 工具选择 | 智能体选择合适的工具 |
| Tool Execution | 工具执行 | 调用工具并获取结果 |
| Multi-agent | 多智能体 | 多个智能体协作的系统 |
| Agent Executor | 智能体执行器 | 运行智能体的引擎 |
| Max Iterations | 最大迭代次数 | 智能体运行的最大轮数 |
| Handle Parsing Errors | 处理解析错误 | 智能体解析失败时的处理 |

## 数据加载与处理

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Data Loader | 数据加载器 | 从各种来源加载数据的组件 |
| Document Loader | 文档加载器 | 专门加载文档的加载器 |
| Text Splitter | 文本分割器 | 将长文本分割成小块 |
| Character Splitter | 字符分割器 | 按字符数分割文本 |
| Recursive Splitter | 递归分割器 | 递归地按分隔符分割 |
| Token Splitter | 词元分割器 | 按词元数分割文本 |
| Parser | 解析器 | 将原始数据转换为结构化数据 |
| Transformer | 转换器 | 对数据进行变换处理 |

## 输出处理

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Structured Output | 结构化输出 | 格式化的数据输出 |
| Pydantic Model | Pydantic 模型 | 用于数据验证的模型类 |
| JSON Parser | JSON 解析器 | 解析 JSON 格式的输出 |
| XML Parser | XML 解析器 | 解析 XML 格式的输出 |
| YAML Parser | YAML 解析器 | 解析 YAML 格式的输出 |
| CSV Parser | CSV 解析器 | 解析 CSV 格式的输出 |
| Regex Parser | 正则解析器 | 使用正则表达式解析 |
| List Parser | 列表解析器 | 解析列表格式的输出 |
| Datetime Parser | 日期时间解析器 | 解析日期时间格式 |
| Enum | 枚举 | 有限取值集合的类型 |

## 缓存与存储

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Cache | 缓存 | 临时存储以提高性能 |
| In-Memory Cache | 内存缓存 | 存储在内存中的缓存 |
| Redis Cache | Redis 缓存 | 使用 Redis 的缓存 |
| SQLite Cache | SQLite 缓存 | 使用 SQLite 的缓存 |
| Semantic Cache | 语义缓存 | 基于语义相似度的缓存 |
| Store | 存储 | 持久化数据的存储 |
| Key-Value Store | 键值存储 | 以键值对形式存储数据 |
| Blob Store | 二进制存储 | 存储二进制大对象 |

## 回调与监控

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Callback Handler | 回调处理器 | 处理回调事件的类 |
| Callback Manager | 回调管理器 | 管理多个回调处理器的类 |
| Event | 事件 | 回调系统触发的动作 |
| Run | 运行 | 一次完整的执行过程 |
| Run ID | 运行 ID | 唯一标识一次运行的 ID |
| Parent Run ID | 父运行 ID | 标识父级运行的 ID |
| Tags | 标签 | 用于分类和过滤的标记 |
| Metadata | 元数据 | 附加的运行信息 |
| Streaming Callback | 流式回调 | 处理流式输出的回调 |

## 合作伙伴集成

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Partner Package | 合作伙伴包 | 第三方服务集成包 |
| Integration | 集成 | 与外部服务的连接 |
| Provider | 提供商 | 服务提供方 |
| API Key | API 密钥 | 访问 API 的凭证 |
| Endpoint | 端点 | API 服务的访问地址 |
| Rate Limit | 速率限制 | API 调用的频率限制 |
| Token Limit | 词元限制 | API 的用量限制 |

## 测试相关

| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Unit Test | 单元测试 | 针对单个功能的测试 |
| Integration Test | 集成测试 | 测试多个组件的协作 |
| Mock | 模拟 | 模拟外部依赖的行为 |
| Stub | 存根 | 提供预设响应的测试替身 |
| Fixture | 测试夹具 | 测试前的准备数据 |
| Conftest | 配置测试 | pytest 的配置文件 |
| Parametrize | 参数化 | 使用多组参数运行测试 |

---

## 术语使用规范

1. **优先使用中文翻译**：在注释和文档中，优先使用本表中的中文翻译
2. **保留英文原名**：首次出现时，建议以"中文翻译（英文原名）"的形式标注
3. **保持上下文一致**：在同一篇文档中，对同一术语的翻译保持一致
4. **特殊情况**：对于业界广泛使用的英文术语（如 API、JSON、URL 等），可保留英文

## 更新记录

- **2026-02-01**: 大幅扩充术语表，新增架构、模型、向量检索、智能体等分类
- **2026-01-29**: 初始化术语表，包含核心概念和基础术语

---

> **提示**：如发现术语翻译不当或需要新增术语，请提交 Issue 或 PR 进行讨论。
