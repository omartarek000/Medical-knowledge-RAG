from ..LLmEnum import OpenAIModelEnum
from ..LLmInterface import LLMInterface
from openai import OpenAI
import logging
from ..LLmExceptions import LLMgenerationException , LLMembeddingException , LLMProviderNotFoundException , LLMProviderNotInitializedException


class OPENAIprovider(LLMInterface):
    def __init__(self , api_key:str , api_url:str = None  ,
                     default_max_input_tokens: int = 1000 ,
                     default_max_output_tokens: int = 1000,
                     default_temperature: float = 0.7,
                     ):

        self.api_key = api_key
        self.api_url = api_url
        self.default_max_input_tokens = default_max_input_tokens
        self.default_max_output_tokens = default_max_output_tokens
        self.default_temperature = default_temperature
    
        self.generation_model = None
        self.embedding_model = None
        self.embedding_size = None


        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url
        )
        

        self.logger = logging.getLogger(__name__)



    def process_text(self , text:str) -> str:
        return text[:self.default_max_input_tokens].strip()


    def set_generation_model(self, model_id:str) -> None:
        self.generation_model = model_id


    def set_embedding_model(self, model_id:str , embeding_size:int ) -> None:
        self.embedding_model = model_id
        self.embedding_size = embeding_size


    def generate_response(self, prompt: str , chat_history:list[dict] ,max_tokens :int , temperature:float ) -> str:

        if not self.client:
            self.logger.error("OpenAI client not initialized")
            raise LLMProviderNotInitializedException("OpenAI client not initialized")

        if not self.generation_model:
            self.logger.error("OpenAI generation model not set")
            raise LLMgenerationException("OpenAI generation model not set")
        
        max_tokens = max_tokens if max_tokens else self.default_max_output_tokens
        temperature = temperature if temperature else self.default_temperature
        

        chat_history.append(
            {
                "role": OpenAIModelEnum.USER.value,
                "content": prompt
            }
        )

        response = self.client.chat.completions.create(
            model=self.generation_model,
            messages=chat_history,
            max_tokens=max_tokens,
            temperature=temperature
        )

        if not response or not response.choices or not response.choices[0].message:
            self.logger.error("OpenAI response is empty")
            raise LLMgenerationException("OpenAI response is empty")
        
        return response.choices[0].message.content

        

    def embed_text(self, text:str , document_type:str = None) -> list[float]:
        if not self.client:
            self.logger.error("OpenAI client not initialized")
            raise Exception("OpenAI client not initialized")

        if not self.embedding_model:
            self.logger.error("OpenAI embedding model not set")
            raise Exception("OpenAI embedding model not set")


        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )

        if not response or not response.data:
            self.logger.error("OpenAI embedding response is empty")
            raise Exception("OpenAI embedding response is empty")
        
        return response.data[0].embedding

        
        
    def construct_prompt(self , prompt:str , role:str ) -> dict:
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
        