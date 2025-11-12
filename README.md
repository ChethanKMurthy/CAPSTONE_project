



# 🤖 Advanced ESG Consultant AI

This is an AI-powered web application that acts as an expert ESG (Environmental, Social, and Governance) consultant.

Unlike a simple Q\&A bot, this tool performs an advanced, multi-step analysis. It leverages a local Large Language Model (LLM) to compare general, industry-wide ESG risks against the specific policies and data found in your company's internal documents.

The application then generates a "Compliance Gap Analysis" report, identifies areas where your company's documentation is silent, and provides actionable recommendations. Finally, it can instantly generate a visual summary of its findings.

## ✨ Key Features

* **Automated Compliance Gap Analysis:** Generates a report that compares your company's policies (from your PDFs) against common industry risks.
* **Intelligent RAG:** Uses Retrieval-Augmented Generation (RAG) to ground all answers in your specific documents.
* **Dynamic Visualizations:** Generates bar charts on the fly to provide a visual summary of compliance levels for different risk areas.
* **Industry-Specific Risk Analysis:** Uses the LLM's external knowledge to identify common violations for any industry you specify (e.g., "Technology", "Manufacturing").
* **100% Local \& Private:** Runs entirely on your local machine using Ollama, ensuring your sensitive ESG documents are never sent to a third-party server.

---

## 🛠️ Tools \& Technologies

This project is built with a modern, all-Python stack:


