
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


if __name__ == "__main__":
    doc_processor = DocProcessor()
    chunks = doc_processor.process_docs()
    print(f"Total Chunks Created: {len(chunks)}")
    if chunks:
        print("\n--- First Chunk Metadata ---")
        print(chunks[0].metadata)
        print("\n--- First Chunk Preview ---")
        print(chunks[0].page_content[:200])