# libs\langchain\langchain_classic\callbacks\human.py

`human.py` 提供了需要**人工介入**的回调处理器，主要用于工具调用的审批流。

## 核心类

### `HumanApprovalCallbackHandler`
该处理器在执行特定的 Tool 之前会暂停，并请求用户在终端确认。

### `AsyncHumanApprovalCallbackHandler`
异步版本的审批处理器。

### `HumanRejectedException`
当用户拒绝执行某个操作时抛出的异常。

## 主要功能

- **安全红线**: 对于具有破坏性（如删除数据库记录、发送邮件）的工具调用，强制要求人工审核。
- **动态决定**: 支持通过 `should_check` 函数动态判断哪些输入需要审批。

## 使用示例

```python
from langchain_classic.callbacks import HumanApprovalCallbackHandler

def need_approval(input_dict: dict) -> bool:
    # 只有当输入包含 "delete" 时才需要审批
    return "delete" in input_dict.get("input", "")

handler = HumanApprovalCallbackHandler(
    should_check=need_approval,
    approve_all_tools=False
)

# 代理在调用危险工具前会询问：Do you approve of the following input? (y/n)
agent_executor.invoke({"input": "delete all users"}, callbacks=[handler])
```

## 注意事项

- **交互环境**: 此处理器主要用于本地交互式终端。在 Web 服务或后台任务中，需要自定义逻辑（如通过 API 发送通知并等待回调）。
- **阻塞性**: 它会阻塞当前线程/协程直到收到用户输入。
