import pandas as pd
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# EXTRACT
df = pd.read_csv("users.csv")
users = df.to_dict(orient="records")

# TRANSFORM
for user in users:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"""
Crie uma mensagem curta sobre sobre carros para {user['name']}.
Regras:
- Responda APENAS com a frase final.
- Máximo 100 caracteres.
"""
)

    text = response.text.strip().replace("\n", " ").replace('"', "'")

    user["news"] = text

# LOAD
df = pd.DataFrame(users)
df.to_csv("resultado.csv", index=False)

print("\nPronto ;)")