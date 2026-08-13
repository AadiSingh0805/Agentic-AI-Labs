# DeterministicDSTutor 🎓

A rule-based, deterministic tutoring agent for Core Data Science concepts built with Streamlit, SQLite, and Google Gemini API (`gemini-1.5-flash-latest`).

Unlike standard LLM chatbots that hallucinate or generate free-form responses, **DeterministicDSTutor** uses Gemini **exclusively as a phrasing engine** for pre-approved template data. 

### Key Optimizations
1. **Prompt Optimization:** System prompts are strictly constrained and shortened to ensure formatting compliance and reduce token overhead.
2. **Intent Classification:** The system uses a rule-based classifier to identify the student's exact learning objective (Definition, Code, Complexity, Algorithm, etc.) before calling the LLM, slicing the knowledge base to send only relevant data.

---

## 🚀 Setup & Installation

### 1. Requirements
- Python 3.11 or higher (Conda recommended)
- Google Gemini API Key 

### 2. Environment Setup

```bash
# Create and activate Conda environment
conda create -n dstutor python=3.11
conda activate dstutor

# Install dependencies
pip install -r requirements.txt