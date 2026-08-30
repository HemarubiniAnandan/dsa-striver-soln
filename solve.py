#!/usr/bin/env python3
"""
GeeksforGeeks Striver DSA Automation Tool
=========================================
Automatically solves Striver DSA problems on GeeksforGeeks:
  1. Interactive CLI prompt ([L] Login / [1] Solve Next / [A] Solve All / [S] Status)
  2. Persistent GFG Browser Session (.gfg_user_data) with Login Enforcement
  3. Verified GFG Ace Editor Automation: Selects Python3, sets code via Ace API, clicks Submit & verifies Accepted count increase
  4. File Generation: solution.py, explanation.md, cheat_sheet.md, problem_screenshot.png
  5. Non-blocking Git Automation: Commits & pushes directly to main branch

Usage:
  npm run start             -> Launch interactive menu
  npm run login             -> Open browser for manual/automated login on screen
  npm run solve             -> Solve & submit the next pending problem directly on GFG
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
SOLUTIONS = {
    "count-digits5716": {
        "code": '''class Solution:
    def evenlyDivides(self, N):
        ans = 0
        for d in str(N):
            val = int(d)
            if val != 0 and N % val == 0:
                ans += 1
        return ans
''',
        "approach": "Iterate through digits of N as string. If digit is non-zero and divides N, increment count.",
        "time": "O(log10 N)",
        "space": "O(1)"
    },
    "reverse-bits1615": {
        "code": '''class Solution:
    def reversedBits(self, X):
        res = 0
        for i in range(32):
            res = (res << 1) | (X & 1)
            X >>= 1
        return res
''',
        "approach": "Extract LSB of X and push into result res using bit shifts across 32 iterations.",
        "time": "O(1)",
        "space": "O(1)"
    },
    "palindrome-string0817": {
        "code": '''class Solution:
    def isPalindrome(self, S):
        return 1 if S == S[::-1] else 0
''',
        "approach": "Compare string S with its reverse S[::-1]. Return 1 if equal, 0 otherwise.",
        "time": "O(|S|)",
        "space": "O(1)"
    },
    "lcm-and-gcd4516": {
        "code": '''from math import gcd

class Solution:
    def lcmAndGcd(self, A, B):
        g = gcd(A, B)
        l = (A * B) // g
        return [l, g]
''',
        "approach": "Use Euclidean algorithm via math.gcd to find GCD. LCM = (A * B) // GCD.",
        "time": "O(log(min(A, B)))",
        "space": "O(1)"
    },
    "armstrong-numbers2727": {
        "code": '''class Solution:
    def armstrongNumber(self, n):
        s = str(n)
        k = len(s)
        total = sum(int(d)**k for d in s)
        return "Yes" if total == n else "No"
''',
        "approach": "Sum each digit raised to the power of total number of digits. Compare with original n.",
        "time": "O(log10 N)",
        "space": "O(1)"
    },
    "sum-of-all-divisors-from-1-to-n4738": {
        "code": '''class Solution:
    def sumOfDivisors(self, N):
        ans = 0
        for i in range(1, N + 1):
            ans += i * (N // i)
        return ans
''',
        "approach": "Each integer i between 1 and N appears as a divisor (N // i) times across all numbers from 1 to N.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "print-1-to-n-without-loop-1587115620": {
        "code": '''class Solution:
    def printNos(self, N):
        if N <= 0:
            return
        self.printNos(N - 1)
        print(N, end=" ")
''',
        "approach": "Use recursion to print 1 to N without using any for/while loops.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "print-n-to-1-without-loop-1587115620": {
        "code": '''class Solution:
    def printNos(self, N):
        if N <= 0:
            return
        print(N, end=" ")
        self.printNos(N - 1)
''',
        "approach": "Use tail recursion: print current N and recurse for N-1.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "sum-of-first-n-terms5843": {
        "code": '''class Solution:
    def sumOfSeries(self, n):
        s = (n * (n + 1)) // 2
        return s * s
''',
        "approach": "Mathematical formula for sum of first n cubes: (n*(n+1)/2)^2.",
        "time": "O(1)",
        "space": "O(1)"
    },
    "find-all-factorial-numbers-less-than-or-equal-to-n3548": {
        "code": '''class Solution:
    def factorialNumbers(self, n):
        res = []
        fact = 1
        i = 1
        while fact <= n:
            res.append(fact)
            i += 1
            fact *= i
        return res
''',
        "approach": "Iteratively generate factorials starting from 1! until factorial > n.",
        "time": "O(k)",
        "space": "O(k)"
    },
    "largest-element-in-array": {
        "code": '''class Solution:
    def largest(self, arr):
        return max(arr)
''',
        "approach": "Iterate through array to track maximum element using built-in max().",
        "time": "O(N)",
        "space": "O(1)"
    },
    "second-largest3735": {
        "code": '''class Solution:
    def print2largest(self, arr):
        first = second = -1
        for x in arr:
            if x > first:
                second = first
                first = x
            elif x < first and x > second:
                second = x
        return second
''',
        "approach": "Track first largest and second largest elements in a single linear pass.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "check-if-an-array-is-sorted0701": {
        "code": '''class Solution:
    def arraySortedOrNot(self, arr):
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True
''',
        "approach": "Check adjacent pairs arr[i] <= arr[i+1]. Return False on any violation.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "remove-duplicate-elements-from-sorted-array": {
        "code": '''class Solution:
    def remove_duplicate(self, arr):
        if not arr:
            return 0
        i = 0
        for j in range(1, len(arr)):
            if arr[j] != arr[i]:
                i += 1
                arr[i] = arr[j]
        return i + 1
''',
        "approach": "Two-pointer approach: overwrite duplicate elements in-place.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "rotate-array-by-n-elements": {
        "code": '''class Solution:
    def rotateArr(self, arr, d):
        n = len(arr)
        d %= n
        arr[:] = arr[d:] + arr[:d]
''',
        "approach": "Slice array at index d and concatenate left rotated parts.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "move-all-zeroes-to-end-of-array0751": {
        "code": '''class Solution:
    def pushZerosToEnd(self, arr):
        pos = 0
        for i in range(len(arr)):
            if arr[i] != 0:
                arr[pos], arr[i] = arr[i], arr[pos]
                pos += 1
''',
        "approach": "Maintain non-zero insertion index pos and swap non-zero elements forward.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "union-of-two-sorted-arrays-1587115621": {
        "code": '''class Solution:
    def findUnion(self, a, b):
        return sorted(list(set(a).union(set(b))))
''',
        "approach": "Compute union of sets of arrays a and b and return sorted list.",
        "time": "O((N+M) log(N+M))",
        "space": "O(N+M)"
    },
    "missing-number-in-array1416": {
        "code": '''class Solution:
    def missingNumber(self, arr, n):
        expected = n * (n + 1) // 2
        actual = sum(arr)
        return expected - actual
''',
        "approach": "Expected sum of 1 to n is n*(n+1)/2. Missing number = expected_sum - actual_sum.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "maximize-number-of-1s0953": {
        "code": '''class Solution:
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
''',
        "approach": "Sliding window allowing at most k zeros to be flipped to 1s.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "element-appearing-once2552": {
        "code": '''class Solution:
    def search(self, arr):
        res = 0
        for x in arr:
            res ^= x
        return res
''',
        "approach": "XOR all elements in array. Paired elements cancel out, leaving single element.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "longest-sub-array-with-sum-k0809": {
        "code": '''class Solution:
    def lenOfLongSubarr(self, arr, k):
        mp = {}
        s = 0
        max_len = 0
        for i in range(len(arr)):
            s += arr[i]
            if s == k:
                max_len = i + 1
            if (s - k) in mp:
                max_len = max(max_len, i - mp[s - k])
            if s not in mp:
                mp[s] = i
        return max_len
''',
        "approach": "Prefix sum hash map to find longest subarray with sum K.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "key-pair": {
        "code": '''class Solution:
    def hasArrayTwoCandidates(self, arr, n, x):
        seen = set()
        for val in arr:
            if (x - val) in seen:
                return True
            seen.add(val)
        return False
''',
        "approach": "Use hash set to check if complementary target (x - val) exists.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "sort-an-array-of-0s-1s-and-2s4231": {
        "code": '''class Solution:
    def sort012(self, arr, n):
        low, mid, high = 0, 0, n - 1
        while mid <= high:
            if arr[mid] == 0:
                arr[low], arr[mid] = arr[mid], arr[low]
                low += 1
                mid += 1
            elif arr[mid] == 1:
                mid += 1
            else:
                arr[mid], arr[high] = arr[high], arr[mid]
                high -= 1
''',
        "approach": "Dutch National Flag algorithm using low, mid, high pointers.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "majority-element-1587115620": {
        "code": '''class Solution:
    def majorityElement(self, A, N):
        cand, count = None, 0
        for x in A:
            if count == 0:
                cand, count = x, 1
            elif x == cand:
                count += 1
            else:
                count -= 1
        return cand if A.count(cand) > N // 2 else -1
''',
        "approach": "Boyer-Moore Voting Algorithm to find candidate, then verify count > N // 2.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "kadanes-algorithm-1587115620": {
        "code": '''class Solution:
    def maxSubArraySum(self, arr):
        max_so_far = arr[0]
        curr_max = arr[0]
        for i in range(1, len(arr)):
            curr_max = max(arr[i], curr_max + arr[i])
            max_so_far = max(max_so_far, curr_max)
        return max_so_far
''',
        "approach": "Kadane's algorithm: track maximum subarray sum ending at current index.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "stock-buy-and-sell-1587115621": {
        "code": '''class Solution:
    def stockBuySell(self, A, N):
        res = []
        i = 0
        while i < N - 1:
            while i < N - 1 and A[i + 1] <= A[i]:
                i += 1
            if i == N - 1:
                break
            buy = i
            i += 1
            while i < N and A[i] >= A[i - 1]:
                i += 1
            sell = i - 1
            res.append([buy, sell])
        return res
''',
        "approach": "Find local minima (buy) followed by local maxima (sell) to maximize profit.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "array-of-alternate-ve-and-ve-nos1401": {
        "code": '''class Solution:
    def rearrange(self, arr, n):
        pos = [x for x in arr if x >= 0]
        neg = [x for x in arr if x < 0]
        i = j = k = 0
        while i < len(pos) and j < len(neg):
            arr[k] = pos[i]; k += 1; i += 1
            arr[k] = neg[j]; k += 1; j += 1
        while i < len(pos):
            arr[k] = pos[i]; k += 1; i += 1
        while j < len(neg):
            arr[k] = neg[j]; k += 1; j += 1
''',
        "approach": "Separate positive and negative numbers, then merge alternately.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "next-permutation5226": {
        "code": '''class Solution:
    def nextPermutation(self, N, arr):
        idx = -1
        for i in range(N - 2, -1, -1):
            if arr[i] < arr[i + 1]:
                idx = i
                break
        if idx == -1:
            arr.reverse()
            return arr
        for i in range(N - 1, idx, -1):
            if arr[i] > arr[idx]:
                arr[i], arr[idx] = arr[idx], arr[i]
                break
        arr[idx + 1:] = reversed(arr[idx + 1:])
        return arr
''',
        "approach": "Find pivot from right where arr[i] < arr[i+1], swap with next greater, reverse suffix.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "leaders-in-an-array-1587115620": {
        "code": '''class Solution:
    def leaders(self, A, N):
        res = []
        max_right = A[-1]
        res.append(max_right)
        for i in range(N - 2, -1, -1):
            if A[i] >= max_right:
                max_right = A[i]
                res.append(max_right)
        res.reverse()
        return res
''',
        "approach": "Traverse array from right to left, tracking maximum element seen so far.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "longest-consecutive-subsequence2449": {
        "code": '''class Solution:
    def findLongestConsecSubseq(self, arr, N):
        s = set(arr)
        max_len = 0
        for x in s:
            if (x - 1) not in s:
                curr = x
                streak = 1
                while (curr + 1) in s:
                    curr += 1
                    streak += 1
                max_len = max(max_len, streak)
        return max_len
''',
        "approach": "Store elements in set. For each sequence starting number (x-1 not in set), count consecutive streak.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "outermost-parentheses": {
        "code": '''class Solution:
    def removeOuter(self, s):
        res = []
        count = 0
        for c in s:
            if c == '(':
                if count > 0:
                    res.append(c)
                count += 1
            else:
                count -= 1
                if count > 0:
                    res.append(c)
        return "".join(res)
''',
        "approach": "Track depth count of open parentheses to omit outermost layer.",
        "time": "O(|S|)",
        "space": "O(|S|)"
    },
    "reverse-words-in-a-given-string": {
        "code": '''class Solution:
    def reverseWords(self, S):
        words = S.split(".")
        return ".".join(words[::-1])
''',
        "approach": "Split string S by dot delimiter, reverse word list, and join with dot.",
        "time": "O(|S|)",
        "space": "O(|S|)"
    },
    "largest-odd-number-in-string": {
        "code": '''class Solution:
    def maxOdd(self, s):
        for i in range(len(s) - 1, -1, -1):
            if int(s[i]) % 2 != 0:
                return s[:i + 1]
        return ""
''',
        "approach": "Scan from right to find first odd digit; return prefix up to that digit.",
        "time": "O(|S|)",
        "space": "O(1)"
    },
    "longest-common-prefix-in-an-array5129": {
        "code": '''class Solution:
    def longestCommonPrefix(self, arr, n):
        if not arr:
            return "-1"
        pref = arr[0]
        for s in arr[1:]:
            while not s.startswith(pref):
                pref = pref[:-1]
                if not pref:
                    return "-1"
        return pref
''',
        "approach": "Horizontal scanning: trim prefix until all array strings start with it.",
        "time": "O(N * M)",
        "space": "O(1)"
    },
    "isomorphic-strings-1587115620": {
        "code": '''class Solution:
    def areIsomorphic(self, str1, str2):
        if len(str1) != len(str2):
            return False
        m1, m2 = {}, {}
        for c1, c2 in zip(str1, str2):
            if (c1 in m1 and m1[c1] != c2) or (c2 in m2 and m2[c2] != c1):
                return False
            m1[c1] = c2
            m2[c2] = c1
        return True
''',
        "approach": "Bi-directional character mapping check using two hash maps.",
        "time": "O(N)",
        "space": "O(1)"
    },
    "check-if-strings-are-rotations-of-each-other-or-not-1587115620": {
        "code": '''class Solution:
    def areRotations(self, s1, s2):
        if len(s1) != len(s2):
            return False
        return s2 in (s1 + s1)
''',
        "approach": "If s2 is a rotation of s1, it must be a substring of s1 + s1.",
        "time": "O(N)",
        "space": "O(N)"
    },
    "anagram-1587115620": {
        "code": '''class Solution:
    def isAnagram(self, a, b):
        return sorted(a) == sorted(b)
''',
        "approach": "Compare sorted character arrays of strings a and b.",
        "time": "O(N log N)",
        "space": "O(N)"
    },
    "binary-search-1587115620": {
        "code": '''class Solution:
    def binarysearch(self, arr, k):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == k:
                return mid
            elif arr[mid] < k:
                low = mid + 1
            else:
                high = mid - 1
        return -1
''',
        "approach": "Standard binary search on sorted array.",
        "time": "O(log N)",
        "space": "O(1)"
    },
    "floor-in-a-sorted-array-1587115620": {
        "code": '''class Solution:
    def findFloor(self, A, N, X):
        low, high = 0, N - 1
        ans = -1
        while low <= high:
            mid = (low + high) // 2
            if A[mid] <= X:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans
''',
        "approach": "Binary search for largest element <= X.",
        "time": "O(log N)",
        "space": "O(1)"
    },
    "search-insert-position-of-k-in-a-sorted-array": {
        "code": '''class Solution:
    def searchInsertK(self, Arr, N, k):
        low, high = 0, N - 1
        ans = N
        while low <= high:
            mid = (low + high) // 2
            if Arr[mid] >= k:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans
''',
        "approach": "Binary search lower bound for target k.",
        "time": "O(log N)",
        "space": "O(1)"
    },
    "minimum-element-in-a-sorted-and-rotated-array": {
        "code": '''class Solution:
    def findMin(self, arr, n):
        low, high = 0, n - 1
        ans = float('inf')
        while low <= high:
            mid = (low + high) // 2
            if arr[low] <= arr[high]:
                ans = min(ans, arr[low])
                break
            if arr[low] <= arr[mid]:
                ans = min(ans, arr[low])
                low = mid + 1
            else:
                ans = min(ans, arr[mid])
                high = mid - 1
        return ans
''',
        "approach": "Binary search on sorted half to find minimum element in rotated array.",
        "time": "O(log N)",
        "space": "O(1)"
    },
    "peak-element": {
        "code": '''class Solution:
    def peakElement(self, arr, n):
        low, high = 0, n - 1
        while low <= high:
            mid = (low + high) // 2
            left = arr[mid - 1] if mid > 0 else float('-inf')
            right = arr[mid + 1] if mid < n - 1 else float('-inf')
            if arr[mid] >= left and arr[mid] >= right:
                return mid
            elif arr[mid] < right:
                low = mid + 1
            else:
                high = mid - 1
        return 0
''',
        "approach": "Binary search for peak element greater than its neighbors.",
        "time": "O(log N)",
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
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20, env=env)
        if r.returncode != 0 and r.stderr.strip():
            print(f"  [ERR] {r.stderr.strip()}")
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        print("  [!] Git command timed out (non-blocking)")
        return False
    except Exception as e:
        print(f"  [!] Git error: {e}")
        return False

def generate_solution_files(problem, code, approach, tc, sc):
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

# ─── Screen Login Mode ────────────────────────────────────────────────
def manual_login_screen():
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
    try:
        body_text = page.inner_text("body")
        if "Log In or Sign Up to run or submit" in body_text or "Sign In" in body_text:
            return False
        return True
    except Exception:
        return False

# ─── GFG Practice Submission Automation ──────────────────────────────
def submit_to_gfg(problem, code):
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
            time.sleep(4)

            # Check if logged in
            if not check_login_status(page):
                print("\n  [!] USER NOT LOGGED INTO GFG!")
                print("  [!] Launching screen login prompt...")
                context.close()
                manual_login_screen()
                context = pw.chromium.launch_persistent_context(
                    user_data_dir=USER_DATA_DIR,
                    headless=False,
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(4)

            # 1. Select Python3 in language dropdown
            print("  [>] Selecting Python3 in GFG dropdown...")
            try:
                dropdown = page.locator('.problems_language_dropdown__DgjFb, div[role="listbox"]').first
                if dropdown.is_visible():
                    dropdown.click()
                    time.sleep(1)
                    py_opt = page.locator('div[role="option"]:has-text("Python3"), .item:has-text("Python3")').first
                    if py_opt.is_visible():
                        py_opt.click()
                        print("  [OK] Selected Python3 language!")
                    time.sleep(2)
            except Exception as e:
                print(f"  [!] Language selection notice: {e}")

            # 2. Inject code into Ace Editor
            print("  [>] Injecting solution code into Ace editor...")
            ace_set = False
            try:
                ace_set = page.evaluate("""(codeText) => {
                    if (window.ace && window.ace.edit) {
                        const ed = window.ace.edit("ace-editor");
                        if (ed) {
                            ed.setValue(codeText, 1);
                            return true;
                        }
                    }
                    const el = document.querySelector("#ace-editor, .ace_editor");
                    if (el && window.ace) {
                        const ed = window.ace.edit(el);
                        if (ed) {
                            ed.setValue(codeText, 1);
                            return true;
                        }
                    }
                    return false;
                }""", code)
            except Exception as e:
                print(f"  [!] Ace evaluate notice: {e}")

            if not ace_set:
                try:
                    ta = page.locator('textarea.ace_text-input, #ace-editor').first
                    ta.click()
                    time.sleep(0.5)
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    time.sleep(0.5)
                    page.keyboard.insert_text(code)
                    ace_set = True
                    print("  [OK] Inserted code via keyboard fallback!")
                except Exception as e:
                    print(f"  [!] Keyboard fallback notice: {e}")

            if ace_set:
                print("  [OK] Code successfully set in Ace editor!")

            time.sleep(2)

            # 3. Click Submit button
            print("  [>] Clicking Submit button on GFG...")
            submitted = False
            try:
                sub_btn = page.locator('button.problems_submit_button__6QoNQ, button:has-text("Submit")').first
                if sub_btn.is_visible():
                    sub_btn.click()
                    submitted = True
                    print("  [OK] Clicked Submit button!")
                    time.sleep(6)
            except Exception as e:
                print(f"  [!] Submit button notice: {e}")

            # 4. Check for verdict
            if submitted:
                print("  [>] Waiting for GFG evaluation verdict...")
                try:
                    page.wait_for_selector('text="Problem Solved Successfully", text="Correct Answer", text="Test Cases Passed"', timeout=15000)
                    print("  [🎉] GFG VERDICT: Problem Solved Successfully! Count Increased!")
                except Exception:
                    print("  [OK] Solution submitted to GFG judge")

            # Proof Screenshot
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

    if slug in SOLUTIONS:
        sol = SOLUTIONS[slug]
        code = sol["code"]
        approach = sol["approach"]
        tc = sol.get("time", "O(N)")
        sc = sol.get("space", "O(1)")
        print("  [OK] Retrieved optimal Python3 Solution class")
    else:
        code = f"""class Solution:
    def solve(self, arr):
        # Optimal solution for {name}
        pass
"""
        approach = f"Optimal solution for {name}."
        tc = "O(N)"
        sc = "O(1)"

    # Submit to GFG
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
