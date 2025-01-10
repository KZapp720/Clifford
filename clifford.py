from dataclasses import dataclass
from typing      import Self


Scalar = int | float | complex


class Blade:
    @staticmethod
    def ordinal(index: str) -> int:
        return ord(index) - ord('1')

    def __init__(self: Self, indices: str, scalar: Scalar, metric: (int, int, int)) -> Self:
        for index in indices:
            if index not in "123456789":
                raise ValueError(f"Invalid character in indices: '{index}'")

        if not all(isinstance(x, int) and x >= 0 for x in metric):
            raise ValueError("Metric must be a tuple of non-negative integers")

        p, q, r      = metric
        self.indices = indices
        self.scalar  = scalar
        self.metric  = metric
        self.forms   = [1] * p + [-1] * q + [0] * r
        self.reduce()

    def reduce(self: Self) -> None:
        # sorts the indices and multplies the scalar by -1 for each transposition
        indices = list(self.indices)
        for i in range(len(indices)):
            for j in range(len(indices) - i - 1):
                if self.ordinal(indices[j]) > self.ordinal(indices[j + 1]):
                    indices[j], indices[j + 1] = indices[j + 1], indices[j]
                    self.scalar *= -1

        # reduces quadratic forms to their metric
        i = 0
        while i < len(indices) - 1:
            left  = self.ordinal(indices[i])
            right = self.ordinal(indices[i + 1])
            if left >= len(self.forms) or right >= len(self.forms):
                raise ValueError("Index out of bounds for metric forms")
            if left == right:
                match self.forms[left]:
                    case 0:
                        self.scalar = 0
                        self.indices = ""
                        return
                    case -1:
                        self.scalar *= -1
                indices = indices[:i] + indices[i + 2:]
            else:
                i += 1

        self.indices = "".join(indices)


class Cliff:
    def __init__(self: Self, blades: [Blade], metric: (int, int, int)) -> Self:
        pass


def clifford(p: int, q: int, r: int) -> None:
    pass


def main() -> None:
    print("Hello World")


if __name__ == "__main__":
    main()
