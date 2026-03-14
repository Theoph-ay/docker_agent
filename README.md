# Docker & FastAPI AI Agent

This project is an AI-powered email and research assistant agent, built with **FastAPI**, **LangGraph**, **LangChain**, and **Docker**. 

It was initially inspired by the [CodingForEntrepreneurs Tutorial: Building an agent with Docker and FastAPI](https://www.youtube.com/watch?v=KC8HT0eWSGk&list=PPSV&t=2720s), but has been **significantly expanded** with a custom frontend, persistent chat history, and chat search functionality.

---

## ✨ Key Features Added

- **Interactive UI / Frontend:** A beautifully designed, responsive chat interface built with HTML/CSS/JS and served directly from the backend.
- **Chat History:** Persistent storage of conversations using PostgreSQL and SQLModel.
- **Search Functionality:** Easily search and filter through previous chat sessions directly from the UI sidebar.
- **Multimodal AI Agents (LangGraph):** Uses a Supervisor architecture delegating work to an **Email Agent** (for sending/reading emails) and a **Research Agent**.
- **Dockerized Environment:** Simple, one-command setup using Docker Compose running both the FastAPI backend and a PostgreSQL database.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13, FastAPI, Uvicorn
- **AI & LLMs:** LangChain, LangGraph (Supervisor, prebuilt react agents), LangChain-Groq
- **Database:** PostgreSQL, SQLModel, Psycopg
- **Frontend:** Vanilla HTML, CSS, JavaScript (Fetch API)
- **Deployment:** Docker, Docker Compose

---

## 🚀 Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed.
- API keys for LangChain, Groq, and your specific email provider.

### Installation & Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Theoph-ay/docker_agent.git
   cd docker_agent
   ```
   
2. **Environment Variables:**
   Copy the `.env.sampl-db` to a new `.env` file and fill in your necessary keys:
   ```bash
   cp .env.sampl-db backend/.env
   # Make sure to provide your GROQ_API_KEY and PostgreSQL credentials.
   ```

3. **Run with Docker Compose:**
   Start the application and the database using Docker Compose from the root directory:
   ```bash
   docker compose up --watch --build
   ```

4. **Access the Application:**
   Open your browser and navigate to the frontend at:
   [http://localhost:8080](http://localhost:8080) (or `http://localhost:8000` depending on port mappings).

---

## 🧠 Architecture Overview

- **Supervisor Agent:** Orchestrates tasks and delegates them to specialized sub-agents.
- **Email Agent:** Capable of reading unread emails and sending outbound emails (`send_mail`, `get_unread_emails`).
- **Research Agent:** Performs background research to supplement user queries (`research_email`).

## 🤝 Acknowledgements
- Base agent configuration and Docker setup inspired by [CodingForEntrepreneurs](https://www.youtube.com/c/CodingEntrepreneurs).
- **Custom Additions:** The UI, dynamic chat retrieval, UI search filter, and stateful DB history were custom-built on top of the base tutorial foundation.
