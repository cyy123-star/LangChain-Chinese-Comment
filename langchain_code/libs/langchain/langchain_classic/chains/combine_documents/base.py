"""Base interface for chains combining documents."""

from abc import ABC, abstractmethod
from typing import Any

from langchain_core._api import deprecated
from langchain_core.callbacks import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain_core.documents import Document
from langchain_core.prompts import BasePromptTemplate, PromptTemplate
from langchain_core.runnables.config import RunnableConfig
from langchain_core.utils.pydantic import create_model
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from pydantic import BaseModel, Field
from typing_extensions import override

from langchain_classic.chains.base import Chain

DEFAULT_DOCUMENT_SEPARATOR = "\n\n"
DOCUMENTS_KEY = "context"
DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template("{page_content}")


def _validate_prompt(prompt: BasePromptTemplate, document_variable_name: str) -> None:
    if document_variable_name not in prompt.input_variables:
        msg = (
            f"Prompt must accept {document_variable_name} as an input variable. "
            f"Received prompt with input variables: {prompt.input_variables}"
        )
        raise ValueError(msg)


class BaseCombineDocumentsChain(Chain, ABC):
    """用于合并文档的链的基础接口。

    此链的子类以各种方式处理文档合并。该基类存在的目的是为这些类型的链应暴露的接口增加一些一致性。
    具体来说，它们期望一个与要使用的文档相关的输入键（默认为 `input_documents`），
    并且还暴露了一个方法来计算文档生成的提示词长度（对外部调用者有用，可以用来确定将文档列表传递给此链是否安全，
    或者是否会超过上下文长度）。

    注意：此基类及相关子类已被弃用，建议使用 LCEL (LangChain Expression Language) 实现。
    """

    input_key: str = "input_documents"
    """输入键名，默认为 'input_documents'。"""
    output_key: str = "output_text"
    """输出键名，默认为 'output_text'。"""

    @override
    def get_input_schema(
        self,
        config: RunnableConfig | None = None,
    ) -> type[BaseModel]:
        """获取输入架构。"""
        return create_model(
            "CombineDocumentsInput",
            **{self.input_key: (list[Document], None)},
        )

    @override
    def get_output_schema(
        self,
        config: RunnableConfig | None = None,
    ) -> type[BaseModel]:
        """获取输出架构。"""
        return create_model(
            "CombineDocumentsOutput",
            **{self.output_key: (str, None)},
        )

    @property
    def input_keys(self) -> list[str]:
        """期望的输入键列表。"""
        return [self.input_key]

    @property
    def output_keys(self) -> list[str]:
        """返回的输出键列表。"""
        return [self.output_key]

    def prompt_length(self, docs: list[Document], **kwargs: Any) -> int | None:  # noqa: ARG002
        """返回给定文档列表生成的提示词长度。

        调用者可以使用此方法来确定传入文档列表是否会超过特定的提示词长度限制。
        这在确保提示词大小保持在特定上下文限制内时非常有用。

        参数:
            docs: 用于计算总提示词长度的文档列表。
            **kwargs: 计算提示词长度可能需要的其他参数。

        返回:
            如果该方法不依赖于提示词长度，则返回 None，否则返回以 token 为单位的提示词长度。
        """
        return None

    @abstractmethod
    def combine_docs(self, docs: list[Document], **kwargs: Any) -> tuple[str, dict]:
        """将文档合并为单个字符串。

        参数:
            docs: List[Document]，要合并的文档列表。
            **kwargs: 合并文档时使用的其他参数，通常是提示词的其他输入。

        返回:
            返回的第一个元素是合并后的字符串输出。第二个元素是包含其他要返回的键的字典。
        """

    @abstractmethod
    async def acombine_docs(
        self,
        docs: list[Document],
        **kwargs: Any,
    ) -> tuple[str, dict]:
        """异步将文档合并为单个字符串。

        参数:
            docs: List[Document]，要合并的文档列表。
            **kwargs: 合并文档时使用的其他参数，通常是提示词的其他输入。

        返回:
            返回的第一个元素是合并后的字符串输出。第二个元素是包含其他要返回的键的字典。
        """

    def _call(
        self,
        inputs: dict[str, list[Document]],
        run_manager: CallbackManagerForChainRun | None = None,
    ) -> dict[str, str]:
        """Prepare inputs, call combine docs, prepare outputs."""
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        docs = inputs[self.input_key]
        # Other keys are assumed to be needed for LLM prediction
        other_keys = {k: v for k, v in inputs.items() if k != self.input_key}
        output, extra_return_dict = self.combine_docs(
            docs,
            callbacks=_run_manager.get_child(),
            **other_keys,
        )
        extra_return_dict[self.output_key] = output
        return extra_return_dict

    async def _acall(
        self,
        inputs: dict[str, list[Document]],
        run_manager: AsyncCallbackManagerForChainRun | None = None,
    ) -> dict[str, str]:
        """Prepare inputs, call combine docs, prepare outputs."""
        _run_manager = run_manager or AsyncCallbackManagerForChainRun.get_noop_manager()
        docs = inputs[self.input_key]
        # Other keys are assumed to be needed for LLM prediction
        other_keys = {k: v for k, v in inputs.items() if k != self.input_key}
        output, extra_return_dict = await self.acombine_docs(
            docs,
            callbacks=_run_manager.get_child(),
            **other_keys,
        )
        extra_return_dict[self.output_key] = output
        return extra_return_dict


