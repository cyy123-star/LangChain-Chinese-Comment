# [load.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/load/load.py)

该模块是 LangChain 序列化系统的反序列化核心。它负责将 JSON 字符串或字典还原为真实的 Python 对象，并提供了多层安全防护机制（如白名单和命名空间验证），防止在加载不受信任的数据时发生恶意代码执行。

## 功能概述

1. **对象复原**：通过 `load` 和 `loads` 接口，根据 JSON 中的 `id` 字段动态导入并实例化类。
2. **白名单控制**：通过 `allowed_objects` 参数严格限制允许反序列化的类。
3. **安全防御**：默认禁止在反序列化时使用 Jinja2 模板，并验证所有命名空间是否在信任列表内。
4. **版本兼容**：利用 `mapping.py` 中的映射关系，自动处理已迁移或重命名的类路径。

## 核心组件

### `Reviver` (类)

**功能描述**：
作为 `json.loads` 的 `object_hook`，它是反序列化的灵魂。每当 `json.loads` 解析出一个字典时，都会调用 `Reviver` 的 `__call__` 方法。

**初始化参数**：
| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `allowed_objects` | `Iterable` / `str` | `"core"` | 允许的类白名单。`"core"` 仅允许核心类，`"all"` 允许映射表中的所有类。 |
| `secrets_map` | `dict` | `None` | 密钥映射表。遇到 `type: "secret"` 时，从中查找真实值。 |
| `valid_namespaces` | `list` | `None` | 允许导入的额外模块命名空间。 |
| `init_validator` | `Callable` | `default` | 构造函数校验器，默认禁止 Jinja2。 |

---

### `load` / `loads`

**功能描述**：
公开的反序列化函数。`loads` 接受 JSON 字符串，`load` 接受已解析的字典。

**核心流程**：
1. **反转义**：调用 `_unescape_value` 还原被转义的用户数据。
2. **路径解析**：根据 `id` 查找映射表，确定最终的导入路径。
3. **安全检查**：验证类路径是否在 `allowed_class_paths` 中。
4. **动态导入**：使用 `importlib` 导入模块并获取类。
5. **实例化**：调用 `init_validator` 校验参数后，使用 `kwargs` 实例化对象。

## 安全模型

- **分层白名单**：默认只允许 `langchain_core` 中的对象。对于第三方集成，需要显式指定 `allowed_objects='all'`。
- **命名空间锁定**：只允许从 `langchain`、`langchain_openai` 等受信任的包中导入代码。
- **Jinja2 封禁**：由于 Jinja2 模板可以执行任意 Python 代码，反序列化系统默认拦截任何 `template_format='jinja2'` 的参数。
- **转义拆包**：攻击者无法通过在 JSON 中包含 `lc` 键来欺骗系统实例化非法类，因为所有此类数据在序列化时都已被 `__lc_escaped__` 包装，反序列化时仅作为普通字典处理。

## 使用示例

```python
from langchain_core.load import loads
from langchain_core.messages import HumanMessage

# 从 JSON 字符串恢复对象
json_data = '{"lc": 1, "type": "constructor", "id": ["langchain_core", "messages", "HumanMessage"], "kwargs": {"content": "hello"}}'
msg = loads(json_data)

assert isinstance(msg, HumanMessage)
print(msg.content)  # 输出: hello
```

## 注意事项

- **Beta 阶段**：该模块目前标记为 `beta()`，API 可能会有变动。
- **副作用警告**：反序列化会调用类的 `__init__` 方法。虽然系统有限制，但如果被允许的类在初始化时有网络或文件操作，这些操作仍会执行。

## 相关链接

- [安全模型详解 (_validation.py)](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/load/_validation.md)
- [类路径映射表 (mapping.py)](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/load/mapping.md)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7