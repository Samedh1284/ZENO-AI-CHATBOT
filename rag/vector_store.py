import json
from pathlib import Path
import sys


# ============================================================
# Project root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# Imports
# ============================================================

from document_reader import read_pdf
from chunker import create_chunks
from embeddings import create_embedding


# ============================================================
# Vector store
# ============================================================

STORE_PATH = Path(__file__).resolve().parent / "vector_store.json"


# ============================================================
# Create vector store
# ============================================================

def create_vector_store():

    print()
    print("=" * 50)
    print(" ZENO RAG - VECTOR STORE")
    print("=" * 50)

    # --------------------------------------------------------
    # Read PDF
    # --------------------------------------------------------

    print("\nReading PDF...")

    text = read_pdf()

    if not text.strip():

        raise ValueError(
            "PDF does not contain readable text."
        )

    print(
        f"PDF text loaded: {len(text)} characters"
    )


    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    print("\nCreating chunks...")

    chunks = create_chunks(text)

    if not chunks:

        raise ValueError(
            "No chunks were created from the PDF."
        )

    print(
        f"Total chunks: {len(chunks)}"
    )


    # --------------------------------------------------------
    # Create embeddings
    # --------------------------------------------------------

    vector_store = []

    print("\nCreating embeddings...")

    for index, chunk in enumerate(chunks):

        print(
            f"Embedding {index + 1}/{len(chunks)}..."
        )

        embedding = create_embedding(chunk)

        vector_store.append({

            "id": index,

            "text": chunk,

            "embedding": embedding

        })


    # --------------------------------------------------------
    # Save vector store
    # --------------------------------------------------------

    with open(
        STORE_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            vector_store,
            file
        )


    # --------------------------------------------------------
    # Done
    # --------------------------------------------------------

    print()
    print("=" * 50)
    print(" VECTOR STORE CREATED")
    print("=" * 50)

    print(
        f"\nSaved to:\n{STORE_PATH}"
    )

    print(
        f"\nStored chunks: {len(vector_store)}"
    )


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    create_vector_store()