| Category | Tool | Description |
| :-- | :-- | :-- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white) | Core application language. |
| **Web Framework** | ![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit&logoColor=white) | Used to create the interactive web interface. |
| **AI Framework** | ![LangChain](https://img.shields.io/badge/LangChain-AI_Orchestration-green?logo=langchain&logoColor=white) | Used to build the multi-step RAG and agentic chains. |
| **LLM Serving** | ![Ollama](https://img.shields.io/badge/Ollama-Local_LLMs-lightgrey) | Serves the `llama3.2:3b` model locally. |
| **Vector Database** | ![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-blueviolet) | Stores and retrieves document embeddings. |
| **Embeddings** | ![HuggingFace](https://img.shields.io/badge/SentenceTransformers-Embeddings-yellow?logo=huggingface&logoColor=white) | Generates vector embeddings for your documents. |
| **Data \& Graphing** | ![Pandas](https://img.shields.io/badge/Pandas-Data_Handling-blue?logo=pandas&logoColor=white) \& ![Altair](https://img.shields.io/badge/Altair-Visualization-orange) | Used to parse LLM-generated JSON and create charts. |


---

## 📂 Project Structure

Here is a breakdown of the key files and what they do:

esg_consultant/
|
|-- docs/
| |-- (Place your PDFs here, e.g., 'esg_report_2024.pdf')
|
|-- app.py
|  The main Streamlit web application.
|  This file runs the UI, handles user queries, coordinates the multi-step
|  LLM chains, and renders the final report and graphs.
|
|-- ingest.py
|  A one-time setup script.
|  It reads all PDFs from the /docs folder, splits them into chunks,
|  generates embeddings, and saves them to the local ChromaDB.
|
|-- requirements.txt
|  A list of all necessary Python packages for the project.
|
|-- chroma_db/
| (This folder is created automatically after running ingest.py)
| This is the persistent local vector database.

---

## 🚀 How to Run the Application

Follow these steps to get the application running on your local machine.

### Prerequisites

1. **Python:** You must have Python 3.9 or newer installed.
2. **Ollama:** You must have [Ollama](https://ollama.com/) installed and running.

### Step 1: Clone the Repository

Clone this project to your local machine:

```bash
git clone https://your-repo-url/esg_consultant.git
cd esg_consultant
```


Step 2: Set Up a Virtual Environment & Install Dependencies

Create and activate a virtual environment to keep your dependencies isolated:
Bash
# Create the environment
```python -m venv venv```

# Activate it
# On macOS/Linux:
```source venv/bin/activate```
# On Windows:
```.\venv\Scripts\activate```

# Install all required packages
```pip install -r requirements.txt```


Step 3: Download the LLM

In your terminal, pull the llama3.2:3b model. This only needs to be done once.
```ollama pull llama3.2:3b```

(Make sure the Ollama application is running while you do this.)

Step 4: Add Your ESG Documents

Place all your company's PDF files (ESG reports, compliance policies, etc.) into the docs/ folder.

Step 5: Ingest Your Data

This is a one-time step to "teach" the AI your documents. If you add new PDFs later, you will need to run this script again.
```python ingest.py```

This script will process all the files in the docs/ folder and create a new chroma_db/ directory.

Step 6: Run the Web App!

You are now ready to launch the application.
```streamlit run app.py```

Streamlit will automatically open the application in your default web browser (usually at http://localhost:8501).

💡 How to Use the App

Enter Your Industry: Type your company's industry (e.g., "Technology", "Manufacturing") into the text box at the top.
Generate a Report: In the chat box, type a request like:
Generate a compliance gap analysis for our company.
What are our biggest risks and how are we handling them?
Create a compliance report.
View Report: The AI will generate a detailed report, identifying industry risks and checking them against your documents.
Visualize: After the report appears, click the "Generate Visual Summary" button. The AI will analyze its own report, extract compliance scores, and generate a bar chart for a quick visual overview.

🔮 Future Work & Contributions

This project is a powerful proof-of-concept. Here are some ways it could be improved:
Advanced Prompt Engineering: The prompts can be further optimized for different models or tasks (e.g., a dedicated prompt for llama3.2:3b's specific chat template).
Robust JSON Parsing: The graph generation relies on the LLM outputting perfect JSON. A more robust solution would use LangChain's Pydantic output parsers to guarantee the JSON structure and handle errors.
Docker Deployment: Containerize the application (Streamlit app, Ollama server, and vector DB) using Docker for one-click deployment.
More Visualizations: Expand the visual summary to include pie charts for risk distribution, time-series analysis (if dates are in the docs), or a compliance "heat map."
Authentication: Add a simple authentication layer (e.g., Streamlit's st.secrets) to protect access to the consultant.
Feedback Mechanism: Add a "thumbs up/down" button to log and review the AI's responses, allowing for continuous improvement.
Contributions and ideas are welcome!


## 🛠️ Tools & Technologies

This project is built with a modern, all-Python stack:

| Category | Tool | Description |
| :--- | :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white) | Core application language. |
| **Web Framework** | ![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit&logoColor=white) | Used to create the interactive web interface. |
| **AI Framework** | ![LangChain](https://img.shields.io/badge/LangChain-AI_Orchestration-green?logo=langchain&logoColor=white) | Used to build the multi-step RAG and agentic chains. |
| **LLM Serving** | ![Ollama](https://img.shields.io/badge/Ollama-Local_LLMs-lightgrey) | Serves the `llama3.2:3b` model locally. |
| **Vector Database** | ![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-blueviolet) | Stores and retrieves document embeddings. |
| **Embeddings** | ![HuggingFace](https://img.shields.io/badge/SentenceTransformers-Embeddings-yellow?logo=huggingface&logoColor=white) | Generates vector embeddings for your documents. |
| **Data & Graphing** | ![Pandas](https://img.shields.io/badge/Pandas-Data_Handling-blue?logo=pandas&logoColor=white) & ![Altair](https://img.shields.io/badge/Altair-Visualization-orange) | Used to parse LLM-generated JSON and create charts. |

---

## 📂 Project Structure

Here is a breakdown of the key files and what they do:

```

esg_consultant/
|
|-- docs/
| |-- (Place your PDFs here, e.g., 'esg_report_2024.pdf')
|
|-- app.py
| \# The main Streamlit web application.
| \# This file runs the UI, handles user queries, coordinates the multi-step
| \# LLM chains, and renders the final report and graphs.
|
|-- ingest.py
| \# A one-time setup script.
| \# It reads all PDFs from the /docs folder, splits them into chunks,
| \# generates embeddings, and saves them to the local ChromaDB.
|
|-- requirements.txt
| \# A list of all necessary Python packages for the project.
|
|-- chroma_db/
| \# (This folder is created automatically after running ingest.py)
| \# This is the persistent local vector database.

```

---

## 🚀 How to Run the Application

Follow these steps to get the application running on your local machine.

### Prerequisites

1.  **Python:** You must have Python 3.9 or newer installed.
2.  **Ollama:** You must have [Ollama](https://ollama.com/) installed and running.

### Step 1: Clone the Repository

Clone this project to your local machine:

```

git clone https://your-repo-url/esg_consultant.git
cd esg_consultant

```

### Step 2: Set Up a Virtual Environment & Install Dependencies

Create and activate a virtual environment to keep your dependencies isolated:

```


# Create the environment

python -m venv venv

# Activate it

# On macOS/Linux:

source venv/bin/activate

# On Windows:

.\venv\Scripts\activate

# Install all required packages

pip install -r requirements.txt

```

### Step 3: Download the LLM

In your terminal, pull the llama3.2:3b model. This only needs to be done once.

```

ollama pull llama3.2:3b

```

(Make sure the Ollama application is running while you do this.)

### Step 4: Add Your ESG Documents

Place all your company's PDF files (ESG reports, compliance policies, etc.) into the `docs/` folder.

### Step 5: Ingest Your Data

This is a one-time step to "teach" the AI your documents. If you add new PDFs later, you will need to run this script again.

```

python ingest.py

```

This script will process all the files in the `docs/` folder and create a new `chroma_db/` directory.

### Step 6: Run the Web App!

You are now ready to launch the application.

```

streamlit run app.py

```

Streamlit will automatically open the application in your default web browser (usually at http://localhost:8501).

---

## 💡 How to Use the App

- **Enter Your Industry:** Type your company's industry (e.g., "Technology", "Manufacturing") into the text box at the top.
- **Generate a Report:** In the chat box, type a request like:
  - Generate a compliance gap analysis for our company.
  - What are our biggest risks and how are we handling them?
  - Create a compliance report.
- **View Report:** The AI will generate a detailed report, identifying industry risks and checking them against your documents.
- **Visualize:** After the report appears, click the "Generate Visual Summary" button. The AI will analyze its own report, extract compliance scores, and generate a bar chart for a quick visual overview.

---

## 🔮 Future Work & Contributions

This project is a powerful proof-of-concept. Here are some ways it could be improved:

* Advanced Prompt Engineering: The prompts can be further optimized for different models or tasks (e.g., a dedicated prompt for llama3.2:3b's specific chat template).
* Robust JSON Parsing: The graph generation relies on the LLM outputting perfect JSON. A more robust solution would use LangChain's Pydantic output parsers to guarantee the JSON structure and handle errors.
* Docker Deployment: Containerize the application (Streamlit app, Ollama server, and vector DB) using Docker for one-click deployment.
* More Visualizations: Expand the visual summary to include pie charts for risk distribution, time-series analysis (if dates are in the docs), or a compliance "heat map."
* Authentication: Add a simple authentication layer (e.g., Streamlit's st.secrets) to protect access to the consultant.
* Feedback Mechanism: Add a "thumbs up/down" button to log and review the AI's responses, allowing for continuous improvement.

Contributions and ideas are welcome!
```


