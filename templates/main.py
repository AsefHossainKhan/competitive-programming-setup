import sys
input = sys.stdin.readline


def main():
    data = sys.stdin.read().split()
    it = iter(data)

    # Example: read first number if needed
    # n = int(next(it))

    print(data)


if __name__ == "__main__":
    main()
