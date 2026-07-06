import os
import time
from pathlib import Path
from datetime import datetime
from langchain_openai import ChatOpenAI

ROOT         = Path(__file__).resolve().parents[2]
SKILL_PATH   = ROOT / "skills"  / "SKILL.md"
PROMPT_PATH  = ROOT / "prompts" / "test_prompt.txt"
ENV_PATH     = ROOT / ".env"
RESULTS_PATH = ROOT / "results.md"

# Change this to test each model one by one
MODEL = "z-ai/glm-5.2"   

# All 5 models :
# "moonshotai/kimi-k2.6"                    
# "deepseek-ai/deepseek-v4-flash"                  
# "deepseek-ai/deepseek-v4-pro"
# "minimaxai/minimax-m3"                         
# "qwen/qwen3.5-397b-a17b"        
# "z-ai/glm-5.2"                            

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
    key = os.environ.get("NVIDIA_API_KEY")
    if not key:
        print("ERROR: NVIDIA_API_KEY not found in .env")
        print("Get free key at: https://integrate.api.nvidia.com")
        return None
    return key

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
        f.write(f"| {ts} | LangChain + NVIDIA NIM | {MODEL} | {elapsed:.2f} | {grade} |\n")
        f.write(f"\n---\n### Run: {ts} | NVIDIA NIM | {MODEL}\n")
        f.write(f"**Time:** {elapsed:.2f}s | **Correct:** {grade}\n\n")
        f.write(f"**Response:**\n\n{response_text.strip()}\n")
    print(f"Results saved to: {RESULTS_PATH}")

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

    import httpx
    llm = ChatOpenAI(
        model=MODEL,
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1",  # NVIDIA endpoint
        temperature=0,
        max_tokens=1024,
        http_client=httpx.Client(verify=False),
    )

    from langchain.agents import create_agent
    agent = create_agent(llm, tools=[], system_prompt=system_prompt)

    print(f"\nModel     : {MODEL}")
    print(f"Framework : LangChain + NVIDIA NIM")
    print("Running... please wait\n")

    start  = time.perf_counter()
    result = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
    elapsed = time.perf_counter() - start

    response_text = result["messages"][-1].content
    grade, checks = check_correctness(response_text)

    print("=" * 60)
    print(f"FRAMEWORK  : LangChain + NVIDIA NIM")
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
    save_to_results(elapsed, response_text, grade)

if __name__ == "__main__":
    main()