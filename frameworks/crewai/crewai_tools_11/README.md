# 11 CrewAI Tools

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

One small script per `crewai_tools` tool. Each builds a single agent (`gpt-5.4-mini`) with the
tool and asks you for a question in a loop (type `exit` to quit).

| Script | Tool | Needs |
| --- | --- | --- |
| `code_execution_tool.py` | `E2BPythonTool` | `E2B_API_KEY` |
| `code_execution_tool_and_file_writer.py` | `E2BPythonTool` + `FileWriterTool` | `E2B_API_KEY` |
| `csv_file_rag_search.py` | `CSVSearchTool` on `Financial Sample Data.csv` | |
| `docx_rag_search.py` | `DOCXSearchTool` on `rag_dir/user.docx` | |
| `json_rag_search.py` | `JSONSearchTool` (ask about a file in `rag_dir/`) | |
| `pdf_docs_rag_Search.py` | `PDFSearchTool` on `pdf/AutoGen_Studio-12.pdf` | |
| `exa_search.py` | `ExaSearchTool` | `EXA_API_KEY` |
| `exa_and_website_search.py` | `ExaSearchTool` + `ScrapeWebsiteTool` | `EXA_API_KEY` |
| `serper_dev.py` | `SerperDevTool` | `SERPER_API_KEY` |
| `read_file.py` | `FileReadTool` (e.g. `CodeExamples/bubble_sort.py`) | |
| `vision_rag.py` | `VisionTool` (e.g. `images/cats.jpg`) | |

The code execution scripts used `CodeInterpreterTool` in the video. That tool was removed from
crewai-tools 1.x, so they now use `E2BPythonTool`, which runs the code in an
[E2B](https://e2b.dev/) cloud sandbox.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder with `OPENAI_API_KEY` (also used for the RAG tools'
embeddings) plus any keys from the table above.

## Run

Run the scripts from this folder. The file tools only read and write inside the current
directory:

```bash
python csv_file_rag_search.py
```
