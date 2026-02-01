# Shell Tool Middleware (持久化 Shell 工具中间件)

`shell_tool.py` 实现了一个为代理提供持久化 Shell 访问能力的中间件。与传统的单次命令执行不同，它维护一个长期的 Shell 会话，允许代理在多个步骤之间保持状态（如环境变量、工作目录、后台进程等）。

## 核心定位
它是 LangChain v1 中最强大的工具之一，允许代理像开发人员一样在交互式终端中工作。通过配合不同的 `ExecutionPolicy`，它可以在保证安全性的前提下提供极高的灵活性。

## 核心组件

### 1. `ShellSession` (持久化会话)
负责管理底层的 Shell 子进程。
- **状态保持**: 进程在多次工具调用之间持续运行。
- **输出捕获**: 使用独立的线程读取 `stdout` 和 `stderr`，并通过队列进行同步。
- **完成检测**: 通过向 `stdin` 注入唯一的标记（Marker）和 `printf $?` 来检测命令执行结束并获取退出状态码。
- **超时管理**: 如果命令执行超时，会自动重启会话以保证代理不会陷入死锁。

### 2. `ShellToolMiddleware` (中间件实现)
将 Shell 功能集成到代理系统的核心组件。
- **工具注册**: 自动向代理注册一个名为 `shell` (默认) 的工具。
- **资源生命周期**: 在代理启动时初始化会话资源（如临时工作目录），并在代理结束或被垃圾回收时自动清理。
- **输出脱敏**: 集成了 `_redaction.py` 中的规则，在将输出返回给 LLM 之前自动隐藏敏感信息（如 API Key、密码等）。

### 3. 数据结构
- **`ShellToolState`**: 扩展了 `AgentState`，用于在图中传递 `shell_session_resources`。
- **`CommandExecutionResult`**: 封装了命令执行的结果，包括 `output`、`exit_code`、`timed_out` 以及是否被截断等元数据。

## 中间件配置参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `workspace_root` | `str \| Path` | 工作目录根路径。若未指定，则创建临时的临时目录。 |
| `startup_commands` | `Sequence[str]` | 会话启动后立即执行的初始化命令。 |
| `execution_policy` | `BaseExecutionPolicy` | 执行策略（Host/Codex/Docker），控制安全隔离级别。 |
| `redaction_rules` | `List[RedactionRule]` | 用于脱敏输出的规则列表。 |
| `env` | `Mapping[str, str]` | 注入 Shell 会话的环境变量。 |

## 代理如何使用 Shell 工具
代理在生成的 `ToolCall` 中可以传递以下参数给 `shell` 工具：
- `command`: 要执行的 Shell 命令。
- `restart`: 布尔值，是否强制重启当前的 Shell 会话。

## 注意事项
1. **安全性**: 默认使用 `HostExecutionPolicy`，这意味着代理可以访问宿主机的所有文件和网络。在处理不可信输入时，强烈建议使用 `DockerExecutionPolicy`。
2. **交互性**: `ShellSession` 是非交互式的（没有 TTY）。需要交互的命令（如 `top` 或需要输入密码的命令）可能会导致会话挂起。
3. **输出限制**: 为了防止上下文溢出，输出会根据策略配置进行行数或字节数的截断。
4. **路径引用**: 建议代理使用绝对路径，或在每条命令前确认当前目录（`pwd`）。
