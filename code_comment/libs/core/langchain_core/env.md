# env.py - 运行环境信息工具

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`env.py` 是 LangChain Core 提供的一个简单工具模块，用于获取当前 LangChain 运行环境的信息。它主要被用于日志记录、调试以及向外部服务（如 LangSmith）上报系统状态。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `platform` | 用于获取底层平台的详细信息（操作系统、Python 版本等）。 |
| `functools.lru_cache` | 用于缓存函数结果，避免重复执行系统调用，提高效率。 |
| `langchain_core.__version__` | 获取当前安装的 `langchain-core` 版本号。 |

## 函数详解

### 1. get_runtime_environment
- **功能描述**: 获取 LangChain 运行环境的详细信息字典。
- **参数说明**: 无参数。
- **返回值**: `dict`。包含以下键值对：
    - `library_version`: `langchain-core` 的版本号。
    - `library`: 固定为 `"langchain-core"`。
    - `platform`: 操作系统平台信息。
    - `runtime`: 固定为 `"python"`。
    - `runtime_version`: Python 解释器版本。
- **核心逻辑**:
    - 使用 `@lru_cache(maxsize=1)` 装饰器，确保在整个进程生命周期内只执行一次系统探测。
    - 调用 `platform.platform()` 和 `platform.python_version()` 获取系统信息。
- **使用示例**:
    ```python
    from langchain_core.env import get_runtime_environment

    env_info = get_runtime_environment()
    print(f"当前版本: {env_info['library_version']}")
    print(f"运行平台: {env_info['platform']}")
    ```

## 内部调用关系

该函数被 LangChain 内部的追踪系统（Tracers）和一些日志工具调用，以便在记录运行记录时附带环境元数据。

## 相关链接
- [Python platform 模块文档](https://docs.python.org/3/library/platform.html)
