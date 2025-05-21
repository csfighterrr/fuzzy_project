# ================== fuzzy_logic.py ==================
from typing import Callable, Dict, List, Tuple

class MembershipFunction:
    """Defines a fuzzy membership function over a domain."""
    def __init__(self, func: Callable[[float], float], name: str = None):
        self.func = func
        self.name = name or func.__name__

    def __call__(self, x: float) -> float:
        return max(0.0, min(1.0, self.func(x)))

class FuzzySet:
    """A fuzzy set defined by a membership function over a universe."""
    def __init__(self,
                 mu: MembershipFunction,
                 universe: List[float]):
        self.mu = mu
        self.universe = universe
        self.members: Dict[float, float] = {x: mu(x) for x in universe}

    def complement(self) -> 'FuzzySet':
        return FuzzySet(
            MembershipFunction(lambda x: 1 - self.mu(x), name=f"not_{self.mu.name}"),
            self.universe)

    @staticmethod
    def intersection(A: 'FuzzySet', B: 'FuzzySet') -> 'FuzzySet':
        return FuzzySet(
            MembershipFunction(lambda x: min(A.mu(x), B.mu(x)), name=f"({A.mu.name}_and_{B.mu.name})"),
            A.universe)

    @staticmethod
    def union(A: 'FuzzySet', B: 'FuzzySet') -> 'FuzzySet':
        return FuzzySet(
            MembershipFunction(lambda x: max(A.mu(x), B.mu(x)), name=f"({A.mu.name}_or_{B.mu.name})"),
            A.universe)

# Mamdani inference rule
class FuzzyRule:
    def __init__(self,
                 antecedent: Callable[[Dict[str, float]], float],
                 consequent: FuzzySet):
        self.antecedent = antecedent
        self.consequent = consequent

class FuzzyInferenceSystem:
    def __init__(self,
                 universe: List[float],
                 output_range: List[float]):
        self.universe = universe
        self.output_range = output_range
        self.rules: List[FuzzyRule] = []

    def add_rule(self, rule: FuzzyRule):
        self.rules.append(rule)

    def infer(self, inputs: Dict[str, float]) -> Dict[float, float]:
        # Mamdani: aggregate clipped consequents
        aggregated: Dict[float, float] = {y: 0.0 for y in self.output_range}
        for rule in self.rules:
            degree = rule.antecedent(inputs)
            for y in self.output_range:
                aggregated[y] = max(aggregated[y], min(degree, rule.consequent.mu(y)))
        return aggregated

    def defuzzify(self, aggregated: Dict[float, float]) -> float:
        # Centroid method
        num = sum(y * mu for y, mu in aggregated.items())
        den = sum(mu for mu in aggregated.values())
        return num / den if den != 0 else 0.0

# Triangular and Trapezoidal MFs

def triangular(a: float, b: float, c: float) -> MembershipFunction:
    def mu(x: float) -> float:
        if x <= a or x >= c:
            return 0.0
        return (x - a) / (b - a) if x < b else (c - x) / (c - b)
    return MembershipFunction(mu, name=f"tri_{a}_{b}_{c}")


def trapezoidal(a: float, b: float, c: float, d: float) -> MembershipFunction:
    def mu(x: float) -> float:
        if x <= a or x >= d:
            return 0.0
        if a < x < b:
            return (x - a) / (b - a)
        if b <= x <= c:
            return 1.0
        return (d - x) / (d - c)
    return MembershipFunction(mu, name=f"trap_{a}_{b}_{c}_{d}")

# ================== examples.py ==================
if __name__ == "__main__":
    # Universe
    x_universe = [i for i in range(0, 101)]  # e.g., speed 0-100

    # Define fuzzy sets: slow, medium, fast
    slow = FuzzySet(triangular(0, 0, 50), x_universe)
    medium = FuzzySet(triangular(25, 50, 75), x_universe)
    fast = FuzzySet(triangular(50, 100, 100), x_universe)

    # Show some membership values
    print("Membership of 30 in slow:", slow.mu(30))
    print("Membership of 30 in medium:", medium.mu(30))
    print("Membership of 30 in fast:", fast.mu(30))

    # Fuzzy inference: IF speed is slow THEN output is low
    output = FuzzySet(triangular(0, 0, 50), x_universe)
    engine = FuzzyInferenceSystem(x_universe, x_universe)
    # antecedent: lambda inputs: inputs['speed_is_slow']
    engine.add_rule(FuzzyRule(lambda inp: slow.mu(inp['speed']), output))

    inputs = {'speed': 30}
    agg = engine.infer({'speed': 30})
    crisp = engine.defuzzify(agg)
    print("Defuzzified output:", crisp)
