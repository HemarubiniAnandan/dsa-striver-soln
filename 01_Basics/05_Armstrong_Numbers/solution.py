class Solution:
    def armstrongNumber(self, n):
        s = str(n)
        k = len(s)
        total = sum(int(d)**k for d in s)
        return "Yes" if total == n else "No"
