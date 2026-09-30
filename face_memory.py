import os
import pickle
import numpy as np

DATABASE = "data/faces.pkl"


class FaceMemory:

    def __init__(self):

        os.makedirs("data", exist_ok=True)

        if os.path.exists(DATABASE):

            try:

                with open(DATABASE, "rb") as f:
                    self.db = pickle.load(f)

            except:

                self.db = {}

        else:

            self.db = {}

    def save(self):

        with open(DATABASE, "wb") as f:

            pickle.dump(self.db, f)

    def add_face(self, name, embedding):

        embedding = np.array(embedding)

        if name not in self.db:

            self.db[name] = []

        self.db[name].append(embedding)

        self.save()

    def find_person(self, embedding):

        embedding = np.array(embedding)

        best_name = "Unknown"
        best_score = -1

        for person, embeddings in self.db.items():

            for saved in embeddings:

                score = np.dot(
                    embedding,
                    saved
                ) / (
                    np.linalg.norm(embedding)
                    * np.linalg.norm(saved)
                )

                if score > best_score:

                    best_score = score
                    best_name = person

        print("Similarity:", round(best_score, 3))

        if best_score > 0.55:
            return best_name

        return "Unknown"