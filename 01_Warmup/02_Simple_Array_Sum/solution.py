def simpleArraySum(ar):
    """
    Computes the sum of an array of integers.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    return sum(ar)

if __name__ == '__main__':
    _ = int(input())
    ar = list(map(int, input().rstrip().split()))
    result = simpleArraySum(ar)
    print(result)
