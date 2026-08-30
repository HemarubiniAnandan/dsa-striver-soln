from math import gcd

class Solution:
    def lcmAndGcd(self, A, B):
        g = gcd(A, B)
        l = (A * B) // g
        return [l, g]
