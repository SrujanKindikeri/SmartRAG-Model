"""
=========================================================
SmartRAG Prompt Builder
=========================================================

Pipeline

Conversation History
        │
        ▼
Retrieved Context
        │
        ▼
User Question
        │
        ▼
System Instructions
        │
        ▼
Final Prompt

=========================================================
"""

from config import (
    MEMORY_CONTEXT_LIMIT,
    NO_CONTEXT_RESPONSE
)


class PromptBuilder:

    def __init__(self):

        pass

    # =====================================================
    # Build Conversation History
    # =====================================================

    def build_history(
        self,
        history
    ):

        if not history:

            return ""

        history = history[-MEMORY_CONTEXT_LIMIT:]

        lines = []

        for item in history:

            user = item.get("question", "").strip()

            assistant = item.get("answer", "").strip()

            if user:

                lines.append(f"User: {user}")

            if assistant:

                lines.append(f"Assistant: {assistant}")

        return "\n".join(lines)

    # =====================================================
    # Build Context
    # =====================================================

    def build_context(
        self,
        context
    ):

        if not context:

            return ""

        return context.strip()

    # =====================================================
    # Build System Prompt
    # =====================================================

    def system_prompt(self):

        return """
You are SmartRAG, an intelligent AI assistant.

Rules:

1. Answer ONLY from the provided context.
2. Never invent facts.
3. If the answer is missing from the context, say:

"I couldn't find enough information in the provided documents."

4. Keep answers clear and well structured.
5. Mention important details when available.
6. Never mention internal implementation details.
""".strip()

    # =====================================================
    # Build Prompt
    # =====================================================

    def build_prompt(
        self,
        question,
        context,
        history=None
    ):

        history_text = self.build_history(history)

        context_text = self.build_context(context)

        prompt = f"""
{self.system_prompt()}

================ Conversation ================

{history_text}

================ Context =====================

{context_text}

================ Question ====================

{question}

================ Answer ======================

"""

        return prompt.strip()
    # =====================================================
    # Validate Prompt
    # =====================================================

    def validate(
        self,
        prompt: str
    ):

        if not prompt.strip():

            return False

        if "Question" not in prompt:

            return False

        if "Answer" not in prompt:

            return False

        return True

    # =====================================================
    # Build Empty Prompt
    # =====================================================

    def build_no_context_prompt(
        self,
        question,
        history=None
    ):

        history_text = self.build_history(history)

        prompt = f"""
{self.system_prompt()}

================ Conversation ================

{history_text}

================ Context =====================

No relevant context was retrieved.

================ Question ====================

{question}

================ Answer ======================

{NO_CONTEXT_RESPONSE}
"""

        return prompt.strip()

    # =====================================================
    # Prompt Statistics
    # =====================================================

    def statistics(
        self,
        prompt
    ):

        return {

            "characters": len(prompt),

            "words": len(prompt.split()),

            "lines": len(prompt.splitlines())

        }

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(
        self,
        prompt
    ):

        stats = self.statistics(prompt)

        print("\n" + "=" * 60)
        print("Prompt Statistics")
        print("=" * 60)

        print(f"Characters : {stats['characters']}")
        print(f"Words      : {stats['words']}")
        print(f"Lines      : {stats['lines']}")

        print("=" * 60)

    # =====================================================
    # Preview Prompt
    # =====================================================

    def preview(
        self,
        prompt,
        max_chars=1200
    ):

        print("\n" + "=" * 70)
        print("Prompt Preview")
        print("=" * 70)

        if len(prompt) <= max_chars:

            print(prompt)

        else:

            print(prompt[:max_chars])

            print("\n... (Prompt Truncated) ...")

        print("=" * 70)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        return {

            "status": "healthy",

            "memory_limit": MEMORY_CONTEXT_LIMIT,

            "fallback_enabled": bool(NO_CONTEXT_RESPONSE)

        }

    # =====================================================
    # Print Health
    # =====================================================

    def print_health(self):

        health = self.health()

        print("\n" + "=" * 60)
        print("Prompt Builder Health")
        print("=" * 60)

        for key, value in health.items():

            print(f"{key.capitalize():20}: {value}")

        print("=" * 60)
# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    builder = PromptBuilder()

    history = [

        {

            "question": "Hello",

            "answer": "Hi! How can I help you today?"

        },

        {

            "question": "What is SmartRAG?",

            "answer": "SmartRAG is an intelligent Retrieval-Augmented Generation system."

        }

    ]

    context = """
Attendance Rules

Students must maintain at least 75% attendance.
Short attendance may lead to detention.
"""

    prompt = builder.build_prompt(

        question="What is the minimum attendance required?",

        context=context,

        history=history

    )

    builder.preview(prompt)

    builder.print_statistics(prompt)

    builder.print_health()

    print("\nPrompt Valid :", builder.validate(prompt))