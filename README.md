```markdown
# E-commerce Data Chatbot

A local Streamlit chatbot powered by a GGML Llama model that converts user questions into SQL, queries your e-commerce database, and returns answers (with optional charts).

## Setup
1. Clone this repo.
2. Add CSVs to `data/` and place `ggml-model.bin` in `models/`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. To launch Streamlit UI:
   ```bash
   streamlit run streamlit_app.py
   ```
5. (Optional) To serve an API endpoint:
   ```bash
   python app.py
   ```
```
