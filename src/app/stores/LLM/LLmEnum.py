from enum import Enum

class LLMEnum(Enum):
    OPENAI = "openai"
    GROK = "grok"
    QWEN = "qwen"
    GEMINI = "gemini"
    COHERE = "cohere"


class OpenAIModelEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"