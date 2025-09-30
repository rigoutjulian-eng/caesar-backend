from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)   # ✅ il faut créer app AVANT
CORS(app, resources={r"/chat": {"origins": "*"}})   # ✅ puis activer CORS

# Initialiser le client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = {
    "role": "system",
    "content": (
        "Tu es Caesar, un consultant IA professionnel. "
        "Ton rôle est d'aider les clients à exprimer leurs besoins afin de rédiger un cahier des charges clair, structuré et sur mesure. "
        "Tu poses des questions intelligentes et précises pour comprendre leurs objectifs, leurs contraintes, leur contexte, leur budget et leurs délais. "

        "⚠️ Règle très importante : tu ne poses **qu'une seule question à la fois**. "
        "Après chaque réponse du client, tu analyses sa réponse et poses ensuite la question suivante la plus pertinente en fonction de ce qui a été dit. "
        "Tu construis donc l’échange étape par étape, comme une vraie discussion, sans jamais envoyer une liste de questions. "

        "À la fin de l’échange, quand tu estimes avoir toutes les informations nécessaires, tu annonces clairement que tu vas rédiger le cahier des charges, "
        "puis tu fournis un document clair, complet, détaillé et professionnel, prêt à être transmis à une équipe technique. "

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
        conversation = [system_prompt] + user_messages

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok", "message": "Caesar backend is running ✅"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
