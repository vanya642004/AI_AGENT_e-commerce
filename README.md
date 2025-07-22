```markdown
# E-commerce CSV Query Agent

A Streamlit app that lets you upload any number of CSV files, uses a local GGML Llama model to translate natural‑language questions into SQL, queries the uploaded data, and presents answers (with optional charts).

## Setup
1. Clone this repo.
2. Place a GGML Llama model binary as `models/ggml-model.bin`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage
- On startup, upload one or more CSV files via the file uploader.
- Ask any question about your data; the app will generate and run SQL against all tables.
- View the generated SQL, tabular results, and charts for numeric outputs.
```

