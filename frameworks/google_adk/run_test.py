import os, time, asyncio, re
from pathlib import Path
from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

ROOT         = Path(__file__).resolve().parents[2]
SKILL_PATH   = ROOT / "skills"  / "SKILL.md"
PROMPT_PATH  = ROOT / "prompts" / "test_prompt.txt"
ENV_PATH     = ROOT / ".env"
RESULTS_PATH = ROOT / "results.md"
MODEL        = "openai/gpt-4o-mini"

def load_env_file():
    if not ENV_PATH.exists():
        return
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

def check_api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("ERROR: OPENROUTER_API_KEY not found in .env")
        return None
    return key

def safe_for_adk(text):
    # Replace {anything} with [[anything]] so ADK stops treating them as variables
    return re.sub(r'\{([^{}]+)\}', r'[[\1]]', text)

def check_correctness(r):
    r = r.lower()
    checks = {
        "correct endpoint": "catalog/search" in r,
        "correct filter"  : "type eq" in r and "lakehouse" in r,
        "correct method"  : "post" in r,
    }
    passed = sum(checks.values())
    grade = "YES" if passed==3 else ("PARTIAL" if passed>=1 else "NO")
    return grade, checks

def save_to_results(elapsed, response_text, grade):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    if not RESULTS_PATH.exists() or RESULTS_PATH.stat().st_size == 0:
        RESULTS_PATH.write_text(
            "# Fabric Skill Benchmark Results\n\n"
            "| Timestamp | Framework | Model | Time (s) | Correct? |\n"
            "|-----------|-----------|-------|----------|----------|\n",
            encoding="utf-8"
        )
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(f"| {ts} | Google ADK | {MODEL} | {elapsed:.2f} | {grade} |\n")
        f.write(f"\n---\n### Run: {ts} | Google ADK | {MODEL}\n")
        f.write(f"**Time:** {elapsed:.2f}s | **Correct:** {grade}\n\n")
        f.write(f"**Response:**\n\n{response_text.strip()}\n")
    print(f"Results saved to: {RESULTS_PATH}")

async def run_agent(skill_text, user_prompt, api_key):
    safe_skill = safe_for_adk(skill_text)
    os.environ["OPENROUTER_API_KEY"] = api_key
    agent = LlmAgent(
        name="fabric_skill_agent",
        model=LiteLlm(model=f"openrouter/{MODEL}"),
        instruction=(
            "You strictly follow the Fabric skill document below. "
            "Use no outside knowledge.\n\n"
            "=== SKILL START ===\n"
            + safe_skill +
            "\n=== SKILL END ==="
        ),
        description="Fabric skill benchmark agent",
    )
    svc = InMemorySessionService()
    await svc.create_session(app_name="fb", user_id="u1", session_id="s1")
    runner = Runner(agent=agent, app_name="fb", session_service=svc)
    msg = types.Content(role="user", parts=[types.Part(text=user_prompt)])
    out = ""
    async for event in runner.run_async(user_id="u1", session_id="s1", new_message=msg):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    out += part.text
    return out

def main():
    load_env_file()
    api_key = check_api_key()
    if not api_key:
        return
    skill_text  = SKILL_PATH.read_text(encoding="utf-8")
    user_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    print(f"\nModel     : {MODEL}\nFramework : Google ADK\nRunning... please wait\n")
    start = time.perf_counter()
    response_text = asyncio.run(run_agent(skill_text, user_prompt, api_key))
    elapsed = time.perf_counter() - start
    grade, checks = check_correctness(response_text)
    print("=" * 60)
    print(f"FRAMEWORK  : Google ADK\nMODEL      : {MODEL}\nTIME TAKEN : {elapsed:.2f} seconds\nCORRECT    : {grade}")
    print("=" * 60)
    print("RESPONSE:\n")
    print(response_text)
    print("=" * 60)
    print("\nCORRECTNESS DETAIL:")
    for check, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {check}")
    save_to_results(elapsed, response_text, grade)

if __name__ == "__main__":
    main()
