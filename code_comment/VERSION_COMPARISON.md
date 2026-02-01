# LangChain 架构演进对比：Classic vs v1

在 LangChain 框架的发展历程中，`libs/langchain`（Classic）与 `libs/langchain_v1`（v1）代表了两种完全不同的设计哲学。理解这两者的区别对于开发者选择合适的技术栈至关重要。

---

## **1. 核心架构对比**

### **Classic 架构 (`libs/langchain`)：基于链 (Chains)**
Classic 架构是围绕 **LCEL (LangChain Expression Language)** 构建的，强调**线性流**。
- **设计哲学**：将复杂的任务拆解为一系列顺序执行的步骤（Chain）。
- **核心组件**：
    - `LLMChain`：基础的模型调用链。
    - `RetrievalQA`：经典的检索问答链。
    - `AgentExecutor`：预置的代理运行逻辑。
- **局限性**：难以处理复杂的循环、条件分支以及需要精细状态控制的对话场景。

### **v1 架构 (`libs/langchain_v1`)：基于图 (Graphs)**
v1 架构彻底转向了**有状态图 (Stateful Graphs)**，以 **[LangGraph](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/pyproject.toml#L16)** 为核心。
- **设计哲学**：将 AI 行为建模为一个状态机，每个动作（Node）都会更新状态，并通过边（Edge）决定下一步。
- **核心组件**：
    - **中间件 (Middleware)**：将功能解耦为独立插件（如 [pii.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/agents/middleware/pii.py)）。
    - **工厂模式 (Factory)**：通过 [factory.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/agents/factory.py) 动态构建复杂的智能体。
- **优势**：完美支持循环执行、人机协同（Human-in-the-loop）和复杂的状态管理。

---

## **2. 模块化与解耦深度**

| 维度 | LangChain Classic (`libs/langchain`) | LangChain v1 (`libs/langchain_v1`) |
| :--- | :--- | :--- |
| **代理实现** | 预置大量 Agent 类（如 [mrkl](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain/langchain_classic/agents/mrkl/)） | 采用统一的 [structured_output.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/agents/structured_output.py) 处理逻辑 |
| **功能扩展** | 通过继承基类并重写逻辑来扩展功能 | 通过 [middleware/](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/agents/middleware/) 文件夹下的独立模块横向切面扩展 |
| **工具集成** | 内置了数百个工具包（[agent_toolkits/](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain/langchain_classic/agents/agent_toolkits/)） | 核心极其精简，依赖 [tool_node.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/tools/tool_node.py) 统一调度 |
| **状态控制** | 依赖 `BaseMemory` 等传统的内存对象 | 依赖 `LangGraph` 的 Checkpointer 进行全局状态持久化 |

---

## **3. 关键代码模式差异**

### **Classic 模式：继承与重写**
在 Classic 中，如果你想自定义 Agent 的重试逻辑，通常需要继承 `AgentExecutor` 并修改其内部循环。

### **v1 模式：组合与插件 (Middleware)**
在 v1 中，重试逻辑被封装为独立的中间件：
- [model_retry.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/agents/middleware/model_retry.py)：负责模型调用层级的重试。
- [tool_retry.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/agents/middleware/tool_retry.py)：负责工具调用层级的重试。

这种设计使得开发者可以像玩乐高一样，通过配置 [types.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/agents/middleware/types.py) 中的配置项，自由组合智能体的能力。

---

## **4. 选择建议**

- **选择 Classic (`libs/langchain`) 的场景**：
    - 需要快速复用现有的海量工具集成。
    - 任务逻辑非常简单，是单向流动的（Input -> Prompt -> Model -> Output）。
    - 现有的旧项目维护。

- **选择 v1 (`libs/langchain_v1`) 的场景**：
    - 需要构建具有多轮循环、自我纠错能力的 Agent。
    - 需要对 Agent 的执行步骤进行精细化控制（如在调用特定工具前需要人工审核）。
    - 追求代码的高度模块化和可维护性。
    - 新项目启动（官方目前主推基于 LangGraph 的 v1 架构）。

---

## **5. 术语对照表**

| 术语 | Classic 含义 | v1 (LangGraph) 含义 |
| :--- | :--- | :--- |
| **Workflow** | `Chain` (线性) | `Graph` (节点+边) |
| **Step** | 组件调用 | `Node` (节点) |
| **Loop** | 难以实现或受限 | `Edge` (边) 回指到之前的节点 |
| **Memory** | 外部 `Memory` 对象 | 内部 `State` (状态) 字典 |

---

## **6. `libs` 目录全景视图**

除了上述两个核心库外，`libs/` 目录下还包含以下支撑模块，共同构成了 LangChain 的完整生态：

### **基础抽象层**
- **`core/` ([langchain-core](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/PACKAGE_OVERVIEW.md))**：
    - **职责**：整个框架的“地基”。定义了所有组件的接口（Interfaces）、基础协议（Runnables）和消息模型。
    - **特点**：严格限制依赖，不包含任何具体模型实现。

### **数据处理层**
- **`text-splitters/` ([langchain-text-splitters](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/PACKAGE_OVERVIEW.md))**：
    - **职责**：专门负责文本切分的工具包。
    - **特点**：独立于模型，支持按字符、Token、Markdown 结构等多种方式切分长文本。

### **生态集成层**
- **`partners/` ([partners](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/partners/PACKAGE_OVERVIEW.md))**：
    - **职责**：托管官方维护的第三方集成。
    - **包含**：`openai`, `anthropic`, `google-genai`, `chroma` 等独立包。每个包都有自己的依赖管理。

### **质量与支撑层**
- **`standard-tests/` ([langchain-tests](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/standard-tests/PACKAGE_OVERVIEW.md))**：
    - **职责**：提供标准化测试基类。
    - **作用**：确保任何新的 Partner 集成都能通过一套标准的接口验证。
- **`model-profiles/` ([langchain-model-profiles](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/model-profiles/PACKAGE_OVERVIEW.md))**：
    - **职责**：模型能力配置管理工具。
    - **作用**：用于更新和同步各模型商最新模型的能力特征（如上下文长度、是否支持视觉等）。
