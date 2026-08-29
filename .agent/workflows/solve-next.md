---
description: Automatically solve the next Striver DSA problem from HackerRank, create solutions & documentation, and push directly to GitHub main branch.
---

1. Open `striver_sheet_tracker.json` and identify the next problem with status `"pending"`.
2. Extract the problem's ID, topic, name, slug, and HackerRank URL.
3. Navigate to the HackerRank URL in the browser to inspect problem details and test cases.
4. Derive the optimal Python 3 solution and write it to `<Topic>/<ID>_<Problem_Name>/solution.py`.
5. Write detailed problem analysis to `<Topic>/<ID>_<Problem_Name>/explanation.md`.
6. Write summary notes and key takeaways to `<Topic>/<ID>_<Problem_Name>/cheat_sheet.md`.
7. Run a local Python test to verify that `solution.py` functions correctly.
8. Update `striver_sheet_tracker.json` setting `status: "completed"` and incrementing `last_completed_index`.
// turbo
9. Run `git add -A`
// turbo
10. Run `git commit -m "feat(<Topic>): solve <Problem_Name>"`
// turbo
11. Run `git push origin main`
