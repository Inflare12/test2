import numpy as np


class FaceLearner:

    def __init__(self, memory):
        self.memory = memory

    def learn(self, name, embedding):

        embedding = embedding / np.linalg.norm(embedding)

        self.memory.people[name] = embedding.tolist()

        self.memory.save()

        print(name, "saved.")