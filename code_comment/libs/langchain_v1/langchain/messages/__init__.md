# Messages (消息类型)

`messages` 模块定义了 LangChain v1 中所有与模型交互的消息格式和内容块。它不仅包含了基础的角色消息，还引入了对多模态输入和复杂推理过程的结构化支持。

## 核心组件

### 1. 基础消息类型
- **HumanMessage**: 用户发送的消息。
- **AIMessage**: AI 生成的消息。
- **SystemMessage**: 系统指令或上下文。
- **ToolMessage**: 工具调用的返回结果。
- **RemoveMessage**: 用于在对话历史中标记删除的消息（常用于 LangGraph 的状态管理）。

### 2. 多模态内容块 (Content Blocks)
v1 版本显著增强了对多模态内容的支持，允许在 `content` 字段中使用列表形式的内容块：
- **TextContentBlock**: 纯文本内容。
- **ImageContentBlock**: 图像数据（支持 URL 或 Base64）。
- **AudioContentBlock**: 音频数据。
- **VideoContentBlock**: 视频数据。
- **FileContentBlock**: 文件数据。

### 3. 推理与工具调用
- **ReasoningContentBlock**: 记录模型的思考/推理链（Chain of Thought），与最终输出分离。
- **ToolCall**: 模型发出的工具调用请求。
- **UsageMetadata**: 消息关联的 Token 使用统计数据（输入、输出、总计）。

### 4. 实用工具
- **trim_messages**: 根据 Token 限制、消息数量或特定的起始/结束条件修剪消息历史。

## 代码参考
- [__init__.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/messages/__init__.py): 所有消息类型的导出定义。

## 使用示例

### 多模态消息构造
```python
from langchain.messages import HumanMessage, ImageContentBlock

message = HumanMessage(
    content=[
        {"type": "text", "text": "请描述这张图片的内容："},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
    ]
)
```

### 消息修剪
```python
from langchain.messages import trim_messages

# 保留最后 5 条消息，确保以 HumanMessage 开始
trimmed = trim_messages(
    messages,
    max_tokens=1000,
    strategy="last",
    token_counter=len, # 简化示例
    start_on="human"
)
```
