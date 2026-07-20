"""
=========================================================
SmartRAG Prompt Builder
=========================================================

Builds the prompt that is sent to the LLM.

Flow:

Conversation Memory
        +
Retrieved Context
        +
Current Question
        ↓
      Final Prompt
"""

from datetime import datetime
from config import MEMORY_CONTEXT_LIMIT


class PromptBuilder:

    def __init__(self):
        pass

    # ------------------------------------------------------
    # Build Prompt
    # ------------------------------------------------------

    def build_prompt(self, question, search_results, memory):

        # ==========================================
        # Conversation Memory
        # ==========================================

        history = memory.load()

        if len(history) > MEMORY_CONTEXT_LIMIT:
            history = history[-MEMORY_CONTEXT_LIMIT:]

        conversation = ""

        for chat in history:

            conversation += f"""
User:
{chat['user']}

Assistant:
{chat['assistant']}

"""

        # ==========================================
        # Retrieved Context
        # ==========================================

        context_chunks = []

        sources = []

        seen = set()

        for result in search_results:

            text = result["text"].strip()

            filename = result["filename"]

            if text not in seen:

                seen.add(text)

                context_chunks.append(text)

            if filename not in sources:

                sources.append(filename)

        context = "\n\n".join(context_chunks)

        # ==========================================
        # Prompt
        # ==========================================

        prompt = f"""
You are SmartRAG.

Today's Date:
{datetime.now().strftime("%d-%m-%Y")}

==========================================================
ROLE
==========================================================

You are an intelligent AI assistant that answers ONLY
from the provided documents.

You are NOT allowed to use your own knowledge.

==========================================================
RULES
==========================================================

1. Answer ONLY using the retrieved context.

2. NEVER hallucinate.

3. NEVER invent facts.

4. NEVER guess.

5. If the answer is not available say exactly:

"I couldn't find the answer in the provided documents."

6. If multiple documents contain the answer,
combine them into one clear response.

7. Explain in simple language.

8. Use bullet points whenever helpful.

9. Do not mention internal chunk numbers.

10. Give ONE final answer.

==========================================================
CONVERSATION MEMORY
==========================================================

{conversation}

==========================================================
DOCUMENT CONTEXT
==========================================================

{context}

==========================================================
USER QUESTION
==========================================================

{question}

==========================================================
FINAL ANSWER
==========================================================
"""

        return prompt, sources