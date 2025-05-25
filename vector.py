from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_csv('ttp-desc-mappings.csv', sep='\t')
embeddings = OllamaEmbeddings(model="mxbai-embed-large")


db_location = "./chrome_langchain_db"
add_docs = not os.path.exists(db_location)

if add_docs:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row['description'],
            metadata={'ttp': row['ttp']},
            id=row['ttp']
        )
        ids.append(row['ttp'])
        documents.append(document)

vector_store = Chroma(
    collection_name="ttp-desc-mapping",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_docs:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)