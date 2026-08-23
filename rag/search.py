import json
import math
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# VECTOR STORE
# ============================================================

STORE_PATH = (
    PROJECT_ROOT
    / "rag"
    / "vector_store.json"
)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        return 0.0

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


# ============================================================
# LOAD VECTOR STORE
# ============================================================

def load_vector_store():

    if not STORE_PATH.exists():

        raise FileNotFoundError(
            f"""
Vector store not found.

Expected location:
{STORE_PATH}

Create it first using:

python rag\\vector_store.py
"""
        )

    try:

        with open(
            STORE_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            documents = json.load(file)

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Invalid vector_store.json: {e}"
        )

    if not isinstance(documents, list):

        raise ValueError(
            "vector_store.json must contain a list."
        )

    return documents


# ============================================================
# SEARCH DOCUMENT
# ============================================================

def search(
    query: str,
    top_k: int = 3
):

    query = query.strip()

    if not query:
        return []


    # --------------------------------------------------------
    # Import embedding function correctly
    # --------------------------------------------------------

    from rag.embeddings import create_embedding


    # --------------------------------------------------------
    # Create embedding for user's question
    # --------------------------------------------------------

    print(
        "[RAG] Creating query embedding..."
    )

    query_embedding = create_embedding(
        query
    )


    # --------------------------------------------------------
    # Load vector database
    # --------------------------------------------------------

    documents = load_vector_store()


    if not documents:
        return []


    # --------------------------------------------------------
    # Calculate similarity
    # --------------------------------------------------------

    results = []

    for document in documents:

        text = document.get(
            "text",
            ""
        )

        embedding = document.get(
            "embedding",
            []
        )

        if not text or not embedding:
            continue


        score = cosine_similarity(
            query_embedding,
            embedding
        )


        results.append({

            "id": document.get(
                "id"
            ),

            "text": text,

            "score": score

        })


    # --------------------------------------------------------
    # Sort highest similarity first
    # --------------------------------------------------------

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    # --------------------------------------------------------
    # Return top results
    # --------------------------------------------------------

    return results[:top_k]


# ============================================================
# TEST SEARCH
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print(" ZENO RAG SEARCH TEST")
    print("=" * 50)


    question = input(
        "\nAsk something about your PDF: "
    ).strip()


    if not question:

        print(
            "\nPlease enter a question."
        )

        sys.exit(0)


    try:

        results = search(
            question,
            top_k=3
        )


        if not results:

            print(
                "\nNo relevant information found."
            )

            sys.exit(0)


        print()
        print(
            f"Found {len(results)} relevant chunks."
        )


        for index, result in enumerate(
            results,
            start=1
        ):

            print()
            print("-" * 50)

            print(
                f"Result {index}"
            )

            print(
                f"Similarity: "
                f"{result['score']:.4f}"
            )

            print()

            print(
                result["text"][:1000]
            )


    except Exception as e:

        print()
        print("=" * 50)
        print(" RAG ERROR")
        print("=" * 50)

        print()
        print(str(e))