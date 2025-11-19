# Career Ladder — Show Mimic Chatbot  
### LM Studio + Python (Auto-Repair, 10-Question Interview Bot)

This project implements **Career Ladder — Show Mimic**, a strict-format, show-style career-guessing chatbot powered by a **local LLM** through **LM Studio**.  
The chatbot conducts an **indirect 10-question interview**, then generates a final career prediction.

Your entire logic (system prompt, reinforcement prompt, auto-repair, final prediction mode) lives inside one file:

➡️ `chatbot.py`

---

## 📌 Features

- Fully offline via **LM Studio Local Server API**
- Strict two-line format for every question:
  ```
  INSIGHT: <short inference>
  QUESTION: <one indirect question only>
  ```
- Enforces:
  - NO job titles  
  - NO tools  
  - NO industries  
  - NO tasks  
  - NO greetings  
- Automatically repairs malformed model output
- Collects 10 user answers
- Produces a **final prediction** with 3–5 explanatory sentences
- Clean UX with Insight + Question printing
- Uses your chosen model (`mistralai/mistral-7b-instruct-v0.3`)

---

## 📁 Project Structure

```
career-ladder/
│
├── chatbot.py     # The complete chatbot logic
└── README.md      # This documentation
```

---

## 🛠 Requirements

### LM Studio
1. Download LM Studio: https://lmstudio.ai  
2. Load a chat-capable model (your script uses Mistral)
3. Enable Local Server:  
   - Developer → **Start Local Server**
   - It will run at:
     ```
     http://localhost:1234/v1/chat/completions
     ```

### Python Dependencies

```
python 3.8+
pip install requests
```

---

## ⚙️ Configuration (Inside `chatbot.py`)

These values can be changed at the top of the script:

```python
API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-7b-instruct-v0.3"

TEMPERATURE = 0.35
MAX_TOKENS = 200
```

---

## ▶️ How to Run

Start LM Studio in Local Server mode, then run:

```
python chatbot.py
```

The bot begins automatically:

```
INSIGHT: We are beginning the Career Ladder interview.
QUESTION: Do you mostly work indoors or outdoors?
```

You then answer 10 indirect questions.

---

## 🎬 Interview Flow

### **Each round includes:**
1. Model asks a question (strict INSIGHT/Q format)
2. You answer
3. Reinforcement prompt is injected to enforce discipline
4. Auto-repair checks for valid formatting
5. Model asks next question

Example console output:

```
🧩 Insight: You appear to work mostly indoors.
Q4: Would you describe your environment as quiet or active?
```

---

## 🧠 Final Prediction Mode

After collecting 10 answers, the script enters:

```
FINAL PREDICTION MODE
```

The model receives:

- All 10 user answers  
- Instructions to provide:
  - 3–5 sentence explanation
  - 1–3 job titles  
  - NO chain-of-thought  
  - NO INSIGHT/QUESTION formatting  

Example output:

```
Final prediction: Financial Analyst, Market Researcher
```

---

## 🧩 Auto-Repair System

If the LLM ever produces a malformed response (missing INSIGHT or QUESTION), the script repairs it:

```
⚠️ Malformed response — applying repair.
```

This guarantees continuity even with weaker models.

---

## 🔧 Customization

You may easily modify:

- Temperature (creativity vs discipline)
- Question strictness
- Output style
- Which dimension each question covers
- Logging conversations to a file
- Swapping models in LM Studio

---

## 🧪 Troubleshooting

### ❗ Model breaks format
Lower temperature:
```
TEMPERATURE = 0.2
```

### ❗ LM Studio connection error
Restart LM Studio → Developer → Start Local Server.

### ❗ Model not responding
Disable streaming mode in LM Studio if it's ON.

---

## 📜 License
Free for personal or commercial use. No attribution required.

