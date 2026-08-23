import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# Load environment
# ============================================================

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# Create embedding
# ============================================================

def create_embedding(text: str):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    print("Creating test embedding...")

    text = "Artificial Intelligence is a branch of computer science."

    vector = create_embedding(text)

    print()
    print("Embedding created successfully!")
    print("Vector size:", len(vector))

    print()
    print("First 10 values:")

    print(vector[:10])