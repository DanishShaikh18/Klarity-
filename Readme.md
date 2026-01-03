🧠 Klarity — AI Knowledge Assistant

“An intelligent assistant that understands your study material — upload PDFs, Docs, Images, or YouTube links and ask anything!”

🎯 Project Overview

Klarity is an AI-powered study assistant that helps students and learners interact with their study material using Retrieval-Augmented Generation (RAG).
It can analyze PDFs, images, and YouTube videos to answer questions, summarize notes, and extract key insights — all in one place.

🌟 Purpose

To build a multi-modal AI assistant that can:

Extract, understand, and summarize educational content.

Allow users to query any material (PDFs, Images, YouTube videos).

Deliver contextually accurate and concise answers.

🚀 Core Features
Feature	Description
📄 PDF & Docs Q&A	Upload study notes or research papers and ask contextual questions.
🧠 Summarization	Generate concise summaries, outlines, or key points.
🖼️ OCR Extraction	Extract and understand handwritten or printed notes from images.
🎥 YouTube Q&A	Extract video transcripts, translate (Hindi/English), summarize, and query.
💾 Persistent Memory	Save embeddings and chat history for continuous context.
💬 Interactive Chat UI	ChatGPT-like interface for document interaction.
🔍 RAG Pipeline	Ensures context-aware answers through document retrieval.
📚 Multi-document Support	Query across multiple PDFs or video sources.
🧱 Development Model

Iterative Incremental Model — The system is developed in working phases, where each increment adds a usable feature, and each iteration improves existing components.

Phase	Feature	Description
1️⃣	PDF Upload + Q&A	Upload → Extract → Embed → Query
2️⃣	Persistent Memory	Store embeddings + chat history
3️⃣	OCR Integration	Handle images with Tesseract
4️⃣	YouTube Summarizer	Transcript extraction + translation
5️⃣	Summarization & Notes	Auto-generate notes/key points
6️⃣	Chat UI Integration	Full React chat interface
🧰 Tech Stack
🧠 AI / NLP

LLMs: GPT-4o-mini / Ollama (Llama 3.1 / Mistral)

Framework: LangChain

Embeddings: text-embedding-3-small / Ollama Embeddings

💾 Database / Memory

Vector DB: Qdrant (Free Cloud Tier)

Chat Memory: SQLite

📄 Data Extraction

PDFs: PyMuPDF / pdfplumber

Images: pytesseract + PIL (OCR)

YouTube: youtube-transcript-api

Translation: googletrans

⚙️ Backend

Framework: FastAPI (Python)

RAG Framework: LangChain + Qdrant

Embeddings & LLM: OpenAI / Ollama API

💻 Frontend

Stack: React (Vite) + Tailwind CSS

Communication: Axios

☁️ Deployment

Backend: Render / Railway (FastAPI)

Frontend: Vercel

Vector DB: Qdrant Cloud

🏗️ System Architecture
React Frontend (Chat UI)
    │
    ▼
FastAPI Backend
 ├── Upload Handlers (PDF / Image / YouTube)
 ├── Extractors + Translators
 ├── Embedding Generator (OpenAI / Ollama)
 ├── Vector Store (Qdrant)
 ├── Retrieval + LLM (LangChain)
 ├── Memory (SQLite)
 └── REST APIs (Ask / Process)

📂 Folder Structure
klarity/
│
├── klarity-backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   ├── extractor.py         # Extract PDF/Image/YouTube text
│   │   ├── rag_pipeline.py      # LangChain RAG logic
│   │   ├── db.py                # Qdrant setup
│   │   ├── models.py            # Pydantic models for API
│   │   ├── utils.py             # Cleaning & preprocessing
│   │   └── routes/
│   │       ├── doc.py           # /process route
│   │       └── qa.py            # /ask route
│   ├── data/
│   │   ├── uploads/
│   │   ├── processed/
│   │   └── qdrant/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
└── klarity-frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   │   └── api.js
    │   └── App.jsx
    ├── package.json
    └── tailwind.config.js

🧠 RAG Pipeline (Core Logic)
Step	Description	Tool
1️⃣ Extraction	Extract text from PDFs, images, or YouTube	PyMuPDF, pytesseract, youtube-transcript-api
2️⃣ Cleaning	Clean, normalize, and structure extracted text	Regex, spaCy
3️⃣ Chunking	Split text into overlapping chunks	LangChain TextSplitter
4️⃣ Embedding	Convert chunks into vectors	OpenAI / Ollama Embeddings
5️⃣ Storage	Store embeddings for retrieval	Qdrant Vector DB
6️⃣ Retrieval	Fetch top-k relevant chunks per query	LangChain Retriever
7️⃣ Generation	Combine context + query → generate answer	LangChain RetrievalQA
8️⃣ Frontend Chat	Interactive chat experience	React + Tailwind
🎓 Learning Outcomes

Understanding RAG architecture and its real-world application.

Building a FastAPI-based GenAI backend integrated with LLMs.

Implementing vector databases (Qdrant) for knowledge retrieval.

Creating a multi-modal AI system (PDF, OCR, YouTube).

Deploying an end-to-end AI app with free-tier infrastructure.

🧩 Future Enhancements
Feature	Description
🧑‍💼 User Accounts	Login system with personalized memory
🧾 Export Summaries	Export notes or Q&A as PDFs
🌐 Multi-source Context	Combine answers across PDFs, images, and videos
🤖 AI Workflow	Integrate n8n / LangGraph for automation
☁️ Cloud Sync	Persistent embeddings and history per user
⚙️ Software Requirements
Category	Requirements
Backend	Python 3.10+, FastAPI, LangChain, Qdrant-client
Frontend	Node.js 18+, React + Vite, Tailwind CSS
Database	Qdrant (Cloud or Local), SQLite
AI APIs	OpenAI / Ollama
Environment	VS Code, Docker (optional), Git
💻 Hardware Requirements
Component	Minimum	Recommended
CPU	Dual-core	Quad-core i5+
RAM	8 GB	16 GB
Storage	5 GB	10+ GB
GPU (Optional)	For Ollama / Local LLMs	NVIDIA CUDA-enabled
🧭 Example Flow

User: “What is the KDD process?”
System Flow:

Extract text from uploaded PDF.

Clean & split text into chunks.

Generate embeddings and store in Qdrant.

Retrieve relevant chunks for the query.

Send to LLM with context.

Return a clear, context-rich answer.

🧱 Deployment Plan
Component	Platform
Backend	Render / Railway
Frontend	Vercel
Vector DB	Qdrant Cloud
Auth (Future)	Supabase / Firebase
🧩 License

This project is open source under the MIT License.