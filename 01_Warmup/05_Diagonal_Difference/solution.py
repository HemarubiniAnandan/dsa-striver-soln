def diagonalDifference(arr):
    n = len(arr)
    d1 = sum(arr[i][i] for i in range(n))
    d2 = sum(arr[i][n - 1 - i] for i in range(n))
    return abs(d1 - d2)

if __name__ == '__main__':
    n = int(input())
    arr = [list(map(int, input().split())) for _ in range(n)]
    print(diagonalDifference(arr))
