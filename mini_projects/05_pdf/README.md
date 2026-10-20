# 05 Pdf

A Streamlit app that turns a PDF into a quiz question: upload a PDF, LangChain indexes it in a Chroma vectorstore, and AutoGen agents query it (via an `ask_question` tool) to write a multiple-choice question with the answer and reason, convert it to JSON and save it to disk for the page to display. `pdfsummary.py` is a separate LangChain-only script that summarizes a PDF: `python pdfsummary.py path/to/file.pdf ["question"]` (OpenAI by default; set `OPENAI_BASE_URL` to use a local server such as LM Studio).

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Put your `OPENAI_API_KEY` in a `.env` file, then:

```bash
streamlit run main.py
```
