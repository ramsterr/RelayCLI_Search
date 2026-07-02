import numpy as np
from sentence_transformers import SentenceTransformer

EMBEDDING_DIM = 384
BATCH_SIZE = 32


class CodeEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        if not texts:
            #if string empty then make a 2d array od 0,384
            return np.empty((0, EMBEDDING_DIM), dtype=np.float32)
        return self.model.encode(
            texts,
            batch_size=BATCH_SIZE,
            normalize_embeddings=True,
            convert_to_numpy=True
            #normalising because it shrinks every vector to length 1
            # cosine similarity is simple dot product
            # and its the same answer without normalising but cheaper
        )
    def embed_query(self, query):
            return self.model.encode(
                [query],
                normalize_embeddings=True,  
            )[0]
            


def build_text_representation(entry):
    kind = entry["kind"]
    name = entry["name"]
    doc = entry.get("docstring", "")
    source = entry.get("source", "")[:600]  # truncate for 256-token limit
    return f"{kind}: {name}\n{doc}\n{source}"
    #the build text representation convets the parse dictonary to 
       # single string perfunction , then does embed_texts()

#Parser dict  →  build_text_representation()  →  one string  →  embed_texts()  →  vector
   
