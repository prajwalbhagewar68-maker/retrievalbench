from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from retrievalbench.chunking import chunk_documents
from retrievalbench.ingestion import load_text_documents, validate_documents
from retrievalbench.retrieval import available_retrievers

st.set_page_config(page_title="RetrievalBench", page_icon="🔎", layout="wide")
st.title("🔎 RetrievalBench")
st.caption("A reproducible workbench for comparing document retrieval methods.")

data_dir = ROOT / "data" / "sample_docs"
try:
    docs = validate_documents(load_text_documents(data_dir))
    chunks = chunk_documents(docs, chunk_words=120, overlap_words=20)
    retrievers = available_retrievers(chunks)
except Exception as exc:
    st.error(f"Could not load sample documents: {exc}")
    st.stop()

st.sidebar.header("Search settings")
method = st.sidebar.selectbox("Retrieval method", list(retrievers.keys()))
top_k = st.sidebar.slider("Top K", min_value=1, max_value=10, value=5)
query = st.text_input("Ask a question about the sample documents", placeholder="How does BM25 rank documents?")

if query:
    results = retrievers[method].search(query, top_k=top_k)
    if not results:
        st.warning("No matching passages found. Try different wording.")
    for rank, result in enumerate(results, start=1):
        with st.expander(f'{rank}. {result["title"]} · score {result["score"]:.4f}', expanded=(rank == 1)):
            st.write(result["text"])
            st.caption(f'Source: {result["source"]} | Document: {result["doc_id"]} | Chunk: {result["chunk_id"]}')

st.divider()
st.subheader("Included sample corpus")
st.write(f"{len(docs)} documents · {len(chunks)} chunks · {len(retrievers)} retrieval methods")
st.info("This starter version evaluates retrieval and citation references. It does not yet generate answers or prove semantic claim support.")
