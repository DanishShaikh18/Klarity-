# embeddings.py
import os
import ollama

# FORCE OLLAMA HOST (Windows fix)
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"


class Embedder:
    def __init__(self, model_name="nomic-embed-text"):
        self.model = model_name

    def embed_docs(self, docs):
        embedded_items = []

        for i, doc in enumerate(docs):
            text = doc.page_content

            try:
                response = ollama.embeddings(
                    model=self.model,
                    prompt=text
                )
            except Exception as e:
                print(f"❌ Error embedding chunk {i}: {e}")
                continue

            vector = response["embedding"]

            embedded_items.append({
                "id": f"doc_{i}",
                "text": text,
                "embedding": vector,
                "metadata": doc.metadata
            })

        return embedded_items

    def preview_embeddings(self, items, limit=3):
        for i, item in enumerate(items[:limit], start=1):
            print(f"\n=== EMBEDDING {i} ===")
            print("ID:", item["id"])
            print("Metadata:", item["metadata"])
            print("Vector dims:", len(item["embedding"]))
            print("Text Preview:", item["text"][:200], "...")

# NEW: embed a list of plain strings (for questions)
def embed_texts(texts):
    """
    Accepts a list of strings and returns list of vectors.
    Internally wraps them in fake LangChain Document objects
    so existing embed_docs() continues to work.
    """
    # Create lightweight stand-in objects with .page_content and .metadata
    fake_docs = [
        type("FakeDoc", (), {"page_content": t, "metadata": {}}) 
        for t in texts
    ]

    embedder = Embedder()
    embedded_items = embedder.embed_docs(fake_docs)

    # Return ONLY vectors
    return [item["embedding"] for item in embedded_items]
