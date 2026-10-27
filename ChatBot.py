
from groq import Groq


class GroqChatbot:

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def stream_reply(self, messages, model="openai/gpt-oss-120b"):

        resposta = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )

        for parte in resposta:
            texto = parte.choices[0].delta.content

            if texto:
                yield texto
