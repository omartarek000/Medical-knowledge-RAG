
class LLMgenerationException(Exception):
    "raised when LLM generation fails"
    pass


class LLMembeddingException(Exception):
    """raised when LLM embedding fails"""
    pass

class LLMProviderNotFoundException(Exception):
    """raised when LLM provider not found"""
    pass

class LLMProviderNotInitializedException(Exception):
    """raised when LLM provider not initialized"""
    pass