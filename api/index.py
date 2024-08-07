from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__)

# Configurer l'API Google AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

@app.route('/api', methods=['GET'])
def get_response():
    user_input = request.args.get('ask', '')
    if not user_input:
        return jsonify({"error": "No question provided"}), 400

    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [
            "Quel modèle as-tu?",
          ],
        },
        {
          "role": "model",
          "parts": [
            "Je suis un grand modèle linguistique, entraîné par Google.",
          ],
        },
      ]
    )

    response = chat_session.send_message(user_input)
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
