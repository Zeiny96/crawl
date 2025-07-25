import json
from config import USE_OPENAI
from utils.helpers import extract_key_paths
from utils.llm import choose_best_key_path

class ChatbotSession:
    def __init__(self):
        with open('data/scrap.json', 'r', encoding='utf-8') as f:
            self.full_dict = json.load(f)

        with open('data/details.json', 'r', encoding='utf-8') as f:
            self.details_dict = json.load(f)

        self.key_only_dict = extract_key_paths(self.full_dict)
        self.chat_history = []

    def handle_question(self, q):
        try:
            key_path, self.chat_history = choose_best_key_path(q, self.key_only_dict, self.chat_history)

            node = self.full_dict
            for k in key_path:
                node = node[k]

            def find_first_url(d):
                for v in d.values():
                    if isinstance(v, str): return v
                    elif isinstance(v, dict):
                        result = find_first_url(v)
                        if result: return result
                return None

            url = node if isinstance(node, str) else find_first_url(node)

            if key_path:
                path_str = "/".join(key_path)
                answer = {
                    "matched_path": path_str,
                    "url": url,
                    "detailed_answer": None,
                    "message": "تم العثور على مسار مطابق"
                }

                if path_str in self.details_dict:
                    followup_prompt = f"""السؤال: {q}

اعتمد فقط على المحتوى التالي للإجابة:

{self.details_dict[path_str]}"""

                    if USE_OPENAI:
                        from openai import OpenAI
                        client = OpenAI()
                        chat = [{"role": "system", "content": "أجب باللغة العربية فقط."},
                                {"role": "user", "content": followup_prompt}]
                        response = client.chat.completions.create(model="gpt-4o", temperature=0, messages=chat)
                        answer["detailed_answer"] = response.choices[0].message.content.strip()
                    else:
                        from google.generativeai import GenerativeModel
                        model = GenerativeModel('gemini-2.0-flash')
                        response = model.generate_content(followup_prompt)
                        answer["detailed_answer"] = response.text.strip()

                else:
                    answer["message"] = "لا يوجد محتوى تفصيلي لهذا القسم."
                return answer
            else:
                return {"message": "لا استطيع الاجابة على هذا السؤال"}
        except Exception as e:
            return {"error": str(e)}
