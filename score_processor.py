import os

from config import SCORE_FILE_PATH


class ScoreProcessor:
    # ensures that class is singleton
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ScoreProcessor, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.filepath = SCORE_FILE_PATH

    def get_score(self) -> int:
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as file:
                score: str = file.read()
                return score if score.isdigit() else 0
        return 0

    def save_score(self, score: int) -> None:
        with open(self.filepath, "w") as file:
            file.write(str(score))
        print(f"Content successfully written to {self.filepath}")
