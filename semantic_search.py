import pickle
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

with open(
    "embeddings.pkl",
    "rb"
) as f:

    data = pickle.load(f)

topics = data["topics"]
embeddings = data["embeddings"]


def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )


def search_knowledge(query):

    query_embedding = model.encode(query)

    best_score = -1
    best_topic = None

    for topic, emb in zip(
        topics,
        embeddings
    ):

        score = cosine_similarity(
            query_embedding,
            emb
        )

        if score > best_score:

            best_score = score
            best_topic = topic

    print(
        "\nSemantic Score:",
        round(best_score, 3)
    )

    if best_score < 0.35:

        return (
            "No relevant knowledge found."
        )

    return best_topic[:4000]