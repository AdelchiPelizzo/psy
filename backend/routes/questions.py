from flask import Blueprint, request, jsonify
from backend.engine.processing_engine import ProcessingEngine
from backend.llm.call_llm import CallLLM

generate_question_route = Blueprint("questions", __name__)
engine = ProcessingEngine(CallLLM())

@generate_question_route.route("/generate_question", methods=["POST"])
def generate_question():
    data = request.json
    user_id = data.get("user_id", "default_user")  # fallback for simple demo
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
        return jsonify({"error": str(e)}), 500






