import google.generativeai as genai
from flask import request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key from the environment variable
genai.configure(api_key=os.getenv("GEMINI_KEY"))

def ai_assistant():
    """
    Handles AI queries using the Gemini model.
    Accepts a 'query' parameter via request.
    """
    try:
        # Get the query parameter from the request
        query = request.args.get("query", "")

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        # Initialize the Gemini model
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

        # Generate content using the AI model
        response = model.generate_content(
            f"Assume you are an expert electrician and you know how an electricity grid is managed and maintained in multiple sectors. Answer the question and don't go outside of your expertise: {query}"
        )

        # Return the AI-generated response
        return jsonify({"response": response.text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
