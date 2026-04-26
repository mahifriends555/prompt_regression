

# Prompt Regression Eval 🚀

A lightweight tool to test, evaluate, and compare LLM outputs across prompts and models.

---

## 📌 What This Project Does

This project helps you:

- Define prompt-based test cases using YAML
- Run prompts on multiple models (GPT + Gemini)
- Evaluate outputs using an LLM as a judge
- Track performance over time (regression detection)
- Compare model outputs for the same prompt

---

## 🧠 Core Idea

```

Prompt → Model → Output → Evaluation → Comparison

```

This tool checks:

👉 *“For this prompt, is the model still giving correct output?”*

---

## 🤖 Models Used

### Generator Models (produce answers)
- GPT → `gpt-4o-mini`
- Gemini → `gemini-flash-latest`

### Judge Model (evaluates answers)
- GPT → `gpt-4o` (or `gpt-4o-mini`)

---

## 📂 Project Structure

```

prompt_regression/
│
├── data/
│   └── tests.yaml        # Prompt test cases
│
├── prompt_regression/
│   ├── config_loader.py  # Load YAML tests
│   ├── models.py         # Data models
│   ├── runner.py         # Run prompts on models
│   ├── scorer.py         # LLM-based evaluation
│   ├── comparator.py     # Compare with previous runs
│   ├── storage.py        # SQLite storage
│   ├── reporter.py       # Terminal output
│   └── main.py           # Entry point
│
├── .env                  # API keys (not committed)
├── requirements.txt
└── README.md

```

---

## ⚙️ Setup Instructions

### 1. Clone repository

```

git clone [https://github.com/mahifriends555/prompt_regression.git](https://github.com/mahifriends555/prompt_regression.git)
cd prompt_regression

```

---

### 2. Create virtual environment

```

python -m venv venv1
venv1\Scripts\activate   # Windows

```

---

### 3. Install dependencies

```

pip install -r requirements.txt

```

---

### 4. Create `.env` file

Create a `.env` file in the root directory:

```

OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key

```

⚠️ Never commit this file

---

## 🧪 Writing Test Cases

Edit:

```

data/tests.yaml

````

Example:

```yaml
- name: greeting_test
  prompt: "Say hello to the user"
  expected: "Hello! How can I help you today?"

- name: summary_test
  prompt: "Summarize: AI is transforming industries."
  expected: "AI is changing industries."
````

---

## ▶️ Run the Project

```
python main.py
```

---

## 📊 Example Output

```
Test Name            Similarity   Prev Score   Status
----------------------------------------------------
greeting_test_gpt       0.90        0.90       NO CHANGE
greeting_test_gemini    1.00        1.00       NO CHANGE
```

---

## 🧠 Key Concepts

### 1. Prompt-Based Testing

Each test checks how a model responds to a specific prompt.

---

### 2. LLM-as-a-Judge

A model (GPT) evaluates outputs instead of using simple string matching.

---

### 3. Regression Detection

The system compares current results with previous runs to detect performance drops.

---

### 4. Multi-Model Evaluation

Same prompt is tested across:

* GPT
* Gemini

---

## ⚠️ Notes

* Scores depend on evaluation strictness
* Judge model may introduce bias
* First run has no baseline for comparison
* Outputs are normalized across models

---

## 👨‍💻 Author

Mahendra

````
