class Solution:
    def isPalindrome(self, S):
        return 1 if S == S[::-1] else 0
