🧠 EduAI Knowledge Assistant

“An intelligent assistant that understands your study material — upload PDFs, Docs, Images, or YouTube links and ask anything!”

🎯 Project Overview

Purpose:
To build an AI-powered study assistant that answers questions, summarizes notes, and extracts insights from documents, images, and videos using Retrieval-Augmented Generation (RAG).

Goal:
Help students and learners query their own study material and get precise answers, summaries, and concepts — anytime, anywhere.

🚀 Key Features

📄 PDF & Docs Q&A – Upload documents, ask questions, get accurate answers.

🧠 Summarization – Generate concise summaries or key points.

🖼️ OCR Extraction – Extract and understand text from images.

🎥 YouTube Q&A – Extract transcripts, summarize, and answer questions (supports Hindi via translation).

💾 Persistent Memory – Stores embeddings and chat history for future sessions.

💬 Chat Interface – ChatGPT-like UI built with React.

🔍 RAG Pipeline – Retrieval-Augmented Generation ensures context-based answers.

🧰 Multi-document Support – Handle multiple PDFs and sources.

🧱 Development Model: Incremental Model

The system is built phase by phase, where each increment adds a working feature.

Phase	Feature	Description
1️⃣	PDF Upload + Q&A	Upload PDF → Extract text → Embed → Query
2️⃣	Persistent Vector DB + Chat Memory	Store embeddings + chat history
3️⃣	OCR Integration	Extract text from images
4️⃣	YouTube Summarizer	Get transcript, translate, summarize
5️⃣	Summaries + Notes	Generate key points and notes
6️⃣	Full Chat UI	Chat interface with history and context
🧰 Tech Stack
🧠 AI / NLP

OpenAI GPT-4o-mini / Gemini Flash – LLM for Q&A and summarization

text-embedding-3-small – Vector embeddings

LangChain – Build RAG pipeline

💾 Data / Storage

ChromaDB – Vector database for embeddings

SQLite – Chat history & persistence

📄 Extraction Tools

PyMuPDF / pdfplumber – Extract text from PDFs

pytesseract + PIL – OCR for images

youtube-transcript-api – Extract transcripts

googletrans – Translate Hindi transcripts

⚙️ Backend

Flask (Python) – API backend

LangChain + OpenAI SDK – Embedding + LLM calls

💻 Frontend

React (Vite) – UI

Tailwind CSS – Styling

Axios – API communication

🏗️ System Architecture
React Frontend (Chat UI)
    │
    ▼
Flask Backend
 ├── Upload Handlers (PDF / Image / YouTube)
 ├── Text Extractors + Translators
 ├── Embedding Generator (OpenAI)
 ├── Vector Store (ChromaDB)
 ├── Retrieval + LLM (LangChain)
 ├── Memory (SQLite)
 └── REST APIs

📂 Folder Structure
🔹 Frontend (React)
eduai-frontend/
├── src/
│   ├── components/
│   │   ├── ChatBox.jsx
│   │   ├── FileUploader.jsx
│   │   └── MessageBubble.jsx
│   ├── pages/
│   │   └── Home.jsx
│   ├── services/
│   │   └── api.js
│   └── App.jsx
└── package.json

🔹 Backend (Flask)
eduai-backend/
├── app.py
├── routes/
│   ├── upload_routes.py
│   ├── query_routes.py
│   └── youtube_routes.py
├── utils/
│   ├── pdf_handler.py
│   ├── ocr_handler.py
│   ├── yt_handler.py
│   ├── rag_pipeline.py
│   └── db.py
├── vector_store/
├── chat_memory.db
└── requirements.txt

🧭 Phase-Wise Roadmap
📍 Phase 1: Core RAG System

Upload PDF

Extract text

Chunk + embed

Store in Chroma

Query with context

Answer via GPT-4o-mini
✅ Deliverable: Working Q&A for PDFs

📍 Phase 2: Persistence + Chat Memory

Save embeddings permanently

Add SQLite-based memory
✅ Deliverable: Conversations remain available across sessions

📍 Phase 3: OCR Support

Upload image

Extract text via Tesseract

Embed + query
✅ Deliverable: Q&A from image-based notes

📍 Phase 4: YouTube Integration

Input YouTube URL

Extract transcript

Translate Hindi → English

Summarize + Q&A
✅ Deliverable: Summarizer + Q&A from video

📍 Phase 5: Summarization & Notes

Generate study notes

Summarize chapters
✅ Deliverable: Summaries + key concepts

📍 Phase 6: Chat UI Integration

React Chat Interface

File upload support

Show conversation history
✅ Deliverable: Fully interactive chat assistant

🧠 How It Works (Example Flow)

User: Uploads PDF → Asks “What is KDD process?”
System:

Extracts PDF text

Splits into chunks

Generates embeddings

Stores in ChromaDB

Retrieves relevant chunks

Sends to LLM with context

Returns precise answer

🎓 Learning Outcomes

🔍 Understanding of RAG architecture

⚙️ Integration of AI APIs with backend

💻 Frontend-Backend communication

💾 Persistent vector database usage

🧠 Multi-modal data handling (PDF, Image, Video)

🧩 Future Enhancements

🧑‍💼 User accounts + cloud sync

📚 Multi-source context blending

🧾 Export summaries as PDFs

🌐 Deployment on Render / Vercel

