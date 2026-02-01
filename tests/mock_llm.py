import sys
from typing import Any, List, Optional, Union, Dict
from unittest.mock import MagicMock
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration, LLMResult, Generation
from pydantic import Field

class MockChatOpenAI(BaseChatModel):
    model_name: str = Field(default="gpt-4o-mini", alias="model")
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        content = "This is a mock response."
        if "word_count" in str(kwargs): # For OutputFixingParser test
             content = '{"ad_copy": "腕间智能，掌控未来", "word_count": 8}'
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock-chat-openai"

class MockOpenAI(BaseLLM):
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> LLMResult:
        generations = [[Generation(text="This is a mock LLM response.")]]
        return LLMResult(generations=generations)

    @property
    def _llm_type(self) -> str:
        return "mock-openai"

# Mock the entire modules if needed, or just provide these classes
sys.modules['mock_llm'] = MagicMock()
