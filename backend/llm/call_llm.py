import os
import yaml
from openai import OpenAI

# -----------------------------
# Load config from YAML
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)


class CallLLM:
    def __init__(self):
        # MOCK_LLM environment variable (default: False)
        # self.mock = os.getenv("MOCK_LLM", "false").strip().lower() == "false"
        self.mock = False
        #
        self.config = config



        print("🚦 MOCK_LLM >> =", self.mock)

        if not self.mock:
            # Read API key from environment
            api_key = os.getenv("OPENAI_API_KEY")
            print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
            self.client = OpenAI(api_key=api_key)

            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is missing! "
                    "Set it locally or in Render's Environment settings."
                )
        else:
            self.client = None

    def call(self, user_input, system_prompt=None, conversation_history=None):
        """
        Calls the LLM with the given user input and optional system prompt.
        Tracks conversation history to produce context-aware responses.
        Returns dict:
            {
                "observation": str,
                "interpretation": str,
                "question": str
            }
        """

        # -----------------------------
        # Default values
        # -----------------------------
        if conversation_history is None:
            conversation_history = []

        if system_prompt is None:
            system_prompt = self.config.get("system_prompt_template", ("You are a psychoanalytic AI assistant.\n"
                                                                       "Analyze the user's statement and provide:\n"
                                                                       "- Observation: one concise insight\n"
                                                                       "- Interpretation: brief explanation\n"
                                                                       "- Question: one targeted follow-up question\n"
                                                                       "Use the full conversation history to detect patterns, recurring emotions, and triggers.\n"
                                                                       "Do not treat this as a new conversation; build on previous exchanges."))

        # -----------------------------
        # MOCK MODE
        # -----------------------------
        if self.mock:
            obs = "You may be expressing uncertainty about how others perceive you."
            interp = "This can reflect underlying social anxiety or fear of judgment."
            ques = "In which situations do you notice this feeling most strongly?"
            # Save mock interaction in history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": f"{obs}\n{interp}\n{ques}"})
            return {"observation": obs, "interpretation": interp, "question": ques}

        # -----------------------------
        # Build message list
        # -----------------------------
        messages = [{"role": "system", "content": system_prompt}]
        # Include last 12 turns for context
        messages.extend(conversation_history[-12:])
        messages.append({"role": "user", "content": user_input})

        # -----------------------------
        # Real API call
        # -----------------------------
        try:
            response = self.client.chat.completions.create(model=self.config["model"], messages=messages,
                max_tokens=self.config.get("max_output_tokens", 150),
                temperature=float(self.config.get("temperature", 0.3)), top_p=float(self.config.get("top_p", 0.9)),
                frequency_penalty=float(self.config.get("frequency_penalty", 0.2)),
                presence_penalty=float(self.config.get("presence_penalty", 0.0)), )

            text = response.choices[0].message.content.strip()

            # -----------------------------
            # Parse structured output
            # -----------------------------
            observation = ""
            interpretation = ""
            question = ""

            for line in text.splitlines():
                line_lower = line.lower()
                if line_lower.startswith("observation:"):
                    observation = line.split(":", 1)[1].strip()
                elif line_lower.startswith("interpretation:"):
                    interpretation = line.split(":", 1)[1].strip()
                elif line_lower.startswith("question:"):
                    question = line.split(":", 1)[1].strip()

            # fallback if model didn't follow format
            if not observation:
                observation = text

            # -----------------------------
            # Update conversation history
            # -----------------------------
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": text})

            return {"observation": observation, "interpretation": interpretation, "question": question, }

        except Exception as e:
            return {"observation": f"[LLM error: {str(e)}]", "interpretation": "", "question": ""}
