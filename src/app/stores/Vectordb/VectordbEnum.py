from enum import Enum

class VectordbEnum(Enum):
    QDRANT = "QDRANT"
    FAISS = "FAISS"



class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"