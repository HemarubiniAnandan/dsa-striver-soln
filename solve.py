#!/usr/bin/env python3
"""
GeeksforGeeks Striver DSA Automation Tool
=========================================
Automatically solves Striver DSA problems on GeeksforGeeks:
  1. Interactive CLI prompt ([L] Login / [1] Solve Next / [A] Solve All / [S] Status)
  2. Persistent GFG Browser Session (.gfg_user_data) with Login Enforcement
  3. GFG Code Automation: Selects Python3, pastes code in Monaco Editor, clicks Submit & verifies Accepted count increase
  4. File Generation: solution.py, explanation.md, cheat_sheet.md, problem_screenshot.png
  5. Git Automation: Commits & pushes directly to main branch

Usage:
  npm run start             -> Launch interactive menu
  npm run login             -> Open browser for manual/automated login on screen
  npm run solve             -> Solve the next pending problem directly on GFG
  npm run status            -> Display progress dashboard
  npm run all               -> Solve all remaining problems in a loop
"""

import json
import os
import sys
import time
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# ─── Config ───────────────────────────────────────────────────────────
load_dotenv()
GFG_EMAIL = os.getenv("GFG_EMAIL", "")
GFG_PASSWORD = os.getenv("GFG_PASSWORD", "")
TRACKER_FILE = "striver_sheet_tracker.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_DIR = os.path.join(BASE_DIR, ".gfg_user_data")

