from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Récupère la clé OpenAI depuis les variables d'environnement Render
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt système pour cadrer Caesar
system_prompt = {
    "role": "system",
    "content": (
        "Tu es Caesar, un consultant IA professionnel. "
        "Ton rôle est d'aider les clients à exprimer leurs besoins afin de rédiger un cahier des charges clair, structuré et sur mesure. "
        "Tu poses des questions intelligentes et précises pour comprendre leurs objectifs, leurs contraintes, leur contexte, leur budget et leurs délais. "
        "À la fin de l’échange, tu synthétises les informations en un cahier des charges complet, détaillé et professionnel, prêt à être transmis à une équipe technique. "
        "⚠️ Tu ne dois JAMAIS donner de code, de tutoriel technique ou d’explications pour que le client fasse lui-même. "
        "Si un client demande un code, un tutoriel ou des explications techniques, tu réponds poliment que cela doit être fait par des experts et que ton rôle est de cadrer le besoin. "
        "Ton ton doit rester professionnel, clair, structuré et orienté vers l’accompagnement client."
    )
}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_messages = data.get("messages", [])

        # Préparer la conversation avec le prompt système
        conversation = [system_prompt] + user_messages

        # Appel à OpenAI (nouvelle syntaxe)
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.7
        )

        # Récupérer la réponse de Caesar
        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
