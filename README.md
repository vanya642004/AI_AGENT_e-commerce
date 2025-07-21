```markdown
# E‑commerce AI Agent

This project is an AI-powered agent that enables natural language querying of structured e-commerce datasets.

### ✨ Features:
- Accepts user queries via FastAPI or Streamlit interface
- Uses a lightweight LangChain-based LLM agent to convert questions to SQL
- Executes SQL on structured product sales and marketing data
- Returns answers in human-readable form
- Bonus: Includes support for real-time streaming and optional chart visualization

### 🔧 Tech Stack:
- **LangChain** for agent orchestration
- **Hugging Face (Flan-T5)** as LLM
- **SQLite** as the backend DB
- **FastAPI** and **Streamlit** for deployment

### 📊 Dataset Coverage:
- Product-Level Total Sales
- Product-Level Ad Sales
- Product Eligibility Table

### 📌 Objective:
To demonstrate intelligent question answering on product metrics, such as:
- "What is my total sales?"
- "Calculate the Return on Ad Spend (RoAS)"
- "Which product had the highest CPC?"

This project aligns with GenAI intern roles involving LangChain, RAG, and LLM integration with real-world business data.
```
.
├── .gitignore
├── README.md
├── app.py
├── db_init.py
├── query_agent.py
├── utils.py
├── streamlit_app.py
├── prompts/
│   └── sql_prompt.txt
├── data/
│   ├── total_sales.csv
│   ├── ad_sales.csv
│   └── eligibility.csv
├── .streamlit/
│   └── config.toml
└── requirements.txt
```

## ✅ What to Commit

- `app.py`, `db_init.py`, `query_agent.py`, `utils.py`, `streamlit_app.py`
- `prompts/` folder
- `requirements.txt`
- `.streamlit/config.toml` (created via CLI)
- `data/` **with** CSVs: `total_sales.csv`, `ad_sales.csv`, `eligibility.csv`
- `README.md` & `.gitignore`

## ❌ What Not to Commit

- `ecommerce.db` (generate via `db_init.py`)
- `__pycache__/`
- Local secrets (e.g., `.env`)

## 🚀 Streamlit Deployment Only

You can upload this project directly to GitHub and connect it to Streamlit Cloud.

### Steps:
1. **Push all project files** (including `streamlit_app.py`, `query_agent.py`, `requirements.txt`, `prompts/`, `data/`, etc.) to a GitHub repository.

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)** and log in with GitHub.

3. **Create a new app**:
   - Pick your GitHub repo
   - Select `streamlit_app.py` as the entry point

4. **Add secret**: Under app settings → secrets, add:
   ```toml
   HUGGINGFACEHUB_API_TOKEN = "<your_token_here>"
   ```

5. **Upload CSVs**: Make sure `data/total_sales.csv`, `ad_sales.csv`, and `eligibility.csv` are in your repo.

6. Streamlit Cloud will build and launch your live app! 🌐

 for `.streamlit/config.toml`
Create via CLI to avoid Explorer issues:
```powershell
cd project_root
md .streamlit
cd .streamlit
echo [server]  > config.toml
echo headless = true >> config.toml
echo port = $PORT   >> config.toml
echo enableCORS = false >> config.toml
```

## 🔑 Secrets
- Set `HUGGINGFACEHUB_API_TOKEN` in your environment or Streamlit Cloud secrets.
```
```

---

## 📄 .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]

# Database
ecommerce.db

# Env
.env

# Streamlit
.streamlit/secrets.toml
```
