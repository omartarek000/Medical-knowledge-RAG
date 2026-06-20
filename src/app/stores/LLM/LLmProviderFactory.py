from src.app.stores.LLM.LLmEnum import LLMEnum
from src.app.stores.LLM.providers.OPENAIprovider import OPENAIprovider
from src.app.helpers.config import get_settings

class LLmProviderFactory:
    def __init__(self):
        self.config = get_settings()

    
    def create_llm_provider(self , provider :str):
        if provider == LLMEnum.OPENAI.value:
            
            return OPENAIprovider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_URL,
                default_max_input_tokens=self.config.INPUT_DEFAULT_MAX_CHAR,
                default_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMP,
            )
        else:
            raise ValueError(f"Invalid provider: {provider}")
        


        