# 📜 Legal Contract Analyzer API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)

A backend REST API built with **FastAPI**, **MongoDB**, **Docker**, and **Google Gemini LLM**. This application automates legal document processing by parsing `.pdf` and `.txt` contracts, storing metadata in MongoDB, and performing structured AI analysis to extract executive summaries, clause breakdowns, risk flag classifications, and recommendations.

---

## 🖼️ API Interface Overview

<!-- PLACEHOLDER: Replace the path below with your uploaded Swagger screenshot -->
![Swagger UI Screenshot](./assets/swagger-ui.png)

---

## ✨ Key Features

* **Document Upload & Parsing**: Upload `.pdf` and `.txt` contracts with file validation and local disk storage.
* **Metadata Extraction**: Extracts word counts, page counts, and metadata using `PyPDF2`.
* **AI Analysis Pipeline**: Integrates Google Gemini (`gemini-3.8-flash`) via REST API calls with strict JSON output schemas.
* **Risk Flag & Clause Extraction**: Identifies high-risk legal clauses and normalizes risk ratings (`LOW`, `MEDIUM`, `HIGH`).
* **Complete CRUD & Query Options**: Fetch contracts, individual analyses, or all analyses associated with a specific contract ID.
* **Fully Containerized**: Ready-to-use `Dockerfile` and `docker-compose.yaml` setup linking FastAPI and MongoDB.

---

## 🛠️ Tech Stack

* **Framework**: FastAPI, Pydantic v2, Uvicorn
* **Database**: MongoDB, PyMongo
* **AI Model**: Google Gemini API
* **Document Parsing**: PyPDF2
* **Containerization**: Docker, Docker Compose
* **Environment Configuration**: `python-dotenv`

---

## 📂 Project Structure

```text
legal-contract-analyzer/
│
├── app/
│   ├── routes/
│   │   ├── analysis.py          # AI analysis triggers & retrieval routes
│   │   └── contracts.py         # Contract upload and metadata routes
│   │
│   ├── services/
│   │   ├── document_parser.py   # PDF and TXT text extraction logic
│   │   ├── gemini_analysis.py   # Gemini API REST integration & JSON parser
│   │   └── prompt.py            # Structured prompts for Gemini LLM
│   │
│   ├── uploads/                 # Storage directory for contract files
│   ├── config.py                # Environment variables & configuration
│   ├── database.py              # MongoDB client & collection initializations
│   ├── main.py                  # FastAPI application entrypoint
│   └── models.py                # Pydantic schemas & Enums
│
├── Dockerfile                   # Docker image instructions for FastAPI
├── docker-compose.yaml          # Multi-container orchestration (API + MongoDB)
├── requirements.txt             # Python project dependencies
├── .env.example                 # Environment variables template
└── .gitignore                   # Git ignore policies
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/legal-contract-analyzer.git
cd legal-contract-analyzer
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
MONGODB_URI=mongodb://root:mypassword@mongodb:27017/
GEMINI_API_KEY=AIzaSyYourActualGeminiAPIKeyHere
```

### 3. Run with Docker Compose (Recommended)

Start both the FastAPI backend and MongoDB container simultaneously:

```bash
docker compose up --build -d
```

Access the application at:

- **Interactive API Docs:** `http://localhost:8000/docs`
- **Root Health Check:** `http://localhost:8000/`

## 📖 API Endpoint Documentation

| **Category**  | **Method** | **Endpoint**                       | **Description**                                    |
| ------------- | ---------- | ---------------------------------- | -------------------------------------------------- |
| **Default**   | `GET`      | `/`                                | API health check and server info                   |
| **Contracts** | `POST`     | `/contracts/upload`                | Upload a new `.pdf` or `.txt` contract file        |
| **Contracts** | `GET`      | `/contracts/`                      | List all uploaded contracts                        |
| **Contracts** | `GET`      | `/contracts/{contract_id}`         | Retrieve details and text of a contract            |
| **Analysis**  | `POST`     | `/analysis/analyse/{contract_id}`  | Run Gemini AI analysis on a contract               |
| **Analysis**  | `GET`      | `/analysis/{analysis_id}`          | Retrieve a specific analysis report by ID          |
| **Analysis**  | `GET`      | `/analysis/contract/{contract_id}` | Retrieve all analysis reports for a given contract |

## 📊 Sample AI Result Response JSON

```json
{
  "id": "6702e84128f09d81d24c0d12",
  "contract_id": "6702e7b028f09d81d24c0d11",
  "analysis_date": "2026-10-06T15:43:26.123456",
  "summary": "This Non-Disclosure Agreement (NDA) establishes mutual confidentiality obligations between Party A and Party B for a duration of 24 months. It outlines restricted information use and governing jurisdiction.",
  "contract_type": "Non-Disclosure Agreement (NDA)",
  "key_clauses": [
    {
      "clause_title": "Confidentiality Term",
      "clause_text": "Obligations shall survive for a period of 2 years from the date of disclosure.",
      "explanation": "Confidentiality restrictions remain binding for two years after disclosure.",
      "is_standard": true
    },
    {
      "clause_title": "Governing Law",
      "clause_text": "This agreement shall be governed by the laws of California.",
      "explanation": "Specifies the legal jurisdiction governing the contract.",
      "is_standard": true
    }
  ],
  "risk_flags": [
    {
      "risk_title": "Uncapped Indemnification",
      "description": "Liability clause contains no monetary ceiling for breach damages.",
      "risk_level": "high",
      "recommendation": "Insert a maximum liability ceiling (e.g., $100,000 or total contract fee).",
      "clause_reference": "Section 8.2 (Indemnification)"
    }
  ],
  "overall_risk_level": "medium",
  "recommendations": [
    "Insert a maximum liability ceiling into Section 8.2.",
    "Include explicit exceptions for disclosures required by law or court order."
  ]
}
```

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
