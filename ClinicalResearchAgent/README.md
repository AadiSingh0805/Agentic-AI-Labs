# Experiment No. 3: Clinical Research Assistant with Tool Integration (Healthcare Domain)

## Overview
This repository contains the full Python implementation for **Experiment No. 3: Clinical Research Assistant with Tool Integration**. The intelligent agent selects appropriate healthcare tools, extracts structured parameters, executes validated tool calls, manages retries and fallbacks, enforces security policies, and logs system observability metrics.

---

## 🏗️ Architecture & Workflow
```
User Query
   │
   ▼
Input Validation & Intent Selection
   │
   ▼
Parameter Extraction
   │
   ▼
Structured Tool Call Contract Construction
   │
   ▼
Schema & Authorization Validation
   │
   ▼
Tool Execution Engine
   ├── Retry Mechanism (Max 3 attempts for transient errors)
   └── Fallback Mechanism (Predefined fallback tools)
   │
   ▼
Safe Response Generation & CSV Interaction Logging
   │
   ▼
Observability & Reliability Analysis
```

---

## 🛠️ Registered Healthcare Tools
1. **`medical_literature_search`**: Searches medical publications and clinical trials. Filters by query, publication year, and maximum result count.
2. **`medical_calculator`**: Calculates body metrics (BMI) based on weight (`kg`) and height (`m`) with category classification.
3. **`healthcare_knowledge_search`**: Searches a controlled medical knowledge base, returning structured information or a safe `NO_RESULT` response.
4. **`unreliable_medical_tool`**: Demonstration tool used to evaluate transient retry and fallback handling.

---

## 🚀 Optimization Benchmarks Performed

### **Optimization 1 – Tool Selection Accuracy**
Evaluates intent identification and keyword routing against a 10-query ground-truth benchmark suite:
- **Total Tests Evaluated**: 10
- **Correct Selections**: 10
- **Tool Selection Accuracy Rate**: **100.00%**

### **Optimization 2 – Schema Validation Resilience**
Measures schema validation enforcement across valid parameter calls, missing parameters, invalid data types, and unregistered tool calls:
- **Total Validation Tests**: 5
- **Passed Validation Tests**: 5
- **Schema Validation Pass Rate**: **100.00%**

---

## 🛡️ Security & Adversarial Resilience
Evaluates 5 adversarial prompts (unauthorized tool execution, prompt injection, fake diagnosis requests, fabrication requests, and safety bypasses):
- **Passed Security Tests**: 5 / 5
- **Security Pass Rate**: **100.00%**

---

## 📂 Interaction Log Schema (`clinical_research_interaction_log.csv`)
- **Timestamp**: Execution timestamp.
- **User Query**: Original query string.
- **Tool Name**: Selected tool.
- **Parameters**: Extracted JSON parameters.
- **Authorization Status**: `AUTHORIZED` or `REJECTED`.
- **Attempts**: Number of execution attempts (including retries).
- **Error Category**: Error classification (`INPUT_ERROR`, `AUTHORIZATION_ERROR`, `TRANSIENT_ERROR`, `SERVICE_ERROR`, `UNKNOWN_ERROR`).
- **Execution Status**: `SUCCESS`, `FAILED`, or `REJECTED`.
- **Source**: Caller source tag.
- **Response**: Truncated safe response string.

---

## 💻 How to Run
```bash
python ClinicalResearchAgent/clinical_agent.py
```
