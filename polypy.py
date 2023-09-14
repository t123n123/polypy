# Polypy


class Polynomial:
    def __init__(self, coefs: list[float]):
        self._coefs = coefs

    @staticmethod
    def from_roots(roots: list[float]):  # (x - root1) * (x - root2) ...
        P = Polynomial([1])
        for root in roots:
            P = P * Polynomial([-root, 1])  # x - root

        return P

    @property
    def coefs(self):
        return self._coefs

    @coefs.setter
    def coefs(self, new_coefs: list[float]):
        self._coefs = new_coefs

    @property
    def degree(self):
        return len(self.coefs) - 1

    def eval(self, x):
        sum = 0
        exp = 1
        for coef in self.coefs:
            sum += coef * exp
            exp *= x

        return sum

    def __mul__(self, other):
        if type(other) == float:
            return Polynomial(list(map(lambda x: x * other, self.coefs)))
        elif type(other) == Polynomial:
            new_deg = self.degree + other.degree
            new_coefs: list[float] = [0] * (new_deg + 1)

            for i in range(self.degree + 1):
                for j in range(other.degree + 1):
                    new_coefs[i + j] += self.coefs[i] * other.coefs[j]
            return Polynomial(new_coefs)
        else:
            raise TypeError(f"Cannot multiply Polynomial with {type(other)}")

    def __add__(self, other):
        if type(other) == Polynomial:
            new_deg = max(self.degree, other.degree)
            new_coefs: list[float] = [0] * (new_deg + 1)

            for i in range(self.degree + 1):
                new_coefs[i] += self.coefs[i]

            for i in range(other.degree + 1):
                new_coefs[i] += other.coefs[i]

            return Polynomial(new_coefs)
        else:
            raise TypeError(f"Cannot add Polynomial with {type(other)}")

    @staticmethod
    def interpolate(samples: list[tuple[float, float]]):
        sampleX = list(map(lambda t: t[0], samples))

        if len(sampleX) != len(list(set(sampleX))):
            raise RuntimeError("Cannot interpolate polynomial with overlaping samples")

        P = Polynomial([0])

        for sampleX_i, sampleY_i in samples:
            P_i = Polynomial.from_roots(
                [sampleX_j for sampleX_j in sampleX if sampleX_j != sampleX_i]
            )

            P_i = P_i * (sampleY_i / P_i.eval(sampleX_i))

            P = P + P_i

        return P


A = Polynomial.interpolate([(0, 0), (1, 1), (2, 4)])  # intended x^2

print(A.eval(10))  # should print 100
