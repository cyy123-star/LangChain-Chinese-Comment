# libs\core\langchain_core\utils\utils.py

## 文件概述

`utils.py` 是 LangChain Core 的通用工具库，包含了一系列辅助函数，涵盖了装饰器、网络异常处理、测试模拟、动态导入、版本校验、Pydantic 模型处理以及环境变量读取等多个方面。

## 导入依赖

- `functools`, `contextlib`: 提供装饰器和上下文管理器支持。
- `importlib`, `importlib.metadata`: 用于动态模块导入和包元数据查询。
- `packaging.version`: 处理版本号比较逻辑。
- `pydantic`: 处理 Pydantic 模型相关的 Secret 类型和验证。

## 类与函数详解

### 1. xor_args (装饰器)
- **功能描述**: 验证指定的关键字参数组是否互斥且唯一。即每组参数中必须且只能有一个非 `None` 值。
- **参数说明**: `*arg_groups` 接收多个元组，每个元组代表一组互斥参数名。

### 2. raise_for_status_with_text
- **功能描述**: 增强版的请求状态检查。如果 HTTP 请求失败，会将响应体文本（通常包含错误详情）包装在 `ValueError` 中抛出。

### 3. mock_now (上下文管理器)
- **功能描述**: 用于单元测试中模拟 `datetime.datetime.now()`。在作用域内，调用 `now()` 将返回预设的固定时间。

### 4. guard_import
- **功能描述**: 动态导入模块。如果模块不存在，会抛出带有友好安装建议（`pip install ...`）的 `ImportError`。

### 5. check_package_version
- **功能描述**: 校验已安装包的版本是否符合指定的范围（如 `<`、`<=`、`>`、`>=`）。如果不符合要求，抛出 `ValueError`。

### 6. get_pydantic_field_names
- **功能描述**: 获取 Pydantic 类的所有字段名，包括定义的别名（alias）。兼容 Pydantic v1 和 v2。

### 7. _build_model_kwargs
- **功能描述**: 内部函数，用于从构造函数参数中提取并构建 `model_kwargs`。它会自动识别非标准参数并将其转移到 `model_kwargs` 中，同时发出警告。

### 8. from_env
- **功能描述**: 创建一个工厂函数，用于从环境变量中读取值。支持多键查询、默认值设置以及自定义错误消息。

## 核心逻辑

- **Pydantic 兼容性**: 许多函数（如 `get_pydantic_field_names`）通过内部探测 Pydantic 版本，确保在不同环境下的鲁棒性。
- **环境隔离**: `from_env` 允许延迟加载环境变量，这对于配置管理和跨环境部署至关重要。

## 使用示例

```python
from langchain_core.utils.utils import xor_args, from_env

# 1. 互斥参数校验
@xor_args(("api_key", "api_token"))
def connect(api_key=None, api_token=None):
    pass

# 2. 环境变量读取工厂
get_api_key = from_env("OPENAI_API_KEY", default="missing")
print(get_api_key())
```

## 注意事项

- **向后兼容**: 模块中包含一些如 `build_extra_kwargs` 的函数，标记为 `DON'T USE`，仅为了兼容旧版本，新代码不应调用。
- **Secret 处理**: `convert_to_secret_str` 用于确保敏感信息（如 API Key）被包装为 `SecretStr`，防止在日志或输出中意外泄露。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