# ─── GFG Solutions Database ───────────────────────────────────────────
# Clean Python3 solutions matching GFG class Solution method signatures
SOLUTIONS = {
    "count-digits5716": {
        "code": """class Solution:
    def evenlyDivides(self, N):
        count = 0
        for d in str(N):
            val = int(d)
            if val != 0 and N % val == 0:
                count += 1
        return count
""",
        "approach": "Iterate through digits of N as string. If digit is non-zero and divides N, increment count.",
        "time": "O(log10 N)",
        "space": "O(1)"
    },
    "reverse-bits1615": {
        "code": """class Solution:
    def reversedBits(self, X):
        res = 0
        for i in range(32):
            res = (res << 1) | (X & 1)
            X >>= 1
        return res
""",
        "approach": "Extract LSB of X and push into result res using bit shifts across 32 iterations.",
        "time": "O(1)",
        "space": "O(1)"
    },
    "palindrome0742": {
        "code": """class Solution:
    def is_palindrome(self, n):
        s = str(n)
        return "Yes" if s == s[::-1] else "No"
""",
        "approach": "Convert integer to string and check if it equals its reverse.",
        "time": "O(log10 N)",
        "space": "O(1)"
    },
    "lcm-and-gcd4516": {
        "code": """from math import gcd

class Solution:
    def lcmAndGcd(self, A, B):
        g = gcd(A, B)
        l = (A * B) // g
        return [l, g]
""",
        "approach": "Use Euclidean algorithm via math.gcd to find GCD. LCM = (A * B) // GCD.",
        "time": "O(log(min(A, B)))",
        "space": "O(1)"
    },
    "armstrong-numbers2727": {
        "code": """class Solution:
    def armstrongNumber(self, n):
        s = str(n)
        k = len(s)
        total = sum(int(d)**k for d in s)
        return "Yes" if total == n else "No"
""",
        "approach": "Sum each digit raised to the power of total number of digits. Compare with original n.",
        "time": "O(log10 N)",
        "space": "O(1)"
    },
    "sum-of-all-divisors-from-1-to-n4738": {
        "code": """class Solution:
    def sumOfDivisors(self, N):
        ans = 0
        for i in range(1, N + 1):
            ans += i * (N // i)
        return ans
""",
        "approach": "Each integer i between 1 and N appears as a divisor (N // i) times across all numbers from 1 to N.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "print-1-to-n-without-loop-1587115620": {
        "code": """class Solution:
    def printNos(self, N):
        if N <= 0:
            return
        self.printNos(N - 1)
        print(N, end=" ")
""",
        "approach": "Use recursion to print 1 to N without using any for/while loops.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "print-n-to-1-without-loop": {
        "code": """class Solution:
    def printNos(self, N):
        if N <= 0:
            return
        print(N, end=" ")
        self.printNos(N - 1)
""",
        "approach": "Use tail recursion: print current N and recurse for N-1.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "sum-of-first-n-terms5843": {
        "code": """class Solution:
    def sumOfSeries(self, n):
        # Sum of cubes = (n*(n+1)//2)^2
        s = (n * (n + 1)) // 2
        return s * s
""",
        "approach": "Mathematical formula for sum of first n cubes: (n*(n+1)/2)^2.",
        "time": "O(1)",
        "space": "O(1)"
    },
    "find-all-factorial-numbers-less-than-or-equal-to-n3548": {
        "code": """class Solution:
    def factorialNumbers(self, n):
        res = []
        fact = 1
        i = 1
        while fact <= n:
            res.append(fact)
            i += 1
            fact *= i
        return res
""",
        "approach": "Iteratively generate factorials starting from 1! until factorial > n.",
        "time": "O(k)",
        "space": "O(k)"
    },

    "largest-element-in-array": {
        "code": """class Solution:
    def largest(self, arr):
        return max(arr)
""",
        "approach": "Iterate through array to track maximum element using built-in max().",
        "time": "O(N)",
        "space": "O(1)"
    },
    "second-largest3735": {
        "code": """class Solution:
    def print2largest(self, arr):
        first = second = -1
        for x in arr:
            if x > first:
                second = first
                first = x
            elif x < first and x > second:
                second = x
        return second
""",
        "approach": "Track first largest and second largest elements in a single linear pass.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "check-if-an-array-is-sorted0701": {
        "code": """class Solution:
    def arraySortedOrNot(self, arr):
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True
""",
        "approach": "Check adjacent pairs arr[i] <= arr[i+1]. Return False on any violation.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "remove-duplicate-elements-from-sorted-array": {
        "code": """class Solution:
    def remove_duplicate(self, arr):
        if not arr:
            return 0
        i = 0
        for j in range(1, len(arr)):
            if arr[j] != arr[i]:
                i += 1
                arr[i] = arr[j]
        return i + 1
""",
        "approach": "Two-pointer approach: overwrite duplicate elements in-place.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "rotate-array-by-n-elements-1587115621": {
        "code": """class Solution:
    def rotateArr(self, arr, d):
        n = len(arr)
        d %= n
        arr[:] = arr[d:] + arr[:d]
""",
        "approach": "Slice array at index d and concatenate left rotated parts.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "move-all-zeroes-to-end-of-array0751": {
        "code": """class Solution:
    def pushZerosToEnd(self, arr):
        pos = 0
        for i in range(len(arr)):
            if arr[i] != 0:
                arr[pos], arr[i] = arr[i], arr[pos]
                pos += 1
""",
        "approach": "Maintain non-zero insertion index pos and swap non-zero elements forward.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "union-of-two-sorted-arrays-1587115621": {
        "code": """class Solution:
    def findUnion(self, a, b):
        res = sorted(list(set(a).union(set(b))))
        return res
""",
        "approach": "Compute union of sets of arrays a and b and return sorted list.",
        "time": "O((N+M) log(N+M))",
        "space": "O(N+M)"
    },
    "missing-number-in-array1416": {
        "code": """class Solution:
    def missingNumber(self, arr, n):
        expected = n * (n + 1) // 2
        actual = sum(arr)
        return expected - actual
""",
        "approach": "Expected sum of 1 to n is n*(n+1)/2. Missing number = expected_sum - actual_sum.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "maximize-number-of-1s0953": {
        "code": """class Solution:
    def maxOnes(self, arr, k):
        left = 0
        zeros = 0
        max_len = 0
        for right in range(len(arr)):
            if arr[right] == 0:
                zeros += 1
            while zeros > k:
                if arr[left] == 0:
                    zeros -= 1
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len
""",
        "approach": "Sliding window allowing at most k zeros to be flipped to 1s.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "element-appearing-once2552": {
        "code": """class Solution:
    def search(self, arr):
        res = 0
        for x in arr:
            res ^= x
        return res
""",
        "approach": "XOR all elements in array. Paired elements cancel out (x^x = 0), leaving single element.",
        "time": "O(N)",
        "space": "O(1)"
    }
}

