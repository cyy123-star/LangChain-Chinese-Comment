# LangChain Core example_selectors 模块中文文档

## 模块概述

**example_selectors** 模块是 LangChain Core 中的示例选择器模块，主要负责实现示例选择逻辑，用于在提示中包含最相关的示例。该模块提供了一套统一的接口和实现，用于根据不同的策略选择示例。

该模块对于以下场景特别重要：

- **少样本学习**：为 LLM 提供相关的示例，提高模型性能
- **提示优化**：选择最相关的示例，优化提示效果
- **上下文管理**：在有限的上下文窗口中选择最合适的示例
- **语义匹配**：基于语义相似度选择相关示例

## 核心功能

### 主要组件

| 组件名称 | 描述 | 来源文件 |
|---------|------|----------|
| `BaseExampleSelector` | 示例选择器基类，定义统一的选择接口 | base.py |
| `LengthBasedExampleSelector` | 基于长度的示例选择器 | length_based.py |
| `SemanticSimilarityExampleSelector` | 基于语义相似度的示例选择器 | semantic_similarity.py |
| `MaxMarginalRelevanceExampleSelector` | 基于最大边际相关性的示例选择器 | semantic_similarity.py |
| `sorted_values` | 排序值的工具函数 | semantic_similarity.py |

### 模块结构

```
example_selectors/
├── __init__.py               # 模块导出和动态导入机制
├── base.py                   # 基础接口定义
├── length_based.py           # 基于长度的示例选择器
└── semantic_similarity.py    # 基于语义相似度的示例选择器
```

## 详细功能说明

### 1. 基础示例选择器

#### BaseExampleSelector 类

**功能**：示例选择器基类，定义了所有示例选择器必须实现的统一接口。

**主要方法**：
- `select_examples`：选择示例（需要子类实现）
- `add_example`：添加示例

**使用场景**：
- 作为自定义示例选择器的基类
- 提供统一的示例选择接口

### 2. 基于长度的示例选择器

#### LengthBasedExampleSelector 类

**功能**：基于长度的示例选择器，根据示例的长度和可用上下文空间选择示例。

**主要属性**：
- `examples`：示例列表
- `max_length`：最大长度限制
- `example_prompt`：示例提示模板

**主要方法**：
- `select_examples`：根据长度选择示例
- `add_example`：添加示例
- `get_text_length`：获取文本长度

**使用场景**：
- 上下文窗口有限的场景
- 需要控制提示长度的场景
- 确保提示不超过模型的上下文限制

### 3. 基于语义相似度的示例选择器

#### SemanticSimilarityExampleSelector 类

**功能**：基于语义相似度的示例选择器，选择与输入最相似的示例。

**主要属性**：
- `examples`：示例列表
- `embeddings`：嵌入模型
- `k`：选择的示例数量
- `vectorstore`：向量存储

**主要方法**：
- `select_examples`：根据语义相似度选择示例
- `add_example`：添加示例

**使用场景**：
- 需要选择语义相关示例的场景
- 少样本学习场景
- 提高提示相关性的场景

#### MaxMarginalRelevanceExampleSelector 类

**功能**：基于最大边际相关性的示例选择器，平衡相关性和多样性。

**主要属性**：
- `examples`：示例列表
- `embeddings`：嵌入模型
- `k`：选择的示例数量
- `fetch_k`：候选示例数量
- `lambda_mult`：多样性权重

**主要方法**：
- `select_examples`：根据最大边际相关性选择示例
- `add_example`：添加示例

**使用场景**：
- 需要平衡相关性和多样性的场景
- 避免选择过于相似的示例
- 提高示例覆盖范围的场景

#### sorted_values 函数

**功能**：排序值的工具函数，用于排序示例。

**参数**：
- `values`：要排序的值
- `key`：排序键

**返回值**：
- 排序后的值

**使用场景**：
- 排序示例
- 辅助示例选择过程

## 动态导入机制

example_selectors 模块使用了 Python 的动态导入机制，通过 `__getattr__` 函数实现懒加载：

```python
def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result
```

这种机制的优势：
1. 减少模块导入时间
2. 避免循环依赖问题
3. 提高代码组织的灵活性

## 使用示例

### 基础示例选择器示例

