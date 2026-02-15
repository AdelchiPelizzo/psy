from backend.engine.models import UserFrame


class ProcessingEngine:
    def __init__(self, llm):
        """
        llm: instance of CallLLM
        """
        self.llm = llm

    def generate_question(self, user_input, strategy="evidence", depth=2, mode="neutral"):
        # Wrap string input into dict if needed
        if isinstance(user_input, str):
            user_input = {"claim": user_input}

        claim_text = user_input.get("claim", "").strip()
        if not claim_text:
            return {"observation": "[No claim provided]", "question": ""}

        system_prompt = self.llm.config.get("system_prompt_template",
            "You are an AI assistant analyzing the claim and asking one follow-up question if needed.")

        # Call LLM with the claim text
        result = self.llm.call(user_input=claim_text, system_prompt=system_prompt)

        # Ensure dict output
        if isinstance(result, dict):
            return result
        elif hasattr(result, "text"):
            return {"observation": result.text.strip(), "question": ""}
        else:
            return {"observation": str(result), "question": ""}

    # --------------------
    # Input handling
    # --------------------

    def _parse_input(self, data: dict) -> UserFrame:
        required = ["claim"]
        # required = ["topic", "claim", "emotion"]
        for key in required:
            if key not in data or not data[key]:
                raise ValueError(f"Missing field: {key}")

        return UserFrame(
            # topic=data["topic"].strip(),
            claim=data["claim"].strip(),
            # emotion=data["emotion"].lower().strip()
        )

    # --------------------
    # Strategy logic
    # --------------------

    def _choose_strategy(self, frame: UserFrame, strategy_hint: str | None):
        if strategy_hint:
            return strategy_hint

        if frame.emotion in ["fear", "anxiety"]:
            return "assumption"
        if frame.emotion in ["anger"]:
            return "evidence"

        return "clarification"

    # --------------------
    # Prompt construction
    # --------------------

    def _build_system_prompt(self):
        return (
            "You are a concise assistant. Convert the user input into a single question. Try to be relevant to the user input. Ask for clarification, evidence, or exploration as appropriate, but do not repeat the same template every time."
        )

    def _build_task_prompt(self, frame: UserFrame, strategy: str, depth: int, mode: str) -> str:
        return (f"Context:\n"
                # f"Topic: {frame.topic}\n"
                f"Claim: \"{frame.claim}\"\n"
                # f"Emotion: {frame.emotion}\n\n"
                f"Question strategy: {strategy}\n"
                f"Depth level: {depth}\n"
                f"Tone: {mode}\n\n"
                f"Ask ONE question only.")

    # --------------------
    # Output validation
    # --------------------

    def _validate_response(self, text: str) -> str:
        text = text.strip()

        # if not text.endswith("?"):
        #     raise ValueError("LLM did not return a question")
        #
        # if text.count("?") > 1:
        #     raise ValueError("Multiple questions detected")
        #
        # banned_words = ["should", "try", "pampalugo"]
        # if any(word in text.lower() for word in banned_words):
        #     raise ValueError("Advice detected in response")

        return text