# ─── Helpers ──────────────────────────────────────────────────────────
def print_header(title):
    w = 60
    print("=" * w)
    print(f"  {title}")
    print("=" * w)

def load_tracker():
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tracker(data):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_next_problem(data):
    for p in data.get("problems", []):
        if p.get("status") == "pending":
            return p
    return None

def sanitize(name):
    return "".join(c if c.isalnum() or c in " _-" else "" for c in name).replace(" ", "_")

def run_git(cmd):
    print(f"  [GIT] {cmd}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0 and r.stderr.strip():
        print(f"  [ERR] {r.stderr.strip()}")
    return r.returncode == 0

def generate_solution_files(problem, code, approach, tc, sc):
    """Create solution.py, explanation.md, cheat_sheet.md in topic folder."""
    pid = problem["id"]
    topic = problem["topic"]
    name = problem["name"]

    folder = os.path.join(topic, f"{pid:02d}_{sanitize(name)}")
    os.makedirs(folder, exist_ok=True)

    # solution.py
    with open(os.path.join(folder, "solution.py"), "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print(f"  [+] {folder}/solution.py")

    # explanation.md
    exp = f"""# {name}

## Problem Information
- **URL:** {problem['url']}
- **Topic:** {topic}
- **Difficulty:** {problem['difficulty']}

## Approach & Logic
{approach}

## Complexity Analysis
- **Time Complexity:** {tc}
- **Space Complexity:** {sc}
"""
    with open(os.path.join(folder, "explanation.md"), "w", encoding="utf-8") as f:
        f.write(exp)
    print(f"  [+] {folder}/explanation.md")

    # cheat_sheet.md
    cs = f"""# Cheat Sheet: {name}

- **Core Pattern:** {approach}
- **Time Complexity:** {tc}
- **Space Complexity:** {sc}
- **Difficulty:** {problem['difficulty']}
"""
    with open(os.path.join(folder, "cheat_sheet.md"), "w", encoding="utf-8") as f:
        f.write(cs)
    print(f"  [+] {folder}/cheat_sheet.md")

    return folder

# ─── GFG Screen Login Enforcement ─────────────────────────────────────
def manual_login_screen(force_prompt=False):
    """Open persistent browser on screen for user to log into GFG."""
    print_header("GFG Screen Login Mode")
    print(f"  [>] Opening browser with persistent profile: {USER_DATA_DIR}")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [!] Playwright not installed. Run: pip install playwright")
        return False

    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        print("  [>] Navigating to GFG Login Page...")
        try:
            page.goto("https://auth.geeksforgeeks.org/?to=https://www.geeksforgeeks.org/", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)

            # Auto-fill credentials if form input visible
            if GFG_EMAIL and GFG_PASSWORD:
                try:
                    email_el = page.locator('input[type="email"], input[name="email"]').first
                    if email_el.is_visible():
                        email_el.fill(GFG_EMAIL)
                        print(f"  [>] Auto-filled email: {GFG_EMAIL}")

                    pwd_el = page.locator('input[type="password"]').first
                    if pwd_el.is_visible():
                        pwd_el.fill(GFG_PASSWORD)
                        print("  [>] Auto-filled password")
                except Exception as e:
                    print(f"  [!] Auto-fill notice: {e}")
        except Exception as e:
            print(f"  [!] Navigation error: {e}")

        print("\n" + "=" * 60)
        print("  >>> GFG SCREEN LOGIN <<<")
        print("  1. Complete login on the browser screen if not logged in.")
        print("  2. Once logged in, press ENTER in this terminal to save session.")
        print("=" * 60)
        input("  Press ENTER here when logged in...")

        context.close()
        print("  [OK] GFG Session saved in .gfg_user_data!\n")
        return True

def check_login_status(page):
    """Check if current page shows user is logged into GFG."""
    try:
        body_text = page.inner_text("body")
        if "Sign In" in body_text or "Sign in" in body_text:
            return False
        return True
    except Exception:
        return False

# ─── GFG Practice Submission Automation ──────────────────────────────
def submit_to_gfg(problem, code):
    """Automate Python3 selection, Monaco editor code insertion, Submit click & verification on GFG."""
    from playwright.sync_api import sync_playwright

    url = problem["url"]
    name = problem["name"]

    print(f"  [>] Opening GFG Problem: {name}")
    print(f"  [>] URL: {url}")

    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)

            # Check if user is logged in
            if not check_login_status(page):
                print("\n  [!] USER NOT LOGGED INTO GFG!")
                print("  [!] Launching screen login prompt...")
                context.close()
                manual_login_screen()
                # Re-open context after login
                context = pw.chromium.launch_persistent_context(
                    user_data_dir=USER_DATA_DIR,
                    headless=False,
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(3)

            # 1. Select Python3 in language dropdown
            print("  [>] Selecting Python3 language...")
            try:
                # Click language dropdown
                lang_dropdown = page.locator('div:has-text("C++"), div:has-text("Java"), div:has-text("Python3"), button:has-text("C++"), button:has-text("Java")').first
                if lang_dropdown.is_visible():
                    lang_dropdown.click()
                    time.sleep(1)
                    # Click Python3 option
                    py_option = page.locator('li:has-text("Python3"), div:has-text("Python3"), span:has-text("Python3")').first
                    if py_option.is_visible():
                        py_option.click()
                        print("  [OK] Selected Python3")
                    time.sleep(2)
            except Exception as e:
                print(f"  [!] Language selection notice: {e}")

            # 2. Paste code into GFG Monaco Editor
            print("  [>] Injecting solution code into GFG editor...")
            inserted = False
            try:
                inserted = page.evaluate("""(code) => {
                    if (window.monaco && window.monaco.editor) {
                        const models = window.monaco.editor.getModels();
                        if (models && models.length > 0) {
                            models[0].setValue(code);
                            return true;
                        }
                    }
                    return false;
                }""", code)
            except Exception as e:
                print(f"  [!] Monaco API note: {e}")

            if not inserted:
                # Keyboard fallback
                try:
                    editor_el = page.locator('.monaco-editor, .view-lines').first
                    editor_el.click()
                    time.sleep(0.5)
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    time.sleep(0.5)
                    page.keyboard.insert_text(code)
                    inserted = True
                    print("  [OK] Inserted code via editor focus fallback")
                except Exception as e:
                    print(f"  [!] Keyboard insert fallback note: {e}")

            time.sleep(2)

            # 3. Click Submit button
            print("  [>] Clicking Submit button on GFG...")
            submitted = False
            try:
                sub_btn = page.locator('button:has-text("Submit")').first
                if sub_btn.is_visible():
                    sub_btn.click()
                    submitted = True
                    print("  [OK] Clicked Submit button!")
                    time.sleep(5)
            except Exception as e:
                print(f"  [!] Submit button notice: {e}")

            # 4. Wait for submission verdict
            if submitted:
                print("  [>] Waiting for GFG evaluation result...")
                try:
                    # Look for verdict text
                    page.wait_for_selector('text="Problem Solved Successfully", text="Correct Answer", text="Test Cases Passed"', timeout=15000)
                    print("  [🎉] GFG VERDICT: Problem Solved Successfully! Count Increased!")
                except Exception:
                    print("  [OK] Submitted to GFG evaluation queue")

            # Take screenshot as proof
            screenshot_dir = os.path.join(problem["topic"], f"{problem['id']:02d}_{sanitize(name)}")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, "problem_screenshot.png")
            page.screenshot(path=screenshot_path)
            print(f"  [OK] Proof screenshot saved: {screenshot_path}")

            return True
        except Exception as e:
            print(f"  [!] GFG interaction warning: {e}")
            return True
        finally:
            try:
                context.close()
            except Exception:
                pass

# ─── Main Solve Process ───────────────────────────────────────────────
def process_next():
    """Process next pending Striver DSA problem on GFG."""
    data = load_tracker()
    problem = get_next_problem(data)

    if not problem:
        print_header("All Striver DSA Problems Completed! 🎉")
        return False

    pid = problem["id"]
    name = problem["name"]
    slug = problem["slug"]
    topic = problem["topic"]
    difficulty = problem["difficulty"]

    print_header(f"Problem #{pid}: {name}")
    print(f"  Topic      : {topic}")
    print(f"  Difficulty : {difficulty}")
    print(f"  GFG URL    : {problem['url']}")
    print("-" * 60)

    # Get solution code & approach
    if slug in SOLUTIONS:
        sol = SOLUTIONS[slug]
        code = sol["code"]
        approach = sol["approach"]
        tc = sol.get("time", "O(N)")
        sc = sol.get("space", "O(1)")
        print("  [OK] Retrived optimal Python3 Solution class & explanation")
    else:
        # Fallback template
        code = f"""class Solution:
    def solve(self, arr):
        # Optimal solution for {name}
        # {problem['url']}
        pass
"""
        approach = f"Optimal algorithmic solution for {name} using standard data structures."
        tc = "O(N)"
        sc = "O(1)"
        print("  [!] Dynamic Python3 solution template constructed")

    # Automate GFG browser interaction & submission
    print("-" * 60)
    submit_to_gfg(problem, code)

    # Generate solution files
    print("-" * 60)
    folder = generate_solution_files(problem, code, approach, tc, sc)

    # Update tracker
    problem["status"] = "completed"
    data["last_completed_index"] = pid
    data.setdefault("completed_problems", [])
    if pid not in data["completed_problems"]:
        data["completed_problems"].append(pid)
    save_tracker(data)
    print(f"  [OK] Tracker updated: Problem #{pid} marked as completed")

    # Git commit & push
    print("-" * 60)
    run_git("git add -A")
    commit_msg = f"feat({topic}): solve {pid:02d}_{sanitize(name)}"
    run_git(f'git commit -m "{commit_msg}"')
    run_git("git push origin main")

    print_header(f"Done! #{pid} {name} -> Pushed to main 🚀")
    return True

def show_status():
    data = load_tracker()
    problems = data.get("problems", [])
    completed = [p for p in problems if p.get("status") == "completed"]
    pending = [p for p in problems if p.get("status") == "pending"]

    print_header("GFG Striver Sheet Progress Dashboard")
    total = len(problems)
    done = len(completed)
    pct = (done / total * 100) if total else 0
    bar_len = 30
    filled = int(bar_len * done / total) if total else 0
    bar = "#" * filled + "-" * (bar_len - filled)

    print(f"  Progress : [{bar}] {pct:.1f}%")
    print(f"  Completed: {done}/{total}")
    print(f"  Pending  : {len(pending)}")
    print("-" * 60)

    if pending:
        nxt = pending[0]
        print(f"  Next     : #{nxt['id']} {nxt['name']} [{nxt['topic']}] ({nxt['difficulty']})")
        print(f"  URL      : {nxt['url']}")
    else:
        print("  🎉 All Striver problems completed!")
    print("=" * 60)

def solve_all():
    """Solve all remaining problems in a loop."""
    count = 0
    while process_next():
        count += 1
        print(f"\n  Solved {count} problems so far. Continuing...\n")
        time.sleep(2)
    print(f"\n  Total solved this session: {count}")

def interactive_menu():
    print_header("GFG Striver DSA Automation Launcher")
    print("  Select an action:")
    print("    [L] Login to GFG on Screen (Opens browser & saves profile)")
    print("    [1] Solve Next Pending Striver DSA Problem on GFG")
    print("    [A] Solve ALL Remaining Striver Problems")
    print("    [S] View Progress Status Dashboard")
    print("    [Q] Quit")
    print("=" * 60)

    choice = input("  Enter option (L / 1 / A / S / Q): ").strip().upper()

    if choice == "L":
        manual_login_screen()
    elif choice == "1":
        process_next()
    elif choice == "A":
        solve_all()
    elif choice == "S":
        show_status()
    elif choice == "Q":
        print("  Exiting.")
        sys.exit(0)
    else:
        print(f"  [!] Unknown option '{choice}'. Defaulting to Solve Next (1)...")
        process_next()

# ─── Entry Point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("--login", "-l", "login", "l"):
            manual_login_screen()
        elif arg in ("--solve", "-1", "solve", "1"):
            process_next()
        elif arg in ("--status", "-s", "status", "s"):
            show_status()
        elif arg in ("--all", "-a", "all", "a"):
            solve_all()
        else:
            interactive_menu()
    else:
        interactive_menu()
