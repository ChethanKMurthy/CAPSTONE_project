import streamlit as st
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import json                     # <-- NEW GRAPHING IMPORT
import pandas as pd             # <-- NEW GRAPHING IMPORT
import altair as alt            # <-- NEW GRAPHING IMPORT

# --- Configuration ---
CHROMA_DB_DIR = "chroma_db"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
LLM_MODEL = "llama3.2:3b" 

# --- App UI ---
st.set_page_config(page_title="ESG Consultant AI", layout="wide")
st.title("🤖 Advanced ESG Consultant AI")
st.markdown("""
This AI consultant can generate a high-level compliance report for your company.
1.  Enter your industry.
2.  Ask the AI to "generate a compliance report" or ask a specific question.
""")

industry = st.text_input("Enter Your Industry (e.g., Technology, Manufacturing, Energy)", "Technology")

# --- RAG Chain Setup ---
try:
    llm = Ollama(model=LLM_MODEL)
    embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR, 
        embedding_function=embedding_function
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    print(f"Successfully connected to Ollama ({LLM_MODEL}) and loaded Chroma DB.")
except Exception as e:
    st.error(f"Failed to initialize. Did you run ingest.py? Is Ollama running?")
    st.error(f"Error: {e}")
    st.stop()

# --- 1. Prompt for "Common Industry Risks" (External Knowledge) ---
industry_risk_prompt = PromptTemplate.from_template(
    """You are an expert ESG analyst. List the top 5 most common ESG violations or risks for the '{industry}' industry. Be concise. Use a numbered list."""
)

# --- 2. Prompt for "Compliance Report" (Synthesizer) ---
compliance_report_prompt = PromptTemplate.from_template(
    """
### Instruction:
You are an expert ESG (Environmental, Social, and Governance) consultant. 
Your task is to generate a high-level compliance report based on the user's request.

You must synthesize information from THREE sources:
1.  **"Common Industry Risks"**: This is general knowledge about the company's industry.
2.  **"Company's Documents"**: This is the specific context retrieved from the company's internal PDFs.
3.  **"User's Request"**: The specific question the user wants you to answer.

---

### 1. Common Industry Risks (from your general knowledge):
{industry_context}

---

### 2. Company's Documents (Internal RAG Context):
{company_context}

---

### 3. User's Request:
{user_question}

---

### Your Expert Compliance Report:
Based *only* on the information provided above, generate a structured report.

**CRITICAL TASK:**
1.  First, clearly list the **"Common Industry Risks"**.
2.  For each risk, analyze the **"Company's Documents"** to find evidence of how the company is addressing that specific risk.
3.  **Identify and highlight the gaps.** If the company's documents do not mention a policy for a common industry risk, you MUST state that "No specific information was found in the documents regarding [Risk]."
4.  Conclude with a "Recommendations" section, suggesting the company develop policies for the identified gaps.
5.  **Do not** make up information about the company. Stick strictly to the provided document context.

**Report:**
"""
)

# --- 3. ### NEW GRAPH GENERATION PROMPT ### ---
# This new prompt will be used to generate data for our chart.
graph_prompt_template = """
You are a data visualization analyst. Your task is to read the following ESG compliance report and extract the key risks and their compliance levels.
Assign a "Compliance Score" from 0 (No policy mentioned) to 100 (Excellent, comprehensive policy found).

**RULES:**
1.  Identify the main ESG risks discussed (e.g., "Data Privacy", "E-Waste", "Supply Chain Labor").
2.  For each risk, read the analysis and assign a "Compliance Score".
3.  You MUST output *only* a valid JSON list of objects. Do not add any text before or after the JSON.

**Example Output:**
[
  {{"risk": "Data Privacy", "score": 75}},
  {{"risk": "E-Waste Management", "score": 20}},
  {{"risk": "Supply Chain Labor", "score": 0}}
]

**Report to Analyze:**
{report_text}

**Your JSON Output:**
"""
graph_prompt = PromptTemplate.from_template(graph_prompt_template)


# --- Helper Function ---
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- Define the Chains ---

# Chain 1: Gets the "Common Industry Risks"
chain_industry_risks = industry_risk_prompt | llm | StrOutputParser()

# Chain 2: The Final Report Chain
full_report_chain = (
    RunnablePassthrough.assign(
        industry_context=chain_industry_risks,
        company_context=lambda x: (retriever | format_docs).invoke(x["user_question"]),
        user_question=lambda x: x["user_question"]
    )
    | compliance_report_prompt
    | llm
    | StrOutputParser()
)

# Chain 3: ### NEW GRAPH GENERATION CHAIN ###
graph_generation_chain = graph_prompt | llm | StrOutputParser()


# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []
# ### NEW SESSION STATE FOR GRAPHING ###
if "last_report" not in st.session_state:
    st.session_state.last_report = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("Ask for a report (e.g., 'Generate our compliance report')"):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Generating compliance report... (This involves multiple steps)"):
            try:
                input_data = {
                    "industry": industry,
                    "user_question": user_question
                }
                response = full_report_chain.invoke(input_data)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                # ### NEW: Save the last report for graphing ###
                st.session_state.last_report = response
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
                print(f"Error details: {e}")

# ### NEW: "Generate Visual Summary" Button Logic ###
# This block will only execute if a report has been generated
if st.session_state.last_report:
    if st.button("Generate Visual Summary"):
        with st.spinner("Analyzing report and building graph..."):
            try:
                # 1. Call the new graph chain
                graph_json_string = graph_generation_chain.invoke({"report_text": st.session_state.last_report})
                
                # 2. Parse the JSON string
                # We wrap this in a try-except in case the LLM messes up the JSON format
                try:
                    graph_data = json.loads(graph_json_string)
                except json.JSONDecodeError:
                    st.error("Failed to decode the graph data from the LLM. The model may have returned an invalid JSON.")
                    print(f"Invalid JSON from LLM: {graph_json_string}")
                    st.stop()

                # 3. Convert data to Pandas DataFrame
                if not graph_data:
                    st.warning("The model could not extract any data to graph.")
                else:
                    df = pd.DataFrame(graph_data)
                    
                    # 4. Ensure correct columns
                    if 'risk' not in df.columns or 'score' not in df.columns:
                        st.error("The model's data was in the wrong format. Missing 'risk' or 'score' columns.")
                    else:
                        # 5. Create and display the Altair chart
                        st.subheader("Compliance Score Summary")
                        
                        chart = (
                            alt.Chart(df)
                            .mark_bar()
                            .encode(
                                x=alt.X("risk", title="ESG Risk Area"),
                                y=alt.Y("score", title="Compliance Score (0-100)"),
                                color=alt.Color("risk", legend=None),
                                tooltip=["risk", "score"],
                            )
                            .interactive()
                        )
                        st.altair_chart(chart, use_container_width=True)

            except Exception as e:
                st.error(f"An error occurred during graph generation: {e}")