class Solution:
    def sumOfDivisors(self, N):
        ans = 0
        for i in range(1, N + 1):
            ans += i * (N // i)
        return ans
