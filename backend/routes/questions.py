from flask import Blueprint, request, jsonify
from backend.engine.processing_engine import ProcessingEngine
from backend.llm.call_llm import CallLLM

generate_question_route = Blueprint("questions", __name__)
engine = ProcessingEngine(CallLLM())

from flask import jsonify, request
from backend.routes.questions import generate_question_route
from backend.engine.processing_engine import ProcessingEngine
from backend.llm.call_llm import CallLLM

engine = ProcessingEngine(CallLLM())

@generate_question_route.route("/generate_question", methods=["POST"])
def generate_question():
    data = request.json
    print("Received JSON:", data)  # ✅ Debug payload

    try:
        result = engine.generate_question(user_input=data)
        print("Generated result:", result)  # ✅ Debug output

        # Make sure result is a dict with keys
        obs = result.get("observation", "")
        ques = result.get("question", "")
        return jsonify({"observation": obs, "question": ques})

    except Exception as e:
        print("Error in generate_question:", e)  # ✅ Full stack trace will show in console
        return jsonify({"observation": f"[Error: {str(e)}]", "question": ""}), 500



