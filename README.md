# Tenjin
Tenjin is a comprehensive AI powered tool built to help organize, analyze, and summarize complex case documents.

## Planned Features

### Document Management
Tenjin smoothly integrates with existing solutions including One Drive, Google Drive, and Sharepoint. to safely access documents. After summarizing and cataloging such texts, the LLM uses semantic search and historical context to generate conversational question and answer.

### Conversational Question and Answering
Tenjin can instantly locate answers and conduct a detailed dialogue regarding data from the document management system. Tenjin intelligently detects the context and intent of the query and provides precise replies in real time. It speeds up research. Tenjin can also leverage query patterns to provide more appropriate results. Providing customized answers improves efficiency.

### Semantic Search
Keyword search powers most features like Case Notebook and Case Fleet. Semantic search is used by Tenjin to return results. This makes document and case note searches more accurate and efficient. Tenjin will provide results for "breach of contract" that contain the phrases "breach" and "contract" as well as related terms like "violation of the agreement." This helps lawyers quickly find the most essential case papers.

### Summarization
Data analysis requires summarizing massive datasets and automatically building knowledge graphs that link related data. It helps consumers quickly understand data and its relationships. Topic modeling, sentiment analysis, and summarization algorithms can simplify enormous data sets.

### Transcription and Diarisation 
Recorded conversations can be automatically transcribed and speaker-diarized to help you find connections to other case documents. As a result, Tenjin may incorporate sworn testimony, expert interviews, and other legal documents into its natural-sounding QA.

Real-time transcription combined with semantic search and summarization will help convey relevant information and recommend next steps in interviews of the future.

## Requirements
- Python 3.10+
- node  17+
- pnpm
- Docker / Docker Compose
- [Poetry]([Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/)) 

## Setup and Run

### Backend

> To run the base app, you don't need to run Dagster this is simply for importing files into Weaviate (Semantic search db).

```bash
$ git clone https://github.com/Uncommon-intelligence/tenjin.git
$ cd tenjin
$ poetry install

# To run the application simply run
$ make dev
```


### Frontend

```bash
# from the tenjin directory
$ cd frontend
$ pnpm install

# To urn the application
$ pnpm dev
```
