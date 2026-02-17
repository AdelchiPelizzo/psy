from flask import Blueprint, request, jsonify
from backend.engine.processing_engine import ProcessingEngine
from backend.llm.call_llm import CallLLM

generate_question_route = Blueprint("questions", __name__)
engine = ProcessingEngine(CallLLM())

import traceback

@generate_question_route.route("/generate_question", methods=["POST"])
def generate_question():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    user_id = data.get("user_id", "default_user")  # fallback for demo
    print("Received JSON:", data)

    try:
        text = engine.generate_question(
            user_input=data,
            user_id=user_id,
            lang=data.get("lang", "en")
        )
        print("Generated result:", text)
        return jsonify({"result": text})
    except Exception as e:
        # Print full traceback for debugging
        print("ERROR in /generate_question:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500







