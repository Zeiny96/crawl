import json
import re
import openai
import google.generativeai as genai
from openai import OpenAI
from google.generativeai import GenerativeModel
from config import OPENAI_API_KEY, GENAI_API_KEY, USE_OPENAI

# Configure keys
openai.api_key = OPENAI_API_KEY
genai.configure(api_key=GENAI_API_KEY)

def choose_best_key_path(question, key_only_dict, chat_history=None):
    if chat_history is None:
        chat_history = []

    system_prompt = f"""
You are a smart assistant. Based on the following nested menu structure (keys only), return the most relevant full path (as a JSON array of strings) to answer the user query.

Menu:
{json.dumps(key_only_dict, ensure_ascii=False)}

[If no valid path is found return only None.]
""".strip()

    if not any(msg['role'] == 'system' for msg in chat_history):
        chat_history.insert(0, {"role": "system", "content": system_prompt})

    chat_history.append({"role": "user", "content": question})

    if USE_OPENAI:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=chat_history
        )
        content = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": content})
        return json.loads(content), chat_history
    else:
        prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in chat_history])
        model = GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        text = response.text.strip()
        match = re.search(r'\[[^\]]+\]', text)
        chat_history.append({"role": "assistant", "content": text})
        return (json.loads(match.group(0)), chat_history) if match else ([], chat_history)

