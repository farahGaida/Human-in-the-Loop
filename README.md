# CV Information Extraction - Human-in-the-Loop

This project implements a complete **Human-in-the-Loop (HITL)** pipeline designed to extract structured data from resumes (CVs). It bridges the gap between raw AI predictions and high-quality verified data.

## 🏗️ System Architecture
The system uses a **Hybrid Extraction Strategy**:
- **spaCy (NER)**: Extracts complex entities like Names and Organizations.
- **Regex**: Deterministic extraction for Emails, Phone numbers, and Section detection (Experience/Education).
- **HITL Interface**: A React-based UI where humans review, correct, and validate AI output.
- **Monitoring**: A real-time MLOps dashboard tracking annotation speed and model confidence.



## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy (SQLite), spaCy.
- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons, React Router.
- **Data Engineering**: DVC (Data Version Control) for tracking datasets.

## 📂 Project Structure
- `/backend`: FastAPI server and database logic.
- `/frontend`: React dashboard and annotation tool.
- `/ml`: Extraction scripts and NLP models.
- `/data`: Raw and processed CV data (tracked by DVC).

##  Getting Started

### Prerequisites
- Python 3.9+
- Node.js & npm

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/farahgaida/Human-in-the-Loop.git
   cd Human-in-the-Loop
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
  
3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📊 MLOps Key Performance Indicators (KPIs)
The dashboard tracks:

Throughput: Total CVs processed.

   - **Human Effort:** Average time spent per correction (seconds).

   - **AI Confidence:** Percentage of "Auto-accepted" files (where AI = Human).

   - **Data Growth:** Progress bar towards the next model retraining cycle.



