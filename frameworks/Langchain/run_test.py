import os
import time
from pathlib import Path
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

ROOT        = Path(__file__).resolve().parents[2]
SKILL_PATH  = ROOT / "skills"  / "SKILL.md"
PROMPT_PATH = ROOT / "prompts" / "test_prompt.txt"
ENV_PATH    = ROOT / ".env"
RESULTS_PATH = ROOT / "results.md"

MODEL = "openai/gpt-4o-mini-2024-07-18"


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
    """
    Auto-checks if the model's response contains the correct
    endpoint, filter and method from the skill document.
    Returns a simple YES / PARTIAL / NO grade.
    """
    response_lower = response_text.lower()
    checks = {
        "correct endpoint": "catalog/search" in response_lower,
        "correct filter"  : "type eq" in response_lower and "lakehouse" in response_lower,
        "correct method"  : "post" in response_lower,
    }
    passed = sum(checks.values())
    if passed == 3:
        grade = "YES"
    elif passed >= 1:
        grade = "PARTIAL"
    else:
        grade = "NO"
    return grade, checks


def save_to_results(model, elapsed, response_text, grade):
    """
    Appends one run's results to results.md automatically.
    Each run adds a new row so you can compare across runs.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # If results.md is empty or new, write the header first
    if not RESULTS_PATH.exists() or RESULTS_PATH.stat().st_size == 0:
        header = (
            "# Fabric Skill Benchmark Results\n\n"
            "| Timestamp | Framework | Model | Time (s) | Correct? |\n"
            "|-----------|-----------|-------|----------|----------|\n"
        )
        RESULTS_PATH.write_text(header, encoding="utf-8")

    # Append this run as a new row
    row = (
        f"| {timestamp} "
        f"| LangChain + OpenRouter "
        f"| {model} "
        f"| {elapsed:.2f} "
        f"| {grade} |\n"
    )

    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(row)

    # Also append the full response below the table for reference
    divider = f"\n---\n### Run: {timestamp} | {model}\n"
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(divider)
        f.write(f"**Time:** {elapsed:.2f}s | **Correct:** {grade}\n\n")
        f.write("**Response:**\n\n")
        f.write(response_text.strip())
        f.write("\n")

    print(f"\nResults saved to: {RESULTS_PATH}")


def main():
    load_env_file()
    api_key = check_api_key()
    if not api_key:
        return

    skill_text  = SKILL_PATH.read_text(encoding="utf-8")
    user_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    system_prompt = (
        "You are an assistant that strictly follows the Microsoft Fabric "
        "skill document below. Do not use any knowledge outside of it.\n\n"
        "=== SKILL DOCUMENT START ===\n"
        f"{skill_text}\n"
        "=== SKILL DOCUMENT END ==="
    )

    http_client = None
    try:
        import httpx
        http_client = httpx.Client(verify=False)
    except ImportError:
        pass

    llm_kwargs = dict(
        model=MODEL,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=1024,
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "FabricSkillBench",
        }
    )
    if http_client:
        llm_kwargs["http_client"] = http_client

    llm   = ChatOpenAI(**llm_kwargs)
    agent = create_agent(llm, tools=[], system_prompt=system_prompt)

    print(f"\nModel  : {MODEL}")
    print(f"Source : OpenRouter")
    print("Running... please wait\n")

    start   = time.perf_counter()
    result  = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
    elapsed = time.perf_counter() - start

    final_message = result["messages"][-1].content

    # Auto-check correctness
    grade, checks = check_correctness(final_message)

    print("=" * 60)
    print(f"FRAMEWORK  : LangChain + OpenRouter")
    print(f"MODEL      : {MODEL}")
    print(f"TIME TAKEN : {elapsed:.2f} seconds")
    print(f"CORRECT    : {grade}")
    print("=" * 60)
    print("RESPONSE:\n")
    print(final_message)
    print("=" * 60)

    print("\nCORRECTNESS DETAIL:")
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {check}")

    # Save everything to results.md automatically
    save_to_results(MODEL, elapsed, final_message, grade)


if __name__ == "__main__":
    main()
