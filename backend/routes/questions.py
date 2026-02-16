from flask import Blueprint, request, jsonify
from backend.engine.processing_engine import ProcessingEngine
from backend.llm.call_llm import CallLLM

generate_question_route = Blueprint("questions", __name__)
engine = ProcessingEngine(CallLLM())

@generate_question_route.route("/generate_question", methods=["POST"])
def generate_question():
    data = request.json
    print("Received JSON:", data)

    try:
        text = engine.generate_question(
            user_input=data,
            lang=data.get("lang", "en")   # 👈 pass language
        )
        print("Generated result:", text)
        return jsonify({"result": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500





