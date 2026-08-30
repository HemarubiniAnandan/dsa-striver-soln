---
description: Automatically solve the next Striver DSA problem on GeeksforGeeks, generate solutions & documentation, and push directly to GitHub main branch.
---

1. Run `yarn start` (or `python solve.py`) to launch the interactive prompt.
2. If logging in for the first time, select `L` to open the visible browser, log into GeeksforGeeks, and press ENTER in the terminal to save session context to `.gfg_user_data`.
3. Select `1` (or run `yarn solve`) to pick the next pending Striver problem from `striver_sheet_tracker.json`.
4. The tool extracts optimal Python 3 code and detailed complexity explanations.
5. The solution code is written to `<Topic>/<ID>_<Problem_Name>/solution.py`.
6. Detailed problem documentation is saved to `<Topic>/<ID>_<Problem_Name>/explanation.md`.
7. Quick revision notes are saved to `<Topic>/<ID>_<Problem_Name>/cheat_sheet.md`.
8. Updates `striver_sheet_tracker.json` marking status as `"completed"`.
// turbo
9. Run `git add -A`
// turbo
10. Run `git commit -m "feat(<Topic>): solve <ID>_<Problem_Name>"`
// turbo
11. Run `git push origin main`