```python
from langchain_core.example_selectors import BaseExampleSelector

class CustomExampleSelector(BaseExampleSelector):
    """自定义示例选择器"""
    
    def __init__(self, examples):
        """初始化示例选择器"""
        self.examples = examples
    
    def select_examples(self, input_variables):
        """选择示例"""
        # 简单的选择逻辑：返回所有示例
        # 实际实现中，这里会根据输入变量选择相关示例
        return self.examples
    
    def add_example(self, example):
        """添加示例"""
        self.examples.append(example)

# 创建示例
examples = [
    {"input": "你好", "output": "你好！有什么我可以帮助你的吗？"},
    {"input": "再见", "output": "再见！祝你有美好的一天！"},
    {"input": "谢谢", "output": "不客气！随时为你服务。"}
]

# 创建选择器
selector = CustomExampleSelector(examples)

# 选择示例
selected_examples = selector.select_examples({"input": "你好"})
print(f"选择的示例: {selected_examples}")

# 添加示例
selector.add_example({"input": "早上好", "output": "早上好！今天过得怎么样？"})
selected_examples = selector.select_examples({"input": "早上好"})
print(f"添加示例后选择的示例: {selected_examples}")
```

### 基于长度的示例选择器示例

```python
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts import PromptTemplate

# 创建示例
examples = [
    {"input": "你好", "output": "你好！有什么我可以帮助你的吗？"},
    {"input": "再见", "output": "再见！祝你有美好的一天！"},
    {"input": "谢谢", "output": "不客气！随时为你服务。"},
    {"input": "今天天气怎么样？", "output": "抱歉，我无法实时获取天气信息，但你可以查看当地的天气预报。"},
    {"input": "你能做什么？", "output": "我可以回答问题、提供信息、进行对话、帮助解决问题等。请问有什么我可以帮助你的吗？"}
]

# 创建示例提示模板
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="输入: {input}\n输出: {output}\n"
)

# 创建选择器
selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=100  # 最大长度限制
)

# 选择示例（短输入）
short_input = {"input": "你好"}
selected_examples_short = selector.select_examples(short_input)
print(f"短输入选择的示例数量: {len(selected_examples_short)}")
print(f"短输入选择的示例: {selected_examples_short}")

# 选择示例（长输入）
long_input = {"input": "你好，我想了解一下人工智能的发展历史，能给我简单介绍一下吗？"}
selected_examples_long = selector.select_examples(long_input)
print(f"\n长输入选择的示例数量: {len(selected_examples_long)}")
print(f"长输入选择的示例: {selected_examples_long}")
```

### 基于语义相似度的示例选择器示例

```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.embeddings import FakeEmbeddings

# 创建示例
examples = [
    {"input": "你好", "output": "你好！有什么我可以帮助你的吗？"},
    {"input": "再见", "output": "再见！祝你有美好的一天！"},
    {"input": "谢谢", "output": "不客气！随时为你服务。"},
    {"input": "今天天气怎么样？", "output": "抱歉，我无法实时获取天气信息，但你可以查看当地的天气预报。"},
    {"input": "你能做什么？", "output": "我可以回答问题、提供信息、进行对话、帮助解决问题等。请问有什么我可以帮助你的吗？"}
]

# 创建嵌入模型（使用假嵌入模型进行测试）
embeddings = FakeEmbeddings(size=10)

# 创建选择器
selector = SemanticSimilarityExampleSelector(
    examples=examples,
    embeddings=embeddings,
    k=2  # 选择最相似的2个示例
)

# 选择示例（与"你好"相似）
input_hello = {"input": "你好"}
selected_examples_hello = selector.select_examples(input_hello)
print(f"与'你好'相似的示例: {selected_examples_hello}")

# 选择示例（与"天气"相关）
input_weather = {"input": "今天热吗？"}
selected_examples_weather = selector.select_examples(input_weather)
print(f"\n与'今天热吗？'相似的示例: {selected_examples_weather}")

# 选择示例（与"能力"相关）
input_capability = {"input": "你会做什么？"}
selected_examples_capability = selector.select_examples(input_capability)
print(f"\n与'你会做什么？'相似的示例: {selected_examples_capability}")
```

### 基于最大边际相关性的示例选择器示例

```python
from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector
from langchain_core.embeddings import FakeEmbeddings

# 创建示例
examples = [
    {"input": "你好", "output": "你好！有什么我可以帮助你的吗？"},
    {"input": "早上好", "output": "早上好！今天过得怎么样？"},
    {"input": "晚上好", "output": "晚上好！今天过得如何？"},
    {"input": "再见", "output": "再见！祝你有美好的一天！"},
    {"input": "谢谢", "output": "不客气！随时为你服务。"},
    {"input": "感谢你", "output": "不用谢！很高兴能帮到你。"}
]

# 创建嵌入模型（使用假嵌入模型进行测试）
embeddings = FakeEmbeddings(size=10)

# 创建选择器
selector = MaxMarginalRelevanceExampleSelector(
    examples=examples,
    embeddings=embeddings,
    k=3,  # 选择3个示例
    lambda_mult=0.5  # 多样性权重
)

# 选择示例
input_greeting = {"input": "你好"}
selected_examples = selector.select_examples(input_greeting)
print(f"选择的示例数量: {len(selected_examples)}")
print("选择的示例:")
for i, example in enumerate(selected_examples):
    print(f"{i+1}. 输入: {example['input']}, 输出: {example['output']}")

# 注意：由于使用的是假嵌入模型，实际结果可能不具有真正的语义相关性
# 在实际使用中，应该使用真实的嵌入模型，如 OpenAIEmbeddings、HuggingFaceEmbeddings 等
```

