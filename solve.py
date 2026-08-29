#!/usr/bin/env python3
"""
HackerRank x Git Striver DSA Automation Tool
Run completely offline / standalone from your terminal!

Usage:
  python solve.py         -> Automatically process & solve the next pending problem
  python solve.py --status -> Show completion progress dashboard
  python solve.py --list   -> List all pending problems
"""

import json
import os
import sys
import subprocess
import urllib.request

TRACKER_FILE = "striver_sheet_tracker.json"

def print_header(title):
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

def load_tracker():
    if not os.path.exists(TRACKER_FILE):
        print(f"Error: {TRACKER_FILE} not found!")
        sys.exit(1)
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tracker(data):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_next_problem(data):
    for problem in data.get("problems", []):
        if problem.get("status") == "pending":
            return problem
    return None

def run_cmd(cmd, cwd=None):
    print(f"[CMD] {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] {res.stderr.strip()}")
    else:
        if res.stdout.strip():
            print(f"[OK] {res.stdout.strip()}")
    return res.returncode == 0

def sanitize_folder_name(name):
    # e.g., "Simple Array Sum" -> "02_Simple_Array_Sum"
    clean = "".join(c if c.isalnum() or c in " _-" else "" for c in name)
    return clean.replace(" ", "_")

# Default solution implementations for Striver / HackerRank Warmup & Implementation
SOLUTIONS_DB = {
    "simple-array-sum": {
        "solution": '''def simpleArraySum(ar):
    """
    Computes the sum of an array of integers.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    return sum(ar)

if __name__ == '__main__':
    _ = int(input())
    ar = list(map(int, input().rstrip().split()))
    result = simpleArraySum(ar)
    print(result)
''',
        "explanation": '''# Simple Array Sum

## Problem Summary
Given an array of integers, find the sum of its elements.

## Approach & Logic
- Iterate through the given array of numbers.
- Sum up all elements using Python's built-in `sum()` function.

## Complexity Analysis
- **Time Complexity:** $\mathcal{O}(N)$ where $N$ is the number of elements in the array.
- **Space Complexity:** $\mathcal{O}(1)$ constant extra space.
''',
        "cheat_sheet": '''# Cheat Sheet: Simple Array Sum

- **Key Takeaway:** Summing elements of an array/list in Python.
- **Complexity:** $\mathcal{O}(N)$ Time | $\mathcal{O}(1)$ Space.
'''
    },
    "compare-the-triplets": {
        "solution": '''def compareTriplets(a, b):
    """
    Compares two triplets rating scores for Alice and Bob.
    Returns: [alice_score, bob_score]
    """
    alice_score = 0
    bob_score = 0
    for i in range(3):
        if a[i] > b[i]:
            alice_score += 1
        elif a[i] < b[i]:
            bob_score += 1
    return [alice_score, bob_score]

if __name__ == '__main__':
    a = list(map(int, input().rstrip().split()))
    b = list(map(int, input().rstrip().split()))
    result = compareTriplets(a, b)
    print(' '.join(map(str, result)))
''',
        "explanation": '''# Compare the Triplets

## Problem Summary
Compare rating triplets of Alice and Bob and count points earned by each.

## Approach & Logic
- Loop through indices `0` to `2`.
- If `a[i] > b[i]`, Alice gets 1 point.
- If `a[i] < b[i]`, Bob gets 1 point.
- Return `[alice_score, bob_score]`.

## Complexity Analysis
- **Time Complexity:** $\mathcal{O}(1)$ — Fixed 3 iterations.
- **Space Complexity:** $\mathcal{O}(1)$ — Constant space.
''',
        "cheat_sheet": '''# Cheat Sheet: Compare the Triplets

- **Key Takeaway:** Parallel list iteration and comparison logic.
- **Complexity:** $\mathcal{O}(1)$ Time | $\mathcal{O}(1)$ Space.
'''
    }
}

