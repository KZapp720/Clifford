from __future__  import annotations
from typing      import List, Tuple

Scalar = int | float | complex


class Blade:
    @staticmethod
    def ordinal(index: str) -> int:
        return ord(index) - ord('1')

    def __init__(self: Blade, indices: str, scalar: Scalar, metric: Tuple[int, int, int]) -> None:
        if any((index := i) not in "123456789" for i in indices):
            raise ValueError(f"Invalid index passed to Blade constructor: '{index}'")

        if any(not isinstance(m, int) or m < 0 for m in metric):
            raise ValueError(f"Metric must be a tuple of non-negative integers: {metric}")
        
        if sum(metric) > 9:
            raise ValueError("Metric cannot exceed 9 dimensions")
        
        p, q, r      = metric
        self.indices = indices
        self.scalar  = scalar
        self._metric = metric
        self._forms  = [1] * p + [-1] * q + [0] * r
        self.reduce()

    def reduce(self: Blade) -> None:
        # sorts the indices and multiplies the scalar by -1 for each transposition
        indices = list(self.indices)
        for i in range(len(indices)):
            for j in range(len(indices) - i - 1):
                if self.ordinal(indices[j]) > self.ordinal(indices[j + 1]):
                    indices[j], indices[j + 1] = indices[j + 1], indices[j]
                    self.scalar *= -1

        # edge cases for the while loop below
        if len(self._forms) == 0 and self.indices != "":
            raise ValueError("Index out of bounds for metric forms")
        if len(self._forms) == 1 and self.indices not in ("", "1"):
            raise ValueError("Index out of bounds for metric forms")
        if len(self.indices) == 1 and int(self.indices) > len(self._forms):
            raise ValueError("Index out of bounds for metric forms")

        # reduces quadratic forms to their metric
        i = 0
        while i < len(indices) - 1:
            left  = self.ordinal(indices[i])
            right = self.ordinal(indices[i + 1])
            if left >= len(self._forms) or right >= len(self._forms):
                raise ValueError("Index out of bounds for metric forms")
            if left == right:
                match self._forms[left]:
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

    def __add__(self: Blade, other: Scalar | Blade | Cliff) -> Blade:
        if isinstance(other, Scalar):
            return self # TODO returns a Cliff
        elif isinstance(other, Blade):
            if self._metric != other._metric:
              raise ValueError("Cannot add Blades with different metric signatures")
            if self.indices != other.indices:
              return self # TODO returns a Cliff
            return Blade(self.indices, self.scalar + other.scalar, self._metric)
        elif isinstance(other, Cliff):
            if self._metric != other._metric:
              raise ValueError("Cannot add Blade and Cliff with different metric signatures")
            return self # TODO returns a Cliff
        else:
            raise ValueError(f"Blade class does not support addition with type {type(other)}")


class Cliff:
    def __init__(self: Cliff, blades: Cliff | List[Blade] | Blade | Scalar, metric: Tuple[int, int, int] | None = None) -> None:
        match (blades, metric):
            case (cliff, None)       if isinstance(cliff, Cliff):
                self.blades  = cliff.blades
                self._metric = cliff._metric
            case (cliff, (p, q, r))  if isinstance(cliff, Cliff) and p >= 0 and q >= 0 and r >= 0:
                if (p, q, r) != cliff._metric:
                    raise ValueError(f"Mismatched metric signature passed to Cliff initializer: {cliff._metric} ≠ ({p}, {q}, {r})")
                self.blades  = cliff.blades
                self._metric = cliff._metric
            case ([], None):
                pass
            case ([], (p, q, r))     if p >= 0 and q >= 0 and r >= 0:
                pass
            case (xs, None)          if isinstance(xs, list):
                pass
            case (xs, (p, q, r))     if isinstance(xs, list) and p >= 0 and q >= 0 and r >= 0:
                pass
            case (x, None)           if isinstance(x, Blade):
                pass
            case (x, (p, q, r))      if isinstance(x, Blade) and p >= 0 and q >= 0 and r >= 0:
                pass
            case (x, None)           if isinstance(x, Scalar):
                pass
            case (x, (p, q, r))      if isinstance(x, Scalar) and p >= 0 and q >= 0 and r >= 0:
                pass
            case _:
                pass


def clifford(p: int, q: int, r: int) -> None:
    pass


def main() -> None:
    print("Hello World")
    x = Blade("2", 1, (1, 0, 0))
    print(x)


if __name__ == "__main__":
    main()

