import requests

API_URL = "http://127.0.0.1:8000"  # adjust if different

def start_session():
    response = requests.post(f"{API_URL}/start")
    response.raise_for_status()
    session_id = response.json()["session_id"]
    print(f"✅ Session started: {session_id}")
    return session_id

def ask_question(session_id, question):
    response = requests.post(f"{API_URL}/ask", json={
        "session_id": session_id,
        "query": question
    })
    response.raise_for_status()
    return response.json()

def end_session(session_id):
    response = requests.post(f"{API_URL}/end", params={"session_id": session_id})
    response.raise_for_status()
    print(f"🛑 Session {session_id} ended.")

def main():
    session_id = start_session()

    try:
        while True:
            q = input("🧠 اسأل (أو 'exit'): ").strip()
            if q.lower() == "exit":
                break
            answer = ask_question(session_id, q)
            print("🤖 الرد:", answer.get("detailed_answer") or answer.get("message"))

    except KeyboardInterrupt:
        print("\n⛔️ Interrupted.")

    finally:
        end_session(session_id)

if __name__ == "__main__":
    main()
