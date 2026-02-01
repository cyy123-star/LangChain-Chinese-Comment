# serializable.py - LangChain 可序列化基类

## 文件概述
`serializable.py` 定义了 LangChain 框架中所有可序列化对象的基类 `Serializable`。它结合了 Pydantic 的数据验证能力和自定义的序列化逻辑，为对象提供了转换为标准 JSON 格式以及从 JSON 恢复的能力。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `pydantic.BaseModel` | 提供数据模型、验证和基础序列化支持。 |
| `abc.ABC` | 定义抽象基类。 |
| `typing.TypedDict` | 定义序列化输出的固定结构。 |

---

## 核心类定义

### 序列化输出结构 (TypedDict)
- **`BaseSerialized`**: 包含版本号 (`lc`)、唯一标识符 (`id`)、名称 (`name`) 和图结构 (`graph`)。
- **`SerializedConstructor`**: 表示通过构造函数恢复的对象，包含 `kwargs`。
- **`SerializedSecret`**: 表示加密的秘密信息。
- **`SerializedNotImplemented`**: 表示不支持序列化的对象，仅保留其 `repr`。

---

### `Serializable` (类)
**功能描述**：
LangChain 对象的序列化基类。

**关键特性**：
- **选择性序列化**：即使继承自 `Serializable`，默认 `is_lc_serializable()` 也返回 `False`。必须显式重写此方法以启用序列化。
- **秘密信息处理**：通过 `lc_secrets` 属性定义哪些字段是敏感信息（如 API Key），序列化时这些字段会被替换为秘密占位符。
- **属性扩展**：`lc_attributes` 允许将模型字段之外的其他实例属性包含在序列化输出中。

**核心方法**：
| 方法名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_lc_serializable` | 类方法 | 返回该类是否启用序列化。 |
| `get_lc_namespace` | 类方法 | 获取类所属的模块路径空间。 |
| `lc_id` | 类方法 | 生成唯一的类标识符（列表形式）。 |
| `to_json` | 实例方法 | 执行实际的序列化逻辑，生成字典。 |

---

## 核心逻辑：序列化流程
1. **检查权限**：调用 `is_lc_serializable()`，若为 `False` 则调用 `to_json_not_implemented()`。
2. **提取字段**：遍历 Pydantic 模型字段。
3. **过滤默认值**：为了减小序列化体积，默认值通常会被忽略（除非是必填字段）。
4. **处理继承链**：通过遍历 MRO（方法解析顺序），合并来自父类的 `lc_secrets` 和 `lc_attributes`。
5. **脱敏处理**：根据 `lc_secrets` 的定义，将敏感字段的值替换为 `{"lc": 1, "type": "secret", "id": [...]}`。

---

## 注意事项
- **Pydantic 兼容性**：该类深度集成 Pydantic。在定义子类时，应确保字段类型是 Pydantic 支持的。
- **循环引用**：序列化逻辑目前主要针对树状结构，复杂的循环引用可能导致序列化失败。
- **版本控制**：`lc` 字段固定为 `1`，代表当前的序列化协议版本。

---

## 内部调用关系
- **被依赖项**：被 `dump.py` 中的 `dumps` 和 `dumpd` 函数直接调用。
- **反向操作**：其生成的结构由 `load.py` 中的 `Reviver` 进行解析。

---

## 元数据
- **最后更新时间**：2026-01-29
- **对应源码版本**：LangChain Core v1.2.7
