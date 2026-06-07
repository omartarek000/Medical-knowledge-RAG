from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def generate_response(self, prompt: str , chat_history:list[dict] ,max_tokens :int , temperature:float ) -> str:
        pass


    @abstractmethod
    def set_generation_model(self, model_id:str) -> None:
        pass


    @abstractmethod
    def set_embedding_model(self, model_id:str , embeding_size:int) -> None:
        pass

    @abstractmethod
    def embed_text(self, text:str , document_type:str = None) -> list[float]:
        pass

    @abstractmethod
    def construct_prompt(self , prompt:str , role:str ) -> str:
        pass

    