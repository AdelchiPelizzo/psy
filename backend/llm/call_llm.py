import os
import yaml

# Load config
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)


class CallLLM:
    def __init__(self):
        self.mock = os.getenv("MOCK_LLM", "false").lower() == "false"
        self.config = config

        print("🚦 MOCK_LLM =", self.mock)

        if not self.mock:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.config["openai_api_key"])
        else:
            self.client = None

    def call(self, user_input, system_prompt=None):
        # Use system_prompt from config if not provided
        if system_prompt is None:
            system_prompt = self.config.get(
                "system_prompt_template",
                "You are a psychoanalytic AI assistant. Analyze the claim and provide one concise observation and, if needed, a follow-up question."
            )

        # MOCK MODE
        if self.mock:
            return {"observation": "Your claim seems plausible.", "question": "Can you provide evidence for this claim?"}

        # REAL MODE
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=self.config["max_output_tokens"],
                temperature=self.config["temperature"],
            )

            text = response.choices[0].message.content.strip()

            # Split Observation / Question if AI returned both
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
