from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import HTTPException , status
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
import os 
from src.app.Models.enums.ProcessingEnum import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):
    def __init__(self , project_id : str):
        super().__init__()

        self.project_id = project_id
        self.project_dir_path = ProjectController().get_project_path(project_id)

    
    def get_file_extension(self , file_id : str):
        return os.path.splitext(file_id)[-1]


    def get_document_loader(self,file_id : str):
        file_extension = self.get_file_extension(file_id)
        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(os.path.join(self.project_dir_path, file_id) , encoding="utf-8")
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(os.path.join(self.project_dir_path, file_id))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported file type: {file_extension}")

    

    def get_file_content(self , file_id : str):
        loader = self.get_document_loader(file_id)
        return loader.load()
    
    def process_document(self,file_content : list  , file_id : str ,
                    chunk_size : int = 100 , chunk_overlap : int = 20):

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap ,
                    length_function=len)

        file_content_text = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(file_content_text , 
                    metadatas=file_content_metadata)

        return chunks
        
