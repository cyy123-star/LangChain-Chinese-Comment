# SequentialChain

`SequentialChain` 用于将多个链（Chain）按照特定顺序连接起来。前一个链的输出可以作为后一个链的输入，从而形成一个复杂的处理流水线。

## 核心类别

### 1. `SimpleSequentialChain`
最简单的形式。每个步骤只接收一个输入并产生一个输出。
- **限制**: 只能传递单个变量。

### 2. `SequentialChain`
更通用的形式。支持多个输入和输出变量。
- **灵活性**: 可以指定哪些变量传递给下一步，以及最终返回哪些变量。

## 核心参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `chains` | `List[Chain]` | 构成流水线的链列表。 |
| `input_variables` | `List[str]` | 整个流水线期望的初始输入键名。 |
| `output_variables` | `List[str]` | 整个流水线最终返回的输出键名。 |
| `return_all` | `bool` | 是否返回中间步骤产生的所有变量，默认为 `False`。 |

## 校验逻辑

`SequentialChain` 在初始化时会进行严格的校验：
- **输入匹配**: 确保每个子链所需的 `input_keys` 都能在初始输入或之前步骤的输出中找到。
- **键名冲突**: 检查内存变量（Memory）是否与输入变量重名。
- **输出确认**: 确保 `output_variables` 中声明的所有变量最终都能被生成。

```python
# 校验逻辑 (简化)
for chain in chains:
    # 检查当前链需要的输入是否已知
    missing_vars = set(chain.input_keys).difference(known_variables)
    if missing_vars:
        raise ValueError(f"Missing required input keys: {missing_vars}")
    
    # 将当前链的输出加入已知变量池，供下一步使用
    known_variables |= set(chain.output_keys)
```

## 执行逻辑

`SequentialChain` 会按顺序遍历 `chains`，维护一个包含所有中间结果的 `known_values` 字典。

```python
# 核心执行循环 (简化)
known_values = inputs.copy()
for chain in self.chains:
    outputs = chain(known_values)
    known_values.update(outputs)
return {k: known_values[k] for k in self.output_variables}
```

## 迁移方案 (LCEL)

在 LCEL 中，顺序执行通过管道操作符 `|` 实现，这比 `SequentialChain` 更直观且支持流式输出。

```python
# LCEL 等价实现
chain = (
    {"variable_a": step_1_prompt | model | parser} # 步骤 1
    | {"variable_b": step_2_prompt | model | parser, "original_a": itemgetter("variable_a")} # 步骤 2
)
```
