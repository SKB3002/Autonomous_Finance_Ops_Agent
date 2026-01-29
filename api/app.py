import streamlit as st
from graph.graph import financeops_graph
import uuid

st.set_page_config(page_title="Autonomous FinanceOps Agent")

st.title("🧠 Autonomous FinanceOps Agent")

user_query = st.text_input("Ask a finance operations question")

uploaded_file = st.file_uploader(
    "Upload invoice / CSV (optional)",
    type=["pdf", "csv"]
)

persist_document = st.checkbox("Store this document in long-term memory")

run = st.button("Run Agent")

if run and user_query:
    initial_state = {
        "run_id": str(uuid.uuid4()),
        "input_type": "text",
        "user_query": user_query,
        "uploaded_file": None,
        "persist_document": persist_document,
        "requires_live_data": False,
        "db_write_requested": False,
        "db_write_confirmed": False,
        "extracted": False,
        "web_verified": False,
        "db_verified": False,
        "charts_generated": False,
        "validation_result": None,
        "decision": None,
        "confidence_score": None,
        "escalation_required": False,
    }

    if uploaded_file:
        file_path = f"/tmp/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        initial_state["uploaded_file"] = file_path

    result = financeops_graph.invoke(initial_state)

    st.subheader("Decision")
    st.write(result["decision"])

    st.subheader("Confidence Score")
    st.write(result["confidence_score"])

    st.subheader("Escalation Required")
    st.write(result["escalation_required"])

    if result["charts_generated"]:
        st.subheader("Generated Charts")
        st.image("charts", use_column_width=True)

    st.subheader("Full State")
    st.json(result)
