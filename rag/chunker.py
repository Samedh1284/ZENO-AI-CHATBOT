from pathlib import Path
import sys

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from document_reader import read_pdf


# ============================================================
# Create chunks
# ============================================================

def create_chunks(
    text,
    chunk_size=800,
    overlap=100
):
    """
    Split PDF text into smaller overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    print("Reading PDF...")

    text = read_pdf()

    print("Creating chunks...")

    chunks = create_chunks(text)

    print()
    print("Chunking successful!")
    print("Total chunks:", len(chunks))

    print()
    print("First chunk:")
    print("-" * 50)

    print(chunks[0] if chunks else "No chunks found.")

    print("-" * 50)