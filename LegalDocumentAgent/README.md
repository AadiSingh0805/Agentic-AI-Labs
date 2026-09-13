# Experiment No. 4: Legal Document Intelligence and Retrieval System (Legal & Compliance Domain)

## 🏛️ Overview
This repository contains the complete Python implementation and benchmark suite for **Experiment No. 4: Legal Document Intelligence and Retrieval System**. The system ingests, cleans, chunks, embeds, and indexes legal contracts (PDF and DOCX), performs semantic and hybrid retrieval with FAISS vector indexing, applies relevance thresholding, enforces prompt-injection safeguards, generates strictly grounded responses with document/page citations, maintains persistent audit logs, and integrates advanced optimizations.

---

## 🏗️ Architecture & Retrieval Workflow

```
Legal Documents (PDF / DOCX)
          │
          ▼
Text Extraction & Cleaning (pypdf, python-docx, regex)
          │
          ▼
Sliding-Window Chunking & Metadata Binding
          │
          ▼
Dense Embedding Generation (Sentence-Transformers / Dense Vectorizer)
          │
          ▼
FAISS Vector Indexing (IndexFlatIP with L2-Normalized Vectors)
          │
          ▼
Structured Query Execution & Security Inspection (Prompt Injection Guard)
          │
          ▼
Semantic / Hybrid Retrieval (Reciprocal Rank Fusion RRF)
          │
          ▼
Relevance Filtering (Similarity >= 0.35 Threshold)
          │
          ▼
Context Augmentation & Deterministic Grounded Response Synthesis
          │
          ▼
Source Validation & Entity Grounding Check (PASS / REVIEW / FAIL)
          │
          ▼
Traceable Final Output & CSV Interaction Audit Logging
```

---

## 📁 Repository Structure
```
LegalDocumentAgent/
├── documents/                     # Generated PDF and DOCX legal contracts
│   ├── Vendor_Agreement.docx / .pdf
│   ├── Non_Disclosure_Agreement.docx / .pdf
│   ├── Master_Service_Agreement.docx / .pdf
│   └── Employment_Contract.docx / .pdf
├── vector_index/                  # FAISS binary vector index
│   └── faiss_index.bin
├── metadata/                      # Traceable chunk metadata store
│   └── chunk_metadata.json
├── logs/                          # Persistent interaction audit logs
│   ├── legal_retrieval_audit_log.csv
│   └── system.log
├── figures/                       # High-resolution academic B&W figures
│   ├── fig1_system_architecture.png
│   ├── fig2_retrieval_evaluation.png
│   └── fig3_optimizations_benchmark.png
├── legal_agent.py                 # Core legal intelligence agent implementation
├── generate_report_docx.py        # Publication-grade B&W DOCX report generator
├── Legal_Document_Intelligence_Report.docx  # Formal Experiment 4 Academic Report
└── README.md                      # Comprehensive documentation
```

---

## 🚀 Key Features & Implemented Steps

1. **Multi-Format Document Ingestion**: Ingests PDF and DOCX documents with automated page tracking.
2. **Text Normalization**: Strips excessive whitespace, resolves typography, normalizes line breaks.
3. **Sliding-Window Chunking**: Chunk size = 350 chars with 60-char overlap and metadata binding (`chunk_id`, `document`, `page`, `text`).
4. **Vector Embeddings & FAISS Indexing**: Normalized dense vector embeddings with FAISS `IndexFlatIP` inner-product search (exact Cosine Similarity).
5. **Standardized Query Contract**: Structured queries with `top_k`, `document_filter`, and `similarity_threshold`.
6. **Relevance Thresholding**: Rejects weak results below threshold (0.35) with safe refusal notices.
7. **Security Guard & Prompt-Injection Resistance**: Pre-retrieval pattern matching against prompt leaks, rule overrides, and out-of-domain abuse (100% security pass rate).
8. **Deterministic Grounding & Validation**: Formulates responses derived exclusively from context with automated entity grounding (`PASS`, `REVIEW`, `FAIL`) and confidence ratings (`HIGH`, `MEDIUM`, `LOW`).
9. **Exponential Backoff Retry**: 3-stage retry logic (1s, 2s, 4s) for recoverable transient failures.
10. **Persistent Audit Logging**: Detailed CSV log capturing timestamps, queries, filters, source references, scores, and execution traces.

---

## ⚙️ Selected Optimizations

### **Optimization 1 – Metadata-Filtered Retrieval vs. Unfiltered Search**
- **Objective**: Eliminates cross-contract ambiguity by scoping semantic retrieval to a specified document before vector ranking.
- **Result**: Delivers 100% target contract isolation, eliminating irrelevant clauses from other agreements.

### **Optimization 2 – Hybrid Retrieval (Keyword + Semantic with Reciprocal Rank Fusion)**
- **Objective**: Combines lexical term matching (BM25/TF-IDF) with dense semantic search using Reciprocal Rank Fusion (RRF).
- **Result**: Enhances retrieval for exact alphanumeric parameters, monetary values, and strict SLA definitions ($RRF\_Score(d) = \sum \frac{1}{60 + r_i}$).

### **Optimization 3 (Bonus) – Cross-Contract Clause Conflict Detection**
- **Objective**: Detects substantive term discrepancies (payment durations, termination notice periods, governing laws) across multiple agreements.

---

## 💻 How to Run

### 1. Run Full Legal Retrieval Pipeline & Evaluation Benchmarks:
```bash
python LegalDocumentAgent/legal_agent.py
```

### 2. Generate the Formal Black & White Times New Roman DOCX Report:
```bash
python LegalDocumentAgent/generate_report_docx.py
```

---

## 📊 Summary of Benchmark Results

| Evaluation Category | Benchmark Target | Measured Score | Status |
| :--- | :--- | :--- | :--- |
| **Legal Retrieval Accuracy** | Ground-truth top document & term match | **100.0%** | PASS |
| **Mean Cosine Similarity** | Average cosine score across 8 benchmark queries | **0.8484** | OPTIMAL |
| **Grounding Pass Rate** | Strict context support verification | **100.0%** | PASS |
| **Security Resilience** | Prompt injection & out-of-domain defense | **100.0%** (4/4) | PASS |
| **Metadata Filter Precision** | Target agreement clause isolation | **100.0%** | OPTIMIZED |
