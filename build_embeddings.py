import re
import pickle

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

with open(
    "knowledge/health.txt",
    "r",
    encoding="utf-8"
) as f:

    text = f.read()

topics = re.split(
    r"\n\s*\d+\.\s+",
    text
)

topics = [
    t.strip()
    for t in topics
    if len(t.strip()) > 100
]

embeddings = model.encode(
    topics,
    show_progress_bar=True
)

with open(
    "embeddings.pkl",
    "wb"
) as f:

    pickle.dump(
        {
            "topics": topics,
            "embeddings": embeddings
        },
        f
    )

print("Done!")