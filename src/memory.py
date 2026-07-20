import json
import os

from config import MAX_HISTORY


class ConversationMemory:

    def __init__(self):

        self.file = "history.json"

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:
                json.dump([], f)

    # -----------------------------------------

    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)

    # -----------------------------------------

    def save(self, history):

        with open(self.file, "w") as f:
            json.dump(history, f, indent=4)

    # -----------------------------------------

    def add(self, question, answer):

        history = self.load()

        history.append({

            "user": question,

            "assistant": answer

        })

        history = history[-MAX_HISTORY:]

        self.save(history)

    # -----------------------------------------

    def get_context(self):

        history = self.load()

        if len(history) == 0:
            return ""

        conversation = ""

        for chat in history:

            conversation += f"""

User:
{chat['user']}

Assistant:
{chat['assistant']}

"""

        return conversation

    # -----------------------------------------

    def clear(self):

        self.save([])