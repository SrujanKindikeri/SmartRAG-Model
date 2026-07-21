"""
=========================================================
SmartRAG LLM Interface
=========================================================

Pipeline

Prompt
   │
   ▼
Ollama
   │
   ▼
Qwen3:8B
   │
   ▼
Response

=========================================================
"""

import ollama

from config import (
    OLLAMA_MODEL,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
    ENABLE_STREAMING
)


class LLM:

    def __init__(self):

        self.model = OLLAMA_MODEL

        print(f"\nLoading LLM : {self.model}")

    # =====================================================
    # Generate Response
    # =====================================================

    def generate(
        self,
        prompt,
        stream=ENABLE_STREAMING
    ):

        try:

            if stream:

                response = ollama.chat(

                    model=self.model,

                    messages=[

                        {
                            "role": "user",
                            "content": prompt
                        }

                    ],

                    stream=True,

                    options={

                        "temperature": TEMPERATURE,

                        "top_p": TOP_P,

                        "num_predict": MAX_TOKENS

                    }

                )

                answer = ""

                for chunk in response:

                    text = chunk["message"]["content"]

                    print(text, end="", flush=True)

                    answer += text

                print()

                return answer

            else:

                response = ollama.chat(

                    model=self.model,

                    messages=[

                        {
                            "role": "user",
                            "content": prompt
                        }

                    ],

                    options={

                        "temperature": TEMPERATURE,

                        "top_p": TOP_P,

                        "num_predict": MAX_TOKENS

                    }

                )

                return response["message"]["content"]

        except Exception as e:

            return f"LLM Error : {e}"

    # =====================================================
    # Ask
    # =====================================================

    def ask(
        self,
        prompt
    ):

        return self.generate(prompt)
    # =====================================================
    # Model Information
    # =====================================================

    def model_info(self):

        return {

            "model": self.model,

            "temperature": TEMPERATURE,

            "top_p": TOP_P,

            "max_tokens": MAX_TOKENS,

            "streaming": ENABLE_STREAMING

        }

    # =====================================================
    # Print Model Information
    # =====================================================

    def print_model_info(self):

        info = self.model_info()

        print("\n" + "=" * 60)
        print("LLM Configuration")
        print("=" * 60)

        print(f"Model        : {info['model']}")
        print(f"Temperature  : {info['temperature']}")
        print(f"Top P        : {info['top_p']}")
        print(f"Max Tokens   : {info['max_tokens']}")
        print(f"Streaming    : {info['streaming']}")

        print("=" * 60)

    # =====================================================
    # Connection Test
    # =====================================================

    def test_connection(self):

        try:

            response = ollama.chat(

                model=self.model,

                messages=[

                    {
                        "role": "user",
                        "content": "Reply with only the word: OK"
                    }

                ],

                options={

                    "temperature": 0,

                    "num_predict": 5

                }

            )

            answer = response["message"]["content"].strip()

            return answer.upper().startswith("OK")

        except Exception:

            return False

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        return {

            "status": "healthy" if self.test_connection() else "offline",

            "model": self.model,

            "connected": self.test_connection()

        }

    # =====================================================
    # Print Health
    # =====================================================

    def print_health(self):

        health = self.health()

        print("\n" + "=" * 60)
        print("LLM Health")
        print("=" * 60)

        for key, value in health.items():

            print(f"{key.capitalize():15}: {value}")

        print("=" * 60)

    # =====================================================
    # Generate Without Streaming
    # =====================================================

    def generate_text(
        self,
        prompt
    ):

        return self.generate(

            prompt,

            stream=False

        )

    # =====================================================
    # Generate With Streaming
    # =====================================================

    def stream(
        self,
        prompt
    ):

        return self.generate(

            prompt,

            stream=True

        )
# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    llm = LLM()

    llm.print_model_info()

    llm.print_health()

    while True:

        print()

        prompt = input("Prompt > ").strip()

        if prompt.lower() in ["exit", "quit"]:

            break

        print("\nResponse\n")

        answer = llm.generate(prompt)

        print("\n")
