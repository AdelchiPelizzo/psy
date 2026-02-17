from backend.engine.models import UserFrame


class ProcessingEngine:
    def __init__(self, llm):
        """
        llm: instance of CallLLM
        """
        self.llm = llm

    def generate_question(self, user_input, strategy="evidence", depth=2, mode="neutral", lang="en"):
        # Wrap string input into dict if needed
        if isinstance(user_input, str):
            user_input = {"claim": user_input}

        claim_text = user_input.get("claim", "").strip()
        if not claim_text:
            return "[No claim provided]"

        # 🌍 Localized system prompt
        if lang == "it":
            system_prompt = (
                "Sei un assistente di intelligenza artificiale con approccio psicoanalitico."
                "Compito:"
                "Analizza l'affermazione dell'utente e fornisci un insight psicologico conciso."
                "Regole:"
                "- NON porre domande a meno che l'affermazione sia impossibile da interpretare."
                "- Evidenzia emozioni, schemi comportamentali o motivazioni sottostanti."
                "- Evita consigli banali o osservazioni ovvie."
                "- Mantieni un tono calmo, professionale e non giudicante."
                "Formato della risposta:"
                "Osservazione: <insight psicoanalitico conciso>"
                "Interpretazione: <breve spiegazione della dinamica sottostante>"
                "Guida: <suggerimento costruttivo opzionale>"
            )
        else:
            system_prompt = (
                "You are a psychoanalytic AI assistant."
                "Task:"
                " Analyze the user's statement and provide a concise psychological insight."
                "Rules:"
                "- Do NOT ask questions unless the statement is impossible to interpret."
                "- Provide an observation that reveals underlying emotions, patterns, or motivations."
                "- Avoid generic advice or obvious statements."
                "- Maintain a calm, professional, and insightful tone."
                "Response format:"
                "Observation: <one concise psychoanalytic insight>"
                "Interpretation: <brief explanation of the underlying dynamic>"
                "Guidance: <optional constructive suggestion>"
            )

        # Call LLM
        result = self.llm.call(user_input=claim_text, system_prompt=system_prompt)

        obs = result.get("observation", "").strip()
        ques = result.get("question", "").strip()

        if ques:
            return f"{obs} {ques}"
        else:
            return obs

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
