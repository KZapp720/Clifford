from typing import Self


Scalar = int | float | complex


class Blade:
    def __init__(self: Self, indices: str, scalar: Scalar, metric: (int, int, int)) -> Self:
        pass


class Cliff:
    def __init__(self: Self, blades: [Blade], metric: (int, int, int)) -> Self:
        pass


def main():
    print("Hello World")


if __name__ == "__main__":
    main()