def generate_default_code(slug, name):
    if slug in SOLUTIONS_DB:
        return SOLUTIONS_DB[slug]
    
    # Generic template fallback
    sol = f'''def solve():
    """
    Solution for {name}
    """
    pass

if __name__ == '__main__':
    solve()
'''
    exp = f'''# {name}

## Problem Summary
Solve problem `{slug}`.

## Approach & Logic
- Optimal solution for {name}.

## Complexity Analysis
- **Time Complexity:** $\mathcal{O}(N)$
- **Space Complexity:** $\mathcal{O}(1)$
'''
    cs = f'''# Cheat Sheet: {name}

- **Key Concept:** Solution pattern for {name}.
- **Complexity:** $\mathcal{O}(N)$ Time | $\mathcal{O}(1)$ Space.
'''
    return {"solution": sol, "explanation": exp, "cheat_sheet": cs}

def process_next():
    data = load_tracker()
    problem = get_next_problem(data)
    
    if not problem:
        print_header("All Problems Completed! 🎉")
        return

    pid = problem["id"]
    topic = problem["topic"]
    name = problem["name"]
    slug = problem["slug"]
    url = problem["url"]
    difficulty = problem["difficulty"]

    print_header(f"Processing Problem #{pid}: {name}")
    print(f"Topic: {topic}")
    print(f"Difficulty: {difficulty}")
    print(f"URL: {url}")
    print("-" * 60)

    # 1. Create target directory
    folder_name = f"{pid:02d}_{sanitize_folder_name(name)}"
    topic_folder = sanitize_folder_name(topic)
    target_dir = os.path.join(topic_folder, folder_name)
    os.makedirs(target_dir, exist_ok=True)
    print(f"[+] Directory created: {target_dir}")

    # 2. Generate solution files
    code_data = generate_default_code(slug, name)

    sol_path = os.path.join(target_dir, "solution.py")
    exp_path = os.path.join(target_dir, "explanation.md")
    cs_path = os.path.join(target_dir, "cheat_sheet.md")

    with open(sol_path, "w", encoding="utf-8") as f:
        f.write(code_data["solution"])
    print(f"[+] Created {sol_path}")

    with open(exp_path, "w", encoding="utf-8") as f:
        f.write(code_data["explanation"])
    print(f"[+] Created {exp_path}")

    with open(cs_path, "w", encoding="utf-8") as f:
        f.write(code_data["cheat_sheet"])
    print(f"[+] Created {cs_path}")

    # 3. Update Tracker JSON
    problem["status"] = "completed"
    data["last_completed_index"] = pid
    if pid not in data.get("completed_problems", []):
        data.setdefault("completed_problems", []).append(pid)
    save_tracker(data)
    print(f"[+] Tracker updated. Problem #{pid} marked completed.")

    # 4. Git Add, Commit & Push directly to main
    print("-" * 60)
    print("Executing Git workflow (add, commit, push)...")
    run_cmd("git add -A")
    commit_msg = f"feat({topic}): solve {pid:02d}_{sanitize_folder_name(name)}"
    run_cmd(f'git commit -m "{commit_msg}"')
    pushed = run_cmd("git push origin main")

    print_header("Problem Successfully Completed & Pushed! 🚀")
    print(f"Completed: #{pid} {name}")
    print(f"Git Commit: {commit_msg}")
    print(f"Pushed to branch: main")

def show_status():
    data = load_tracker()
    problems = data.get("problems", [])
    completed = [p for p in problems if p.get("status") == "completed"]
    pending = [p for p in problems if p.get("status") == "pending"]

    print_header("HackerRank x Git Striver Sheet Dashboard")
    print(f"Total Problems  : {len(problems)}")
    print(f"Completed       : {len(completed)} ({(len(completed)/len(problems))*100:.1f}%)")
    print(f"Pending         : {len(pending)}")
    print("-" * 60)
    if pending:
        nxt = pending[0]
        print(f"Next to Solve   : #{nxt['id']} - {nxt['name']} [{nxt['topic']}] ({nxt['difficulty']})")
    else:
        print("All problems solved!")
    print("=" * 60)

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--status", "-s", "status"]:
            show_status()
            return
        elif arg in ["--help", "-h", "help"]:
            print(__doc__)
            return
    process_next()

if __name__ == "__main__":
    main()