## 注意事项与最佳实践

### 注意事项

1. **嵌入模型选择**：
   - 语义相似度选择器依赖于嵌入模型的质量
   - 不同的嵌入模型可能会产生不同的选择结果
   - 应根据具体任务选择合适的嵌入模型

2. **性能考虑**：
   - 语义相似度计算可能比较耗时
   - 对于大型示例集，可能需要优化向量存储
   - 考虑使用缓存机制减少重复计算

3. **示例质量**：
   - 示例的质量直接影响选择结果
   - 应确保示例具有代表性和多样性
   - 定期更新和维护示例集

4. **上下文限制**：
   - 基于长度的选择器需要准确估计文本长度
   - 不同的模型和编码方式可能有不同的长度计算方式
   - 应根据具体模型调整长度限制

5. **参数调优**：
   - 不同的选择器参数会影响选择结果
   - 应根据具体任务和数据集进行参数调优

### 最佳实践

1. **示例集管理**：
   - 构建高质量、多样化的示例集
   - 定期评估和更新示例集
   - 为不同类型的任务准备专门的示例集

2. **选择器选择**：
   - 根据具体任务选择合适的选择器
   - 上下文受限场景使用 LengthBasedExampleSelector
   - 需要语义相关性场景使用 SemanticSimilarityExampleSelector
   - 需要平衡相关性和多样性场景使用 MaxMarginalRelevanceExampleSelector

3. **参数调优**：
   - 基于长度的选择器：调整 max_length 以适应不同模型
   - 语义相似度选择器：调整 k 值以平衡相关性和多样性
   - 最大边际相关性选择器：调整 lambda_mult 以控制多样性程度

4. **性能优化**：
   - 对于大型示例集，使用高效的向量存储
   - 实现缓存机制减少重复计算
   - 考虑使用批处理提高效率

5. **评估与改进**：
   - 评估选择器的性能和效果
   - 根据评估结果调整选择策略
   - 结合多种选择策略提高效果

6. **集成使用**：
   - 与提示模板和语言模型无缝集成
   - 构建端到端的少样本学习系统
   - 监控和记录选择结果，持续改进

## 代码优化建议

1. **缓存机制**：
   - 实现示例嵌入的缓存
   - 减少重复的嵌入计算
   - 提高选择速度

2. **批处理**：
   - 实现批处理嵌入计算
   - 减少 API 调用次数
   - 提高处理效率

3. **并行处理**：
   - 对于大型示例集，使用并行处理
   - 提高嵌入计算速度

4. **动态调整**：
   - 实现基于输入的动态参数调整
   - 根据输入长度和复杂性调整选择策略

5. **评估指标**：
   - 实现选择器性能的评估指标
   - 量化选择质量
   - 支持自动调优

6. **可扩展性**：
   - 设计可扩展的选择器架构
   - 支持自定义选择策略
   - 允许组合多种选择策略

7. **监控与日志**：
   - 实现选择过程的监控
   - 记录选择结果和性能指标
   - 支持问题诊断和性能优化

## 总结

example_selectors 模块是 LangChain Core 中负责示例选择的核心组件，它提供了一套灵活、强大的机制，用于在提示中选择最相关的示例。

该模块的主要价值在于：

1. **多样化选择策略**：提供了基于长度和语义的多种选择策略
2. **灵活扩展**：支持自定义示例选择器
3. **性能优化**：通过向量存储和缓存机制提高性能
4. **质量保证**：通过合理的选择策略提高示例质量
5. **易于集成**：与 LangChain 的其他组件无缝集成

example_selectors 模块对于构建高质量的少样本学习系统、优化提示效果、提高模型性能至关重要。通过合理选择和配置示例选择器，开发者可以：

- 提高提示的相关性和有效性
- 控制提示长度，适应不同模型的上下文限制
- 平衡示例的相关性和多样性
- 构建更加智能、高效的 LLM 应用

正确使用 example_selectors 模块可以显著提升 LangChain 应用的性能和用户体验，是构建生产级 LLM 应用的重要工具。