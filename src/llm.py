import ollama
from config import OLLAMA_MODEL


class LLM:
    """
    Handles communication with the Ollama LLM.
    """

    def __init__(self):
        self.model = OLLAMA_MODEL
        print(f"Using Ollama Model: {self.model}")

    def generate(self, prompt):

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "num_predict": 512
                }
            )

            return response["message"]["content"].strip()

        except Exception as e:
            return f"LLM Error: {str(e)}"