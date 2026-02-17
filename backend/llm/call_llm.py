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
        Calls the LLM with the given user input, optional system prompt,
        and optional in-memory conversation history.
        Returns a dict: {"observation": str, "question": str}
        """

        # Use system_prompt from YAML if not provided
        if system_prompt is None:
            system_prompt = self.config.get("system_prompt_template",
                "You are a psychoanalytic AI assistant. Analyze the claim and provide one concise observation and, if needed, a follow-up question.")

        if conversation_history is None:
            conversation_history = []

        # -----------------------------
        # MOCK MODE
        # -----------------------------
        if self.mock:
            return {"observation": "Your claim seems plausible.",
                "question": "Can you provide evidence for this claim?"}

        # -----------------------------
        # REAL MODE
        # -----------------------------
        try:
            # Build messages: system prompt + history + current user input
            messages = [{"role": "system", "content": system_prompt}]
            messages += conversation_history  # previous turns
            messages.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(model=self.config["model"], messages=messages,
                max_tokens=int(self.config.get("max_output_tokens", 150)),
                temperature=float(self.config.get("temperature", 0.8)), top_p=float(self.config.get("top_p", 0.9)),
                frequency_penalty=float(self.config.get("frequency_penalty", 0.2)),
                presence_penalty=float(self.config.get("presence_penalty", 0.0)), )

            text = response.choices[0].message.content.strip()

            # Split Observation / Question
            obs, ques = "", ""
            if "Question:" in text:
                parts = text.split("Question:", 1)
                obs = parts[0].strip()
                ques = parts[1].strip()
            else:
                obs = text
                ques = ""

            return {"observation": obs, "question": ques}

        except Exception as e:
            return {"observation": f"[LLM error: {str(e)}]", "question": ""}

