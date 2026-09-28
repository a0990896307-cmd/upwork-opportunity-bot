# Proposal — Chatbot for University Information Retrieval

**Frameworks I've worked with:**
- Python: FastAPI, BeautifulSoup/Scrapy (web scraping), LangChain/LlamaIndex (RAG pipelines), ChromaDB/Qdrant (vector stores)
- AI: OpenAI-compatible APIs, local models via Ollama, embeddings (sentence-transformers)
- DevOps: Docker, Docker Compose, scheduled jobs (celery/cron) for periodic re-scraping

**Recent experience with similar projects:**
I've built document-retrieval and chatbot systems in Python, including a rule-based retrieval bot pipeline and an RAG-driven assistant that indexes documents and answers questions from them. I work with structured storage, cleaning scraped HTML into searchable text, and building configurable scraping intervals — which matches your "scrape every 10-20 days, configurable per university via frontend" requirement exactly.

**Project approach & QA testing:**
1. **Scraping layer**: per-university adapters, configurable interval stored in DB, exposed via frontend settings.
2. **Indexing**: clean HTML → chunk → embed → vector store (ChromaDB/Qdrant), with dedup so re-scrapes update entries without duplicates.
3. **Retrieval + answer**: hybrid search (keyword + vector), LLM generates answer grounded only in retrieved context; "I don't know" when nothing relevant is found.
4. **Testing**: golden question set per university, automated eval (hit-rate, answer faithfulness) after each re-scrape; HTTP health checks so the service stays highly available.

**Certifications:** None formal — my track record is shipped Python projects (portfolio available on request).

**How I'll work:** modular code (scraper / indexer / API / UI), Docker Compose setup, clear README. You'll be able to run it locally, add universities via the frontend, and watch it re-scrape on schedule.

I can deliver a working first version in about a week. Ready to start — happy to discuss scope and get your university list.

Best,
[Your name]