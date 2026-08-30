class Solution:
    def evenlyDivides(self, N):
        count = 0
        for d in str(N):
            val = int(d)
            if val != 0 and N % val == 0:
                count += 1
        return count