@deprecated(
    since="0.2.7",
    alternative=(
        "example in API reference with more detail: "
        "https://api.python.langchain.com/en/latest/chains/langchain.chains.combine_documents.base.AnalyzeDocumentChain.html"
    ),
    removal="1.0",
)
class AnalyzeDocumentChain(Chain):
    """先拆分文档，然后分块分析的链。

    此链由 TextSplitter 和 CombineDocumentsChain 参数化。
    它接收单个文档作为输入，将其拆分为块，然后将这些块传递给 CombineDocumentsChain。

    注意：此类已被弃用。请参阅下文以了解支持异步和流式操作模式的替代实现。

    如果底层的合并文档链只接收一个 `input_documents` 参数（例如由 `load_summarize_chain` 生成的链）：

        ```python
        split_text = lambda x: text_splitter.create_documents([x])
        summarize_document_chain = split_text | chain
        ```

    如果底层链接收额外参数（例如 `load_qa_chain`，它接收额外的 `question` 参数），我们可以使用以下方式：

        ```python
        from operator import itemgetter
        from langchain_core.runnables import RunnableLambda, RunnableParallel

        split_text = RunnableLambda(lambda x: text_splitter.create_documents([x]))
        summarize_document_chain = RunnableParallel(
            question=itemgetter("question"),
            input_documents=itemgetter("input_document") | split_text,
        ) | chain.pick("output_text")
        ```

    为了像 `AnalyzeDocumentChain` 一样额外返回输入参数，我们可以使用 `RunnablePassthrough` 包装此结构：

        ```python
        from operator import itemgetter
        from langchain_core.runnables import (
            RunnableLambda,
            RunnableParallel,
            RunnablePassthrough,
        )

        split_text = RunnableLambda(lambda x: text_splitter.create_documents([x]))
        summarize_document_chain = RunnablePassthrough.assign(
            output_text=RunnableParallel(
                question=itemgetter("question"),
                input_documents=itemgetter("input_document") | split_text,
            )
            | chain.pick("output_text")
        )
        ```
    """

    input_key: str = "input_document"
    """输入键名，默认为 'input_document'。"""
    text_splitter: TextSplitter = Field(default_factory=RecursiveCharacterTextSplitter)
    """用于拆分文档的文本拆分器。"""
    combine_docs_chain: BaseCombineDocumentsChain
    """用于合并文档块的链。"""

    @property
    def input_keys(self) -> list[str]:
        """期望的输入键。"""
        return [self.input_key]

    @property
    def output_keys(self) -> list[str]:
        """返回的输出键。"""
        return self.combine_docs_chain.output_keys

    @override
    def get_input_schema(
        self,
        config: RunnableConfig | None = None,
    ) -> type[BaseModel]:
        """获取输入架构。"""
        return create_model(
            "AnalyzeDocumentChain",
            **{self.input_key: (str, None)},
        )

    @override
    def get_output_schema(
        self,
        config: RunnableConfig | None = None,
    ) -> type[BaseModel]:
        """获取输出架构。"""
        return self.combine_docs_chain.get_output_schema(config)

    def _call(
        self,
        inputs: dict[str, str],
        run_manager: CallbackManagerForChainRun | None = None,
    ) -> dict[str, str]:
        """将文档拆分为块并传递给 CombineDocumentsChain。"""
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        document = inputs[self.input_key]
        docs = self.text_splitter.create_documents([document])
        # 假设其他键是 LLM 预测所需的
        other_keys: dict = {k: v for k, v in inputs.items() if k != self.input_key}
        other_keys[self.combine_docs_chain.input_key] = docs
        return self.combine_docs_chain(
            other_keys,
            return_only_outputs=True,
            callbacks=_run_manager.get_child(),
        )
