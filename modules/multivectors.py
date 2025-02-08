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

    def __add__(self: Blade, other: Scalar | Blade | Cliff) -> Blade | Cliff:
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
    Forms       = List[Blade] | List[str] | Blade | str | Scalar
    MaybeMetric = Tuple[int, int, int] | None

    def __init__(self: Cliff, blades: Cliff | Forms, metric: MaybeMetric = None):
        def validate_metric(metric):
            return metric and all(isinstance(x, int) and x >= 0 for x in metric)

        def check_metric_consistency(existing_metric, new_metric):
            if existing_metric != new_metric:
                raise ValueError(f"Mismatched metric signature: {existing_metric} ≠ {new_metric}")

        match (blades, metric):
            case (cliff, None) if isinstance(cliff, Cliff):
                self.blades, self._metric = cliff.blades, cliff._metric

            case (cliff, (p, q, r)) if isinstance(cliff, Cliff) and validate_metric((p, q, r)):
                check_metric_consistency(cliff._metric, (p, q, r))
                self.blades, self._metric = cliff.blades, cliff._metric

            case (xs, None) if isinstance(xs, list) and all(isinstance(b, Blade) for b in xs):
                self.blades, self._metric = xs, xs[0]._metric if xs else [Blade("", 1, (3, 0, 0))], (3, 0, 0)

            case (xs, (p, q, r)) if isinstance(xs, list) and all(isinstance(b, Blade) for b in xs) and validate_metric((p, q, r)):
                for blade in xs:
                    check_metric_consistency(blade._metric, (p, q, r))
                self.blades, self._metric = xs, (p, q, r)

            case (xs, None) if isinstance(xs, list) and all(isinstance(s, str) for s in xs):
                raise ValueError("Must supply metric when passing a list of strings")

            case (xs, (p, q, r)) if isinstance(xs, list) and all(isinstance(s, str) for s in xs) and validate_metric((p, q, r)):
                self.blades = [Blade(name, 1, (p, q, r)) for name in xs]
                self._metric = (p, q, r)

            case (blade, None) if isinstance(blade, Blade):
                self.blades, self._metric = [blade], blade._metric

            case (blade, (p, q, r)) if isinstance(blade, Blade) and validate_metric((p, q, r)):
                check_metric_consistency(blade._metric, (p, q, r))
                self.blades, self._metric = [blade], (p, q, r)

            case (s, None) if isinstance(s, str):
                raise ValueError("Must supply metric when passing a string")

            case (s, (p, q, r)) if isinstance(s, str) and validate_metric((p, q, r)):
                if not all(c.isdigit() for c in s):
                    raise ValueError("Invalid characters in string for blade representation")
                self.blades = [Blade(s, 1, (p, q, r))]
                self._metric = (p, q, r)

            case (scalar, None) if isinstance(scalar, Scalar):
                raise ValueError("Must supply metric when passing a scalar")

            case (scalar, (p, q, r)) if isinstance(scalar, Scalar) and validate_metric((p, q, r)):
                self.blades = [Blade("", scalar, (p, q, r))]
                self._metric = (p, q, r)

            case _:
                raise ValueError("Invalid input combination for Cliff initialization")

            self.reduce()

        def reduce(self: Cliff) -> None:
            blade_dict = {}

            for blade in self.blades:
                key = blade.indices
                if key in blade_dict:
                    blade_dict[key].scalar += blade.scalar
                else:
                    blade_dict[key] = Blade(blade.indices, blade.scalar, blade._metric)

            self.blades = [blade for blade in blade_dict.values() if blade.scalar != 0]


def clifford(p: int, q: int, r: int) -> None:
    pass


def multivectors_test() -> None:
    print("multivectors.py test!")


if __name__ == "__main__":
    multivectors_test()

