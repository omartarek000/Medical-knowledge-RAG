from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import HTTPException , status
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path
import os
from fastapi import status , HTTPException
from src.app.Models.enums.ProcessingEnum import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):
    def __init__(self , project_id : str):
        super().__init__()

        self.project_id = project_id
        self.project_dir_path = ProjectController().get_project_path(project_id)

    
    def get_file_extension(self , file_id : str):
        return os.path.splitext(file_id)[-1]



    def get_document_loader(self, file_id: str):
        # 1. Modernize path handling and eliminate repetition
        file_path = Path(self.project_dir_path) / file_id

        # 2. Consistent HTTP error handling for missing files
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"File {file_id} not found."
            )

        file_extension = self.get_file_extension(file_id)

        # 3. Clean routing using a dictionary mapping (or Python 3.10+ match/case)
        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(str(file_path), encoding="utf-8")
        
        if file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(str(file_path))

        # 4. Fallback for unsupported types
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Unsupported file type: {file_extension}"
        )

    def get_file_content(self , file_id : str):
        loader = self.get_document_loader(file_id)
        if loader:
            return loader.load()

        else:
            return None
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
        
        
