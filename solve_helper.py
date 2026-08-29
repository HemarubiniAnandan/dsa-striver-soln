import json
import os
import sys

TRACKER_FILE = "striver_sheet_tracker.json"

def load_tracker():
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tracker(data):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_next_problem():
    data = load_tracker()
    for problem in data.get("problems", []):
        if problem.get("status") == "pending":
            return problem
    return None

def mark_completed(problem_id):
    data = load_tracker()
    found = False
    for problem in data.get("problems", []):
        if problem.get("id") == problem_id:
            problem["status"] = "completed"
            found = True
            break
    if found:
        data["last_completed_index"] = problem_id
        if problem_id not in data.get("completed_problems", []):
            data.setdefault("completed_problems", []).append(problem_id)
        save_tracker(data)
        print(f"Problem {problem_id} marked as completed.")
    else:
        print(f"Problem {problem_id} not found.")

def print_status():
    data = load_tracker()
    problems = data.get("problems", [])
    completed = [p for p in problems if p.get("status") == "completed"]
    pending = [p for p in problems if p.get("status") == "pending"]
    print(f"Total Problems: {len(problems)}")
    print(f"Completed: {len(completed)}")
    print(f"Pending: {len(pending)}")
    next_p = get_next_problem()
    if next_p:
        print(f"Next Pending: #{next_p['id']} - {next_p['name']} ({next_p['topic']})")
    else:
        print("All problems completed!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "next":
            p = get_next_problem()
            if p:
                print(json.dumps(p, indent=2))
            else:
                print("No pending problem.")
        elif cmd == "complete" and len(sys.argv) > 2:
            mark_completed(int(sys.argv[2]))
        elif cmd == "status":
            print_status()
    else:
        print_status()
