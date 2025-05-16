# Travel Agent AI
A demo application of an AI travel assistant that helps users plan their perfect trip.
The user provides preferences (interests, budget, transport, number of days), and the assistant recommends destinations and generates a day-by-day travel itinerary.

## Built with
- LangChain  
- LangGraph  
- Qdrant  
- Streamlit  
- OpenAI API

## How to Run Locally
### 1. Clone the repository
### 2. Install dependencies (Poetry)
### 3. Create a .env file
In the project root, create a .env file with your credentials:  
- OPENAI_API_KEY=your_openai_key
- QDRANT_URL=your_qdrant_url
- DRANT_API_KEY=your_qdrant_key
- LANGSMITH_API_KEY=your_langsmith_key
- TAVILY_API_KEY=your_tavily_key
### 4. Initialize the Qdrant vector database
Before running the app, load data into the Qdrant vector store:  
poetry run python init_db.py
### 5. Start the application (Streamlit)
poetry run streamlit run agent_ai/app.py

## Requirements:
- Python 3.12  
- OpenAI API Key (GPT-4o, Embeddings)  
- Qdrant (local or cloud instance)  
- Poetry for environment management

## What this project demonstrates:
- Using LangGraph to manage AI agent workflow  
- Retrieval Augmented Generation (RAG) with Qdrant vector database  
- Function calling (recommend_destinations, suggest_budget, etc.)  
- User interface in Streamlit (form + chat interaction)