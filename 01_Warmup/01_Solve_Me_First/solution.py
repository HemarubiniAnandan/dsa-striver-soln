def solveMeFirst(a: int, b: int) -> int:
    """
    Computes the sum of two integers.

    Parameters:
    a (int): First integer (1 <= a <= 1000)
    b (int): Second integer (1 <= b <= 1000)

    Returns:
    int: Sum of a and b
    """
    return a + b


if __name__ == '__main__':
    num1 = int(input())
    num2 = int(input())
    res = solveMeFirst(num1, num2)
    print(res)
