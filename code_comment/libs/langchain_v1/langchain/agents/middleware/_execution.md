# Shell Execution Policies (Shell 执行策略)

`_execution.py` 为持久化 Shell 会话定义了一系列执行策略，用于控制 Shell 进程的启动方式和资源限制。

## 核心定位
该模块是 `ShellToolMiddleware` 等中间件的基础，通过封装不同的隔离级别（从宿主机直接运行到 Docker 容器隔离），确保代理在执行代码或命令时的安全性和可控性。

## 执行策略概览

### 1. `BaseExecutionPolicy` (抽象基类)
所有执行策略的共同契约，定义了通用的超时和输出限制参数。

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `command_timeout` | `float` | `30.0` | 单条命令执行的超时时间（秒） |
| `startup_timeout` | `float` | `30.0` | Shell 进程启动的超时时间（秒） |
| `termination_timeout` | `float` | `10.0` | 停止进程时的超时时间（秒） |
| `max_output_lines` | `int` | `100` | 允许输出的最大行数 |
| `max_output_bytes` | `int \| None` | `None` | 允许输出的最大字节数 |

### 2. `HostExecutionPolicy` (宿主机策略)
在宿主机进程中直接运行 Shell。适用于可信环境或已经处于沙箱中的容器。

- **隔离级别**: 低（无文件系统或网络隔离）。
- **资源限制**: 支持通过 Python `resource` 模块限制 CPU 时间和内存（仅限 Linux/macOS）。
- **核心参数**:
    - `cpu_time_seconds`: 限制 CPU 使用时长。
    - `memory_bytes`: 限制内存使用大小。
    - `create_process_group`: 是否为 Shell 创建新的进程组，以便超时时能终止整个进程树。

### 3. `CodexSandboxExecutionPolicy` (Codex 沙箱策略)
通过 Codex CLI (如 Anthropic 的 Seatbelt 或 Landlock) 启动 Shell。

- **隔离级别**: 中（系统调用和文件系统限制）。
- **特点**: 利用内核级特性（如 Linux 的 Landlock）提供比 `HostExecutionPolicy` 更强的细粒度权限控制。
- **核心参数**:
    - `binary`: Codex 可执行文件路径（默认为 `"codex"`）。
    - `config_overrides`: 传递给沙箱的配置项。

### 4. `DockerExecutionPolicy` (Docker 容器策略)
在专用的 Docker 容器中运行 Shell。

- **隔离级别**: 高（完整的容器隔离）。
- **安全特性**: 默认禁用网络 (`--network none`)，支持只读根文件系统 (`--read-only`)。
- **核心参数**:
    - `image`: 使用的 Docker 镜像（默认 `python:3.12-alpine3.19`）。
    - `memory_bytes`: 容器内存限制。
    - `cpus`: CPU 限制（字符串格式，如 `"0.5"`）。
    - `user`: 容器内运行的用户。
    - `read_only_rootfs`: 是否挂载只读根文件系统。

## 核心方法

### `spawn(*, workspace, env, command)`
这是所有策略必须实现的抽象方法，负责根据策略配置启动 `subprocess.Popen` 进程。

## 注意事项
1. **平台限制**: `HostExecutionPolicy` 的资源限制依赖于 POSIX 平台的 `resource` 模块，在 Windows 上不可用。
2. **Docker 安全**: 使用 `DockerExecutionPolicy` 时，应确保 Docker 守护进程已加固（如 rootless 模式）。
3. **工作目录**: `DockerExecutionPolicy` 仅在工作目录不是临时目录时才进行挂载，以减少宿主机暴露。
