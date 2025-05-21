# ================== README.md ==================
"""
# Fuzzy Logic System

This Python project demonstrates fuzzy set theory, membership functions, and a Mamdani-style inference engine. It includes:

- Definition and use of fuzzy sets
- Triangular and trapezoidal membership functions
- Set operations: union, intersection, complement
- Mamdani fuzzy inference system
- Centroid defuzzification

## Getting Started

1. Clone or copy the project files
2. Run `examples.py` to see a simple fuzzy inference in action:

```bash
python examples.py
```

## Example Use Case
- Fuzzify speed into "slow", "medium", "fast"
- Define fuzzy rule: IF speed is slow THEN output is low
- Defuzzify the result

## File Structure

```
fuzzy_project/
├── fuzzy_logic.py    # Core fuzzy logic implementation
├── examples.py       # Demo script
└── README.md         # Project description
```
"""
# ================== examples.py ==================
from fuzzy import FuzzySet, FuzzyInferenceSystem, FuzzyRule, triangular

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
    engine.add_rule(FuzzyRule(lambda inp: slow.mu(inp['speed']), output))

    inputs = {'speed': 30}
    agg = engine.infer(inputs)
    crisp = engine.defuzzify(agg)
    print("Defuzzified output:", crisp)
