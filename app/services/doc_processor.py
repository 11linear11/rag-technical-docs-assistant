
from app.core.config import settings
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import DirectoryLoader, TextLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocProcessor:
    def __init__(self):
        self.docs_dir = settings.docs_dir
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
    
    def loader_docs(self):
        loader = DirectoryLoader(self.docs_dir, glob="**/*.md", loader_cls=TextLoader,loader_kwargs={"encoding":"utf-8"})
        return loader.load()

    def process_docs(self):
        docs = self.loader_docs()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        return text_splitter.split_documents(docs)


