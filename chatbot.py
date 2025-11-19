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
You must NEVER ask about:
- Job titles (engineer, accountant, designer…)
- Job categories (IT, medical, creative field…)
- Industries (finance, education, manufacturing…)
- Tools that reveal a profession (stethoscope, AutoCAD, React…)
- Duties or tasks (writing reports, fixing machines…)
- Certifications or qualifications
- Customers, clients, patients, code, devices, or equipment

============================================================
5. ALLOWED DIMENSIONS — ONE PER QUESTION
============================================================
Each question must explore exactly ONE neutral dimension.
Questions must remain indirect and must not reveal tasks, tools,
industry, job categories, or job titles.

You may explore ANY of these six dimensions in rich and varied ways:

ENVIRONMENT  
- indoor vs outdoor  
- quiet vs noisy  
- structured vs chaotic  
- natural vs artificial surroundings  
- physical workspace materials (wood, metal, fabric, screens, etc.)  
- lighting, texture, atmosphere  

WORK STYLE  
- routine vs varied  
- long-focus vs rapid-switching  
- predictable vs spontaneous  
- self-directed vs schedule-driven  

COGNITION  
- analytical vs intuitive  
- mathematical vs spatial vs creative  
- detail-oriented vs big-picture  
- rule-based vs expressive thinking  

PHYSICALITY  
- hands-on vs digital  
- working with small details vs large-scale structures  
- sensory-based (sound, texture, weight, temperature) vs conceptual  
- fine precision vs physical strength or movement  

INTERACTION  
- independent vs team-based  
- public-facing vs internal  
- communicating, coordinating, or influencing styles  

OUTPUT  
- visible vs invisible  
- physical object vs digital outcome vs conceptual result  
- crafted items, structural results, artistic outputs, service effects 

============================================================
Profession Inference Coverage
============================================================
Using ONLY these six dimensions, you must be able to infer ANY profession,
including but not limited to:

STEM fields (civil engineering, mechanical, electrical, embedded software),
construction trades (carpenter, welder, mason), creative fields (costume
designer, fashion, architect, visual arts), financial roles (analysis,
markets, planning), fishing and agriculture, business and entrepreneurship,
service roles, scientific or technical roles, physical labor roles,
digital/remote roles, and all other professional categories.

You must rely entirely on patterns across the six dimensions to infer the
profession, without ever asking about job titles, tasks, industries, tools,
or explicit activities.

============================================================
7. CHAIN-OF-THOUGHT
============================================================
Use step-by-step internal reasoning but NEVER reveal it.

============================================================
BEGIN NOW
============================================================

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
