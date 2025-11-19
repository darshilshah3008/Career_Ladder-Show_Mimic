# Career Ladder — Show Mimic Chatbot  
### LM Studio + Python (Local LLM, Config Support, Auto‑Repair, 10‑Question Interview Bot)

Career Ladder — Show Mimic is a show‑style career‑guessing chatbot designed to run **fully locally** using **LM Studio’s Local Server API**.  
The chatbot asks the user **10 indirect questions**, each following the strict format:

```
INSIGHT: <short inference>
QUESTION: <one indirect question only>
```

At the end of the session, the bot produces a **final career prediction** based on your 10 responses.

This project includes config‑file support and command‑line overrides so anyone can run the chatbot regardless of their LM Studio setup.

---

## 🚀 Features

- Runs 100% offline via LM Studio  
- Strict INSIGHT/QUESTION format enforced  
- Auto‑repair system for malformed LLM responses  
- Loads configuration from `config.json`  
- Command‑line override support  
- Clean terminal output with insight + question separation  
- Final prediction mode (3–5 sentence explanation + career guess)

---

## 📁 Project Structure

```
career-ladder/
│
├── chatbot.py       # Main chatbot script
├── config.json      # User-editable configuration file
└── README.md        # Documentation
```

---

## 🛠 Requirements

### LM Studio
1. Install LM Studio → https://lmstudio.ai  
2. Load a chat‑capable model (e.g., Mistral, LLaMA, Gemma, etc.)  
3. Start Local Server:  
   **Developer → Start Local Server**  
4. Default endpoint:  
   ```
   http://localhost:1234/v1/chat/completions
   ```

### Python
```
python 3.8+
pip install requests
```

---

## ⚙️ Configuration (`config.json`)

The chatbot loads settings from `config.json`:

```json
{
    "api_url": "http://localhost:1234/v1/chat/completions",
    "model_name": "mistralai/mistral-7b-instruct-v0.3",
    "temperature": 0.35,
    "max_tokens": 200
}
```

Users may edit these values to match their LM Studio setup.

---

## ▶️ How to Run

### Basic usage (uses `config.json`):
```
python chatbot.py
```

### Windows PowerShell:
```
python .\chatbot.py
```

### macOS / Linux:
```
python3 chatbot.py
```

If LM Studio is running, the chatbot begins with:

```
INSIGHT: We are beginning the Career Ladder interview.
QUESTION: Do you mostly work indoors or outdoors?
```

---

## 🧩 Command‑Line Overrides

You may override config.json on the fly:

### Change API URL:
```
python chatbot.py --api http://localhost:9000/v1/chat/completions
```

### Change model:
```
python chatbot.py --model mistralai/Mistral-7B-Instruct-v0.2
```

### Override temperature:
```
python chatbot.py --temp 0.2
```

### Override max tokens:
```
python chatbot.py --max 300
```

Overrides always take priority over config.json.

---

## 🎬 Interview Flow

1. Bot asks the fixed first question  
2. You answer  
3. Bot generates INSIGHT + new QUESTION  
4. Process repeats for **10 questions**  
5. Script enters **Final Prediction Mode**  
6. Bot outputs:
   - 3–5 sentence explanation  
   - **Final prediction: \<job titles\>**

---

## 🛠 Auto‑Repair Protection

If the LLM breaks formatting, the script corrects it:

```
⚠️ Malformed response — applying repair.
```

This ensures stability even on small or experimental models.

---

## 🧪 Troubleshooting

### ❗ The bot does not respond
Ensure LM Studio Local Server is running.

### ❗ Wrong API URL
Edit:
```
api_url in config.json
```
or run:
```
python chatbot.py --api <your_url>
```

### ❗ Model breaks formatting
Lower the temperature:
```
"temperature": 0.2
```

---

## 📜 License
Free for personal and commercial use. No attribution required.

---

If you'd like, I can also generate:
- A ZIP containing the whole project  
- A colored terminal UI version  
- A Gradio or web UI version  
- A `.bat` or `.sh` launcher  
Just ask!
