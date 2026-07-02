# Fabric Agent Framework Benchmark

A benchmarking scaffold that tests different AI agent frameworks invoking Microsoft Fabric skill documents, to determine which framework performs fastest and most accurately.

## What This Project Does

Microsoft Fabric skills are instruction documents (SKILL.md files) that teach an AI agent how to perform Fabric tasks — searching Lakehouses, building pipelines, creating Dataflows etc.

This project answers one question:

> **Does the choice of agent framework (LangChain vs smolagents vs Google ADK vs AutoGen) affect speed and accuracy when invoking the same Fabric skill?**

The model is kept the same across all frameworks so only the framework overhead is measured.

---

## Project Structure

```
skillsWorkbench_1/
├── .env                          ← API keys (never share this)
├── .gitignore                    ← keeps .env and venv out of git
├── results.md                    ← auto-filled benchmark results
├── SUMMARY.md                    ← one page findings
├── README.md                     ← this file
│
├── skills/
│   └── SKILL.md                  ← search-consumption-cli skill doc
│
├── prompts/
│   └── test_prompt.txt           ← fixed test question used by all frameworks
│
├── frameworks/
│   ├── openrouter/
│   │   └── run_test.py           ← LangChain + OpenRouter test
│   ├── smolagents/
│   │   └── run_test.py           ← smolagents test
│   ├── google_adk/
│   │   └── run_test.py           ← Google ADK test
│   └── autogen/
│       └── run_test.py           ← AutoGen (Microsoft) test
│
└── verification/
    └── verify_in_fabric.py       ← confirms skill works on real Fabric workspace
```

---

## Prerequisites

- Python 3.11 or 3.12 recommended (3.14 has SSL compatibility issues)
- OpenRouter API key — set in `.env` file
- Org Microsoft Fabric account — for verification script only

---

## Setup (First Time Only)

**Step 1 — Create virtual environment:**
```powershell
cd skillsWorkbench_1
python -m venv venv
venv\Scripts\Activate.ps1
```

**Step 2 — Install all packages:**
```powershell
pip install langchain langchain-openai smolagents openai google-adk litellm autogen-agentchat "autogen-ext[openai]" azure-identity requests
```

**Step 3 — Create `.env` file** in the `skillsWorkbench_1` folder:
```
OPENROUTER_API_KEY=your-key-here
```

---

## How to Run Each Framework

Activate venv first every time you open a new terminal:
```powershell
venv\Scripts\Activate
```

**LangChain (OpenRouter):**
```powershell
python frameworks/Langchain/run_test.py
```

**smolagents:**
```powershell
python frameworks/smolagents/run_test.py
```

**Google ADK:**
```powershell
python frameworks/google_adk/run_test.py
```

**AutoGen (Microsoft):**
```powershell
python frameworks/autogen/run_test.py
```

Each script automatically saves timing and correctness to `results.md`.

---

## How to Verify Results in Real Fabric

**Step 1 — Install verification dependencies:**
```powershell
pip install azure-identity requests
```

**Step 2 — Run verification:**
```powershell
python verification/verify_in_fabric.py
```

**Step 3 — What happens:**
- Browser opens automatically
- Log in with your org Microsoft account
- Script calls the real Fabric REST API
- Prints your actual workspaces and Lakehouses

This confirms the `az rest` command the LLM generated actually works against a live Fabric environment.

---

## How to Check Results

Open `results.md` — it auto-fills after every run:

```
| Timestamp | Framework | Model | Time (s) | Correct? |
|-----------|-----------|-------|----------|----------|
| ...       | LangChain | ...   | 5.89     | YES      |
| ...       | smolagents| ...   | 7.70     | YES      |
```

**Correctness is auto-checked against 3 criteria:**
- ✅ Correct endpoint: `api.fabric.microsoft.com/v1/catalog/search`
- ✅ Correct method: `POST`  
- ✅ Correct filter: `Type eq 'Lakehouse'`

---

## How to Change the Model

Open any `run_test.py` and change the MODEL line at the top:

```python
# Current:
MODEL = "openai/gpt-4o-mini"
```

Keep the same model across all frameworks for a fair comparison.

---
## Key Findings

| Framework | Time (gpt-4o-mini) | Recommendation |
|-----------|-------------------|----------------|
| LangChain | 5.89s | ✅ Best overall |
| AutoGen | 6.01s | ✅ Good, Microsoft ecosystem fit |
| smolagents | 7.70s | ⚠️ Acceptable |
| Google ADK | 9.21s | ❌ Slowest, setup complexity, skill doc compatibility issue |

See `SUMMARY.md` for full findings and recommendation.

---

## Known Issues

**Google ADK curly brace issue:**
Google ADK treats `{variable}` patterns in instruction text as template variables. Since SKILL.md contains JSON like `{"search": ""}`, a regex workaround replaces curly braces with square brackets before passing to ADK. The LLM still correctly follows the skill but outputs `[[search]]` instead of `{"search"}` in JSON examples.

