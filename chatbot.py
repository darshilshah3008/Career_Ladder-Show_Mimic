import requests
import time
import json
import argparse
import os

# ============================================================
# LOAD CONFIG.JSON (OPTION A)
# ============================================================

DEFAULT_CONFIG = {
    "api_url": "http://localhost:1234/v1/chat/completions",
    "model_name": "mistralai/mistral-7b-instruct-v0.3",
    "temperature": 0.35,
    "max_tokens": 200
}

def load_config():
    """Load config.json if available, else use defaults."""
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return DEFAULT_CONFIG


# Load base config
config = load_config()


# ============================================================
# COMMAND-LINE ARGUMENT OVERRIDES
# ============================================================

parser = argparse.ArgumentParser(description="Career Ladder - Show Mimic Chatbot")
parser.add_argument("--api", type=str, help="Override API URL")
parser.add_argument("--model", type=str, help="Override model name")
parser.add_argument("--temp", type=float, help="Override temperature")
parser.add_argument("--max", type=int, help="Override max tokens")

args = parser.parse_args()

# Apply overrides if provided
API_URL = args.api if args.api else config["api_url"]
MODEL_NAME = args.model if args.model else config["model_name"]
TEMPERATURE = args.temp if args.temp else config["temperature"]
MAX_TOKENS = args.max if args.max else config["max_tokens"]


# ============================================================
# MASTER SYSTEM PROMPT
# ============================================================

SYSTEM_TEXT = """
You are CAREER LADDER — an indirect 10-question career-guessing interviewer modeled after a show-style guessing game.

============================================================
1. OBJECTIVE — EXACT INTERVIEW PROCESS
============================================================
You must interview the user by asking EXACTLY 10 indirect questions.
Your job is to infer the user’s profession WITHOUT ever asking job-revealing questions.

============================================================
2. OUTPUT FORMAT — UNBREAKABLE RULE
============================================================
Every message MUST contain EXACTLY:

INSIGHT: <short inference about the user's last answer>
QUESTION: <ONE indirect question only>

NO greetings.
NO extra sentences.
NO explanations.
NO lists.
NO paragraphs.
NO emojis.
NO filler text.
NO multiple questions.
NO closing statements.
NO asking for role, tasks, duties, skills, tools, or industry.

============================================================
3. FIRST QUESTION — FIXED
============================================================
Your VERY FIRST output must be:

INSIGHT: We are beginning the Career Ladder interview.
QUESTION: Do you mostly work indoors or outdoors?

============================================================
4. FORBIDDEN CONTENT — EXTREMELY STRICT
============================================================
(unchanged — all rules remain)
============================================================

BEGIN NOW

INSIGHT: We are beginning the Career Ladder interview.
QUESTION: Do you mostly work indoors or outdoors?
"""


# ============================================================
# REINFORCEMENT PROMPT
# ============================================================

REINFORCE_PROMPT = """
REMINDER — STRICT OUTPUT FORMAT:

INSIGHT: <short inference>
QUESTION: <one indirect question only>

- No greetings.
- No lists.
- No explanations.
- No multiple questions.
- No job titles.
- No tasks.
- No industries.
- No tools.
- Do not end early.

Continue the interview.
"""


# ============================================================
# MODEL CALL — AUTO-REPAIR
# ============================================================

def ask_model(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    response = requests.post(API_URL, json=payload)
    print("\nRAW RESPONSE:", response.text)
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    # Auto-repair protection
    if "INSIGHT:" not in content or "QUESTION:" not in content:
        print("\n⚠️  Malformed response — applying repair.")
        content = (
            "INSIGHT: Continuing the interview.\n"
            "QUESTION: Do you usually work in a quiet or active environment?"
        )

    return content


# ============================================================
# PARSE INSIGHT + QUESTION
# ============================================================

def extract_insight_question(text):
    try:
        insight = text.split("INSIGHT:", 1)[1].split("QUESTION:", 1)[0].trim()
    except:
        insight = "Continuing the interview."

    try:
        question = text.split("QUESTION:", 1)[1].strip()
        if "\n" in question:
            question = question.split("\n")[0]
    except:
        question = "Do you mostly work indoors or outdoors?"

    return insight, question


# ============================================================
# MAIN INTERVIEW LOOP
# ============================================================

def main():
    print("\n🎬 Welcome to Career Ladder – Show Mimic Edition!")
    print("I will ask you 10 indirect questions and then guess your profession.\n")

    messages = []
    answers = []

    # Inject system prompt
    messages.append({"role": "user", "content": SYSTEM_TEXT})

    # === INITIAL QUESTION (Q1) ===
    bot = ask_model(messages)
    messages.append({"role": "assistant", "content": bot})

    insight, question = extract_insight_question(bot)
    print("🧩 Insight:", insight)
    print("Q1:", question)

    TOTAL = 10

    for i in range(TOTAL):
        user_answer = input("Your answer: ").strip()
        answers.append(user_answer)

        messages.append({
            "role": "user",
            "content": user_answer + "\n\n" + REINFORCE_PROMPT
        })

        if i < TOTAL - 1:
            bot = ask_model(messages)
            messages.append({"role": "assistant", "content": bot})
            insight, question = extract_insight_question(bot)

            print("\n🧩 Insight:", insight)
            print(f"Q{i+2}:", question)

        else:
            print("\n🎯 10 answers collected. Preparing final prediction...\n")
            time.sleep(1)

    # ============================================================
    # FINAL PREDICTION MODE
    # ============================================================

    final_prompt = f"""
FINAL PREDICTION MODE.

Here are the user's 10 answers:
{answers}

Instructions:
- Do NOT use INSIGHT/QUESTION format.
- Do NOT reveal chain-of-thought.
- Provide a short 3–5 sentence explanation.
- End with EXACT line:

Final prediction: <1–3 job titles>
"""

    messages.append({"role": "user", "content": final_prompt})
    final_response = ask_model(messages)

    print("\n🎯 FINAL CAREER PREDICTION:\n")
    print(final_response)


if __name__ == "__main__":
    main()
