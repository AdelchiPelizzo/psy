"""
TokenManager.py

Utility for counting OpenAI tokens using tiktoken.
Supports:
- Plain text token counting
- Chat-style message token counting
- Token budgeting helpers

Requires:
    pip install tiktoken
"""

from typing import List, Dict, Optional
import tiktoken


class TokenManager:
    def __init__(self, model: str = "gpt-4.1"):
        """
        Initialize the TokenManager with a target model.
        """
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)

    # -------------------------
    # Basic text token counting
    # -------------------------
    def count_text_tokens(self, text: str) -> int:
        """
        Count tokens for plain text.
        """
        if not text:
            return 0
        return len(self.encoding.encode(text))

    # -------------------------
    # Chat message token counting
    # -------------------------
    def count_chat_tokens(
        self,
        messages: List[Dict[str, str]],
        include_assistant_preamble: bool = True
    ) -> int:
        """
        Count tokens for chat-style messages.

        messages format:
        [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]

        Token rules are approximate but accurate enough for pricing & limits.
        """

        tokens = 0

        for message in messages:
            # Per-message overhead (role + formatting)
            tokens += 4

            for key, value in message.items():
                if value:
                    tokens += len(self.encoding.encode(value))

                # Role field sometimes adds a token
                if key == "role":
                    tokens += 1

        # Assistant reply priming
        if include_assistant_preamble:
            tokens += 2

        return tokens

    # -------------------------
    # Token budgeting helpers
    # -------------------------
    def remaining_tokens(
        self,
        messages: List[Dict[str, str]],
        max_context_tokens: int
    ) -> int:
        """
        Return how many tokens remain in the context window.
        """
        used = self.count_chat_tokens(messages)
        return max(max_context_tokens - used, 0)

    def can_fit(
        self,
        messages: List[Dict[str, str]],
        max_context_tokens: int,
        expected_output_tokens: int
    ) -> bool:
        """
        Check if messages + expected output fit in the context window.
        """
        used = self.count_chat_tokens(messages)
        return used + expected_output_tokens <= max_context_tokens

    # -------------------------
    # Debug helpers
    # -------------------------
    def debug_tokens(self, text: str) -> None:
        """
        Print token breakdown for debugging.
        """
        tokens = self.encoding.encode(text)
        print("Token count:", len(tokens))
        print("Token IDs:", tokens)


# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    tm = TokenManager(model="gpt-4.1")

    text = "Hello world! 👋"
    print("Text tokens:", tm.count_text_tokens(text))

    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain what tokens are"}
    ]

    print("Chat tokens:", tm.count_chat_tokens(messages))
    print("Remaining tokens (8k ctx):", tm.remaining_tokens(messages, 8192))
