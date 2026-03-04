# chunking.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class Chunker:
    def __init__(self,
                 chunk_size=1500,
                 chunk_overlap=200):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",   # paragraph level
                ". ",     # sentence level
                "\n",     # line level
                " ",      # word level
                ""        # fallback char level
            ]
        )

    def chunk(self, docs):
        """
        docs = list[Document] (cleaned output)
        returns list[Document] with chunked text + preserved metadata
        """

        chunked_docs = []
        for doc in docs:
            # split preserves metadata by default
            chunks = self.splitter.split_documents([doc])

            # add chunk index to metadata (important!)
            for idx, c in enumerate(chunks):
                c.metadata = dict(c.metadata)  # clone metadata
                c.metadata["chunk_index"] = idx
                chunked_docs.append(c)

        return chunked_docs

    def preview(self, chunked_docs, limit=5):
        """See how chunked text looks."""
        for i, doc in enumerate(chunked_docs[:limit], start=1):
            print(f"\n--- CHUNK {i} ---")
            print("Page:", doc.metadata.get("page"))
            print("Chunk Index:", doc.metadata.get("chunk_index"))
            print("Preview:", doc.page_content[:300], "...")
