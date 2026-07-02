"""
smolagents test harness for Fabric skill benchmark.
Same model as other frameworks (gpt-4o-mini via OpenRouter)
Only the FRAMEWORK WRAPPER changes - that is what we are benchmarking.

Requirements:
  pip install smolagents openai
"""

import os
import time
from pathlib import Path
from datetime import datetime
from smolagents import OpenAIServerModel, ToolCallingAgent

ROOT         = Path(__file__).resolve().parents[2]
SKILL_PATH   = ROOT / "skills"  / "SKILL.md"
PROMPT_PATH  = ROOT / "prompts" / "test_prompt.txt"
ENV_PATH     = ROOT / ".env"
RESULTS_PATH = ROOT / "results.md"
MODEL        = "openai/gpt-4o-mini-2024-07-18"


def load_env_file():
    if not ENV_PATH.exists():
        print(f"ERROR: .env file not found at: {ENV_PATH}")
        return
    with open(ENV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


def check_api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("ERROR: OPENROUTER_API_KEY not found in .env file.")
        return None
    return key


def check_correctness(response_text):
    r = response_text.lower()
    checks = {
        "correct endpoint": "catalog/search" in r,
        "correct filter"  : "type eq" in r and "lakehouse" in r,
        "correct method"  : "post" in r,
    }
    passed = sum(checks.values())
    grade = "YES" if passed == 3 else ("PARTIAL" if passed >= 1 else "NO")
    return grade, checks


def save_to_results(model, elapsed, response_text, grade):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if not RESULTS_PATH.exists() or RESULTS_PATH.stat().st_size == 0:
        RESULTS_PATH.write_text(
            "# Fabric Skill Benchmark Results\n\n"
            "| Timestamp | Framework | Model | Time (s) | Correct? |\n"
            "|-----------|-----------|-------|----------|----------|\n",
            encoding="utf-8"
        )
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(f"| {timestamp} | smolagents | {model} | {elapsed:.2f} | {grade} |\n")
        f.write(f"\n---\n### Run: {timestamp} | smolagents | {model}\n")
        f.write(f"**Time:** {elapsed:.2f}s | **Correct:** {grade}\n\n")
        f.write(f"**Response:**\n\n{response_text.strip()}\n")
    print(f"\nResults saved to: {RESULTS_PATH}")


def main():
    load_env_file()
    api_key = check_api_key()
    if not api_key:
        return

    skill_text  = SKILL_PATH.read_text(encoding="utf-8")
    user_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    full_task = (
        "You are an assistant that strictly follows the Microsoft Fabric "
        "skill document below. Do not use any knowledge outside of it.\n\n"
        "=== SKILL DOCUMENT START ===\n"
        f"{skill_text}\n"
        "=== SKILL DOCUMENT END ===\n\n"
        f"User request:\n{user_prompt}"
    )

    model = OpenAIServerModel(
        model_id=MODEL,
        api_base="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0,
        max_tokens=1024,
    )

    agent = ToolCallingAgent(tools=[], model=model)

    print(f"\nModel     : {MODEL}")
    print(f"Framework : smolagents")
    print("Running... please wait\n")

    start   = time.perf_counter()
    result  = agent.run(full_task)
    elapsed = time.perf_counter() - start

    response_text = str(result)
    grade, checks = check_correctness(response_text)

    print("=" * 60)
    print(f"FRAMEWORK  : smolagents")
    print(f"MODEL      : {MODEL}")
    print(f"TIME TAKEN : {elapsed:.2f} seconds")
    print(f"CORRECT    : {grade}")
    print("=" * 60)
    print("RESPONSE:\n")
    print(response_text)
    print("=" * 60)
    print("\nCORRECTNESS DETAIL:")
    for check, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {check}")
    save_to_results(MODEL, elapsed, response_text, grade)


if __name__ == "__main__":
    main()
