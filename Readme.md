# Klarity – AI Powered Document Intelligence System

Klarity is an AI-powered document interaction system that allows users to upload PDF documents and ask questions in natural language.  
The system retrieves relevant information from the uploaded documents and generates accurate answers using a Retrieval-Augmented Generation (RAG) pipeline.

The goal of Klarity is to simplify document understanding by enabling conversational interaction with large study materials, technical documents, and notes.

---

# Problem Statement

Large documents such as textbooks, lecture notes, and technical manuals are difficult to navigate manually.

Traditional document readers only support keyword search, which:
- does not understand context
- cannot summarize information
- requires manual scanning of multiple pages

General AI chatbots also struggle because they:
- rely on pretrained knowledge
- do not understand user-specific documents
- may produce hallucinated responses

Klarity solves this problem by grounding AI responses directly in uploaded documents.

---

# Solution

Klarity uses **Retrieval-Augmented Generation (RAG)** to combine semantic document search with a large language model.

Instead of letting the AI guess answers, Klarity:

1. Extracts text from uploaded documents  
2. Splits the content into smaller semantic chunks  
3. Converts chunks into vector embeddings  
4. Stores embeddings in a vector database  
5. Retrieves the most relevant chunks for each query  
6. Sends the retrieved context to the LLM to generate an answer

This ensures answers are **document-grounded, relevant, and reliable**.

---

# Key Features

- Upload and analyze PDF documents
- Natural language question answering
- Document-grounded responses
- Multi-chat session support
- Persistent chat history
- Document summary generation
- Semantic document search
- Chat-level document isolation
- Smart Summary Creation
---

# System Architecture

The system follows a **client-server architecture** with a modular backend.

Frontend  
→ sends user queries and document uploads  

Backend (FastAPI)  
→ handles document processing and query logic  

Vector Database (Qdrant)  
→ stores document embeddings  

LLM (Gemini)  
→ generates answers using retrieved context

Pipeline:

User Query  
→ Query Embedding  
→ Vector Search  
→ Context Retrieval  
→ LLM Response Generation

---

# Technology Stack

## Backend
- Python
- FastAPI

## Frontend
- React
- Tailwind CSS

## AI & NLP
- Retrieval-Augmented Generation (RAG)
- Gemini LLM
- Nomic Embedding Model

## Databases
- SQLite (chat metadata)
- Qdrant (vector embeddings)

## Document Processing
- LangChain text splitting
- Custom chunking pipeline

---

# Implementation Highlights

### Document Processing Pipeline
The system extracts document text and processes it through multiple stages:

Extraction  
→ Cleaning  
→ Chunking  
→ Embedding  
→ Vector Storage

This ensures efficient semantic retrieval.

### Semantic Search
Instead of keyword matching, Klarity uses vector embeddings to identify semantically relevant document chunks.

### Chat-Based Interaction
Users interact with documents through a conversational interface, making document exploration intuitive.

### Context-Aware Responses
Only retrieved document chunks are passed to the LLM, reducing hallucination and improving answer reliability.

---

# Challenges and Engineering Decisions

### Chunking Strategy
Proper chunking was required to ensure that definitions and context remained together during retrieval.

### Prompt Engineering
The system uses structured prompts to ensure answers are grounded in document context and formatted clearly.

### Retrieval Optimization
Top-k vector search is used to retrieve the most relevant document segments for each query.

---

# Use Cases

- Study material exploration
- Technical documentation search
- Research paper analysis
- Educational learning assistant
- Knowledge base interaction

---

# Future Improvements

- Support for additional file formats (DOCX, images)
- OCR for scanned documents
- User authentication
- Cloud deployment
- Flashcards and quiz generation
- Voice-based interaction

---

# Project Status

Academic project completed as part of a final year software engineering project.