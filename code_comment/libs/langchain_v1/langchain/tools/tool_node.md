# Tool Node 模块文档

## 功能描述
`tools` 模块中的 `tool_node` 是 LangChain v1.2.7 与 **LangGraph** 深度集成的体现。它主要提供了 `ToolNode` 类，用于在有状态的图（StateGraph）中自动执行工具调用。

## 核心组件

### `ToolNode`
`ToolNode` 是一个预构建的图节点，它可以接收包含 `tool_calls` 的消息，自动调用相应的工具，并将结果返回给图的状态。

## 核心功能
- **自动执行**: 自动解析模型输出中的工具调用请求并执行。
- **状态注入**: 支持 `InjectedState` 和 `InjectedStore`，允许工具访问图的当前状态或跨运行的存储。
- **错误处理**: 内置了对工具执行异常的处理逻辑。
- **向后兼容**: 该模块作为 `langgraph.prebuilt.tool_node` 的导出接口，确保了在 LangChain 生态内的统一导入路径。

## 使用示例

### 在 LangGraph 中使用 ToolNode
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_v1.langchain.tools import ToolNode
from langgraph.graph import StateGraph, END

@tool
def get_weather(city: str):
    """获取指定城市的当前天气。"""
    return f"{city} 的天气晴朗，25度。"

tools = [get_weather]
model = ChatOpenAI().bind_tools(tools)

# 创建 ToolNode
tool_node = ToolNode(tools)

# 构建图
workflow = StateGraph(dict)
workflow.add_node("agent", lambda state: {"messages": [model.invoke(state["messages"])]})
workflow.add_node("tools", tool_node)

# 设置连线逻辑...
```

## 注意事项
- **绑定工具**: 在使用 `ToolNode` 之前，模型必须先通过 `.bind_tools()` 方法绑定相同的工具列表。
- **消息协议**: `ToolNode` 期望输入状态中包含 `AIMessage` 且带有有效的 `tool_calls` 字段。
- **LangGraph 依赖**: 虽然该模块位于 `langchain_v1` 下，但其核心逻辑依赖于 `langgraph` 包，请确保已安装 `langgraph>=1.0.7`。
