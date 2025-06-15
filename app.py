import gradio as gr
import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openchat/openchat-3.5-0106:free"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """
You are Esther Shenboyejo — a warm, emotionally intelligent coach for business founders.
You support entrepreneurs in navigating business growth, love life, and mental clarity.
Use a warm, conversational tone. Give practical advice with relatable examples. Be brief and kind.
"""

def chat_with_esther(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user, reply in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": reply})
    messages.append({"role": "user", "content": message})

    try:
        response = requests.post(
            ENDPOINT,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "I'm reconnecting… please try again in a moment 💜"
    except:
        return "I'm reconnecting… please try again in a moment 💜"

chatbot = gr.ChatInterface(
    fn=chat_with_esther,
    title="💬 Ask Esther — Your Founder's AI Coach",
    description="Esther helps you grow your business, love deeply, and stay sane 💜",
    theme=gr.themes.Soft(),
    chatbot=gr.Chatbot(height=420),
    placeholder="Ask Esther anything…",
)

chatbot.launch()
