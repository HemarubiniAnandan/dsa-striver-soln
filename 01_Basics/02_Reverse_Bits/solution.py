class Solution:
    def reversedBits(self, X):
        res = 0
        for i in range(32):
            res = (res << 1) | (X & 1)
            X >>= 1
        return res